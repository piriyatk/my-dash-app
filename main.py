from playwright.async_api import async_playwright
import pandas as pd
import asyncio
import re
import os

from sqlalchemy import create_engine, text


# =========================
# CONFIG
# =========================

SET50_URL = "https://www.set.or.th/th/market/index/set50/overview"
SHAREHOLDER_URL = "https://www.set.or.th/th/market/product/stock/quote/{symbol}/major-shareholders"

# อ่าน Connection string จาก GitHub Secrets หรือ Environment Variable
# GitHub Actions ต้องตั้ง Secret ชื่อ DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", "")

# ชื่อตารางใน Neon
TABLE_NAME = "set50"

# ถ้าดึงนิ่งแล้วค่อยลองเพิ่มเป็น 5
CONCURRENT_PAGES = 3


# =========================
# DATABASE ENGINE
# =========================

def get_engine():
    if DATABASE_URL.strip() == "":
        raise Exception("ยังไม่ได้ตั้งค่า DATABASE_URL จาก Neon ใน GitHub Secrets")

    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=1,
        max_overflow=2,
        connect_args={
            "connect_timeout": 30
        }
    )


# =========================
# CLEAN TEXT
# =========================

def clean_text(x):
    if pd.isna(x):
        return ""
    return re.sub(r"\s+", " ", str(x)).strip()


# =========================
# SAFE GOTO
# =========================

async def safe_goto(page, url, timeout=120000, retries=4):
    last_error = None

    for _ in range(retries):
        try:
            await page.goto(
                url,
                wait_until="commit",
                timeout=timeout
            )
            return True

        except Exception as e:
            last_error = e

            try:
                await page.wait_for_timeout(3000)
            except Exception:
                pass

            try:
                await page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=timeout
                )
                return True

            except Exception as e2:
                last_error = e2

                try:
                    await page.wait_for_timeout(5000)
                except Exception:
                    pass

    raise last_error


# =========================
# EXTRACT AS OF DATE
# =========================

def extract_as_of_date(text):
    patterns = [
        r"ภาพรวมข้อมูลผู้ถือหุ้น\s*ณ วันที่\s*([^\n]+)",
        r"ข้อมูล.*?ณ วันที่\s*([^\n]+)",
        r"ณ วันที่\s*([^\n]+)",
        r"วันที่ปิดสมุดทะเบียน\s*([^\n]+)",
    ]

    for p in patterns:
        m = re.search(p, text)
        if m:
            return clean_text(m.group(1))

    return ""


# =========================
# GET SET50 SYMBOLS
# =========================

async def get_set50_symbols(page):
    await safe_goto(page, SET50_URL)

    await page.wait_for_function(
        """
        () => {
            const links = [...document.querySelectorAll("a[href*='/stock/quote/']")];

            const symbols = new Set(
                links
                    .map(a => {
                        const m = a.href.match(/\\/stock\\/quote\\/([A-Z0-9]+)\\//);
                        return m ? m[1] : null;
                    })
                    .filter(Boolean)
            );

            return symbols.size >= 50;
        }
        """,
        timeout=60000
    )

    symbols = await page.eval_on_selector_all(
        "a[href*='/stock/quote/']",
        """
        els => {
            const symbols = [];

            for (const a of els) {
                const m = a.href.match(/\\/stock\\/quote\\/([A-Z0-9]+)\\//);

                if (m) {
                    const symbol = m[1].trim().toUpperCase();

                    if (!symbols.includes(symbol)) {
                        symbols.push(symbol);
                    }
                }

                if (symbols.length >= 50) break;
            }

            return symbols;
        }
        """
    )

    return symbols[:50]


# =========================
# EXTRACT SHAREHOLDER TABLE
# =========================

async def extract_shareholder_table_from_page(page, symbol, url):
    rows = await page.evaluate(
        """
        () => {
            const result = [];

            const normalize = (x) =>
                (x || "").replace(/\\s+/g, " ").trim();

            const tables = [...document.querySelectorAll("table")];

            for (const table of tables) {
                const trs = [...table.querySelectorAll("tbody tr, tr")];

                for (const tr of trs) {
                    const cells = [...tr.querySelectorAll("td")].map(td =>
                        normalize(td.innerText)
                    );

                    if (cells.length < 4) {
                        continue;
                    }

                    const no = cells[0];
                    const shareholder = cells[1];
                    const shares = cells[2];
                    const percent = cells[3];

                    if (!/^\\d+$/.test(no)) {
                        continue;
                    }

                    if (!shareholder || shareholder === "ไม่มีข้อมูล") {
                        continue;
                    }

                    if (!shares || !percent) {
                        continue;
                    }

                    result.push({
                        "ลำดับ": no,
                        "ผู้ถือหุ้น": shareholder,
                        "จำนวนหุ้น (หุ้น)": shares,
                        "%หุ้น": percent
                    });
                }
            }

            return result;
        }
        """
    )

    if not rows:
        return None

    df = pd.DataFrame(rows)
    df = df.drop_duplicates()

    df.insert(0, "Symbol", symbol)
    df["SourceURL"] = url

    return df


# =========================
# FETCH SHAREHOLDERS
# =========================

async def fetch_major_shareholders(context, symbol, sem):
    async with sem:
        page = await context.new_page()
        url = SHAREHOLDER_URL.format(symbol=symbol)

        try:
            await safe_goto(page, url)

            # ช่วยให้บางหน้าที่ layout โหลดช้า เช่น TCAP / TIDLOR / TISCO แสดงตารางทัน
            try:
                await page.wait_for_timeout(3000)
                await page.mouse.wheel(0, 2500)
                await page.wait_for_timeout(2000)
            except Exception:
                pass

            try:
                await page.wait_for_function(
                    """
                    () => {
                        const text = document.body.innerText || "";

                        const hasShareholderSection =
                            text.includes("ข้อมูลผู้ถือหุ้น") ||
                            text.includes("ผู้ถือหุ้น*") ||
                            text.includes("ผู้ถือหุ้น");

                        const hasRealRows =
                            [...document.querySelectorAll("table tbody tr, table tr")]
                                .some(tr => {
                                    const cells = [...tr.querySelectorAll("td")].map(td =>
                                        (td.innerText || "").replace(/\\s+/g, " ").trim()
                                    );

                                    return cells.length >= 4 && /^\\d+$/.test(cells[0]);
                                });

                        return hasShareholderSection && hasRealRows;
                    }
                    """,
                    timeout=60000
                )
            except Exception:
                pass

            df = None

            # retry เผื่อ SET โหลดข้อมูลช้า
            for _ in range(30):
                df = await extract_shareholder_table_from_page(page, symbol, url)

                if df is not None and len(df) > 0:
                    break

                try:
                    await page.mouse.wheel(0, 1200)
                except Exception:
                    pass

                await page.wait_for_timeout(1000)

            try:
                body_text = await page.locator("body").inner_text(timeout=10000)
            except Exception:
                body_text = ""

            as_of_date = extract_as_of_date(body_text)

            if df is None or len(df) == 0:
                print(f"ไม่พบข้อมูล: {symbol}")

                return None, {
                    "Symbol": symbol,
                    "URL": url,
                    "Error": "ไม่พบตารางผู้ถือหุ้นจริงบนหน้า"
                }

            df["AsOfDate"] = as_of_date

            print(f"สำเร็จ: {symbol} | {len(df)} rows")

            return df, None

        except Exception as e:
            print(f"ล้มเหลว: {symbol} | {e}")

            return None, {
                "Symbol": symbol,
                "URL": url,
                "Error": str(e)
            }

        finally:
            try:
                await page.close()
            except Exception:
                pass


# =========================
# MAIN SCRAPER
# =========================

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-extensions",
                "--disable-background-networking",
                "--disable-sync",
                "--disable-default-apps",
                "--mute-audio",
                "--disable-notifications",
                "--blink-settings=imagesEnabled=false",
            ]
        )

        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:151.0) "
                "Gecko/20100101 Firefox/151.0"
            ),
            locale="th-TH",
            viewport={"width": 1280, "height": 720}
        )

        context.set_default_navigation_timeout(120000)
        context.set_default_timeout(120000)

        async def block_unneeded(route):
            rtype = route.request.resource_type
            req_url = route.request.url.lower()

            blocked_types = {
                "image",
                "font",
                "media",
            }

            blocked_domains = [
                "google-analytics",
                "googletagmanager",
                "doubleclick",
                "facebook",
                "clarity",
                "hotjar",
                "youtube",
                "ytimg",
            ]

            if rtype in blocked_types or any(d in req_url for d in blocked_domains):
                await route.abort()
            else:
                await route.continue_()

        await context.route("**/*", block_unneeded)

        page = await context.new_page()

        print("กำลังดึงรายชื่อ SET50...")
        set50_TickerSymbol = await get_set50_symbols(page)
        await page.close()

        print(f"พบ SET50 ทั้งหมด {len(set50_TickerSymbol)} ตัว")
        print(set50_TickerSymbol)

        sem = asyncio.Semaphore(CONCURRENT_PAGES)

        tasks = [
            fetch_major_shareholders(context, symbol, sem)
            for symbol in set50_TickerSymbol
        ]

        results = await asyncio.gather(*tasks)

        all_dfs = []
        failed_rows = []

        for df, err in results:
            if df is not None:
                all_dfs.append(df)

            if err is not None:
                failed_rows.append(err)

        if all_dfs:
            set50_detail = pd.concat(all_dfs, ignore_index=True)
        else:
            set50_detail = pd.DataFrame()

        failed_df = pd.DataFrame(failed_rows)

        await browser.close()

        return set50_TickerSymbol, set50_detail, failed_df


# =========================
# TEST NEON CONNECTION
# =========================

def test_neon_connection():
    engine = get_engine()

    with engine.connect() as conn:
        now = conn.execute(text("SELECT NOW();")).scalar()
        print(f"เชื่อม Neon สำเร็จ: {now}")


# =========================
# PREPARE set50_detail
# =========================

def prepare_set50_detail(set50_detail):
    if set50_detail is None or set50_detail.empty:
        return pd.DataFrame()

    df = set50_detail.copy()

    # เปลี่ยนชื่อคอลัมน์จาก set50_detail ให้เป็นชื่อ field ใน table set50
    df = df.rename(columns={
        "Symbol": "symbol",
        "ลำดับ": "rank_no",
        "ผู้ถือหุ้น": "shareholder_name",
        "จำนวนหุ้น (หุ้น)": "shares",
        "%หุ้น": "percent_shares",
        "AsOfDate": "as_of_date",
        "SourceURL": "source_url",
    })

    keep_cols = [
        "symbol",
        "rank_no",
        "shareholder_name",
        "shares",
        "percent_shares",
        "as_of_date",
        "source_url",
    ]

    df = df[keep_cols]

    for col in keep_cols:
        df[col] = df[col].astype(str).str.strip()

    return df


# =========================
# SAVE ONLY set50_detail TO NEON
# =========================

def save_set50_detail_to_neon(set50_detail):
    # เอาเข้าเฉพาะ set50_detail เท่านั้น
    if set50_detail is None or set50_detail.empty:
        print("set50_detail ว่าง ไม่มีข้อมูลให้บันทึกลง Neon")
        return

    df = prepare_set50_detail(set50_detail)

    if df.empty:
        print("หลังเตรียมข้อมูลแล้วว่าง ไม่มีข้อมูลให้บันทึกลง Neon")
        return

    engine = get_engine()

    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id BIGSERIAL PRIMARY KEY,
        symbol TEXT NOT NULL,
        rank_no TEXT,
        shareholder_name TEXT,
        shares TEXT,
        percent_shares TEXT,
        as_of_date TEXT,
        source_url TEXT,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """

    create_index_symbol_sql = f"""
    CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_symbol
    ON {TABLE_NAME} (symbol);
    """

    create_index_created_at_sql = f"""
    CREATE INDEX IF NOT EXISTS idx_{TABLE_NAME}_created_at
    ON {TABLE_NAME} (created_at);
    """

    with engine.begin() as conn:
        print(f"ตรวจสอบ / สร้าง table {TABLE_NAME} ถ้ายังไม่มี...")
        conn.execute(text(create_table_sql))

        print(f"ตรวจสอบ / สร้าง index ของ table {TABLE_NAME}...")
        conn.execute(text(create_index_symbol_sql))
        conn.execute(text(create_index_created_at_sql))

        print(f"ล้างข้อมูลเก่าใน table {TABLE_NAME}...")
        conn.execute(text(f"TRUNCATE TABLE {TABLE_NAME} RESTART IDENTITY;"))

    print(f"กำลังนำเข้าเฉพาะ set50_detail ไปยัง table {TABLE_NAME}...")

    df.to_sql(
        TABLE_NAME,
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000
    )

    print(f"นำเข้า set50_detail ลง Neon table {TABLE_NAME} สำเร็จ: {len(df)} rows")


# =========================
# RUN
# =========================

if __name__ == "__main__":
    print("เริ่มทดสอบการเชื่อมต่อ Neon...")
    test_neon_connection()

    print("\nเริ่มดึงข้อมูล SET50...")
    set50_TickerSymbol, set50_detail, failed_df = asyncio.run(main())

    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 300)
    pd.set_option("display.max_colwidth", None)

    print("\n===== SET50 DETAIL DATAFRAME =====")
    print(set50_detail)

    if not failed_df.empty:
        print("\n===== FAILED DATAFRAME เฉพาะแสดงผล ไม่ได้นำเข้า Neon =====")
        print(failed_df)

    print("\nเริ่มบันทึกเฉพาะ set50_detail เข้า Neon table set50...")
    save_set50_detail_to_neon(set50_detail)

    print("\nเสร็จทั้งหมด")
