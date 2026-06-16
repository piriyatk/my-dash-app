import os
import pandas as pd
import streamlit as st
import networkx as nx
import plotly.graph_objects as go

from sqlalchemy import create_engine


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="SET50 Social Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================
# CUSTOM CSS
# =========================

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;500;600;700;800;900&display=swap');

        :root {
            --bg-0: #050816;
            --bg-1: #07111f;
            --card: rgba(15, 23, 42, 0.72);
            --card-2: rgba(17, 24, 39, 0.76);
            --line: rgba(148, 163, 184, 0.18);
            --text: #f8fafc;
            --muted: #94a3b8;
            --blue: #38bdf8;
            --cyan: #22d3ee;
            --violet: #a78bfa;
            --pink: #fb7185;
            --green: #34d399;
            --amber: #fbbf24;
        }

        html, body, [class*="css"] {
            font-family: 'Noto Sans Thai', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 12% 8%, rgba(56, 189, 248, 0.18) 0%, transparent 28%),
                radial-gradient(circle at 82% 12%, rgba(167, 139, 250, 0.18) 0%, transparent 30%),
                radial-gradient(circle at 80% 88%, rgba(34, 211, 238, 0.10) 0%, transparent 28%),
                linear-gradient(135deg, #030712 0%, #07111f 48%, #020617 100%);
            color: var(--text);
        }

        .block-container {
            max-width: 1580px;
            padding-top: 1.25rem;
            padding-bottom: 3.5rem;
        }

        header[data-testid="stHeader"] {
            background: rgba(2, 6, 23, 0.48);
            backdrop-filter: blur(18px);
            border-bottom: 1px solid rgba(148, 163, 184, 0.10);
        }

        section[data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 20% 0%, rgba(56, 189, 248, 0.16) 0%, transparent 28%),
                linear-gradient(180deg, rgba(15, 23, 42, 0.98), rgba(2, 6, 23, 0.98));
            border-right: 1px solid rgba(148, 163, 184, 0.16);
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #f8fafc;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #cbd5e1;
        }

        .main-shell {
            border-radius: 34px;
            padding: 1px;
            background:
                linear-gradient(135deg, rgba(56, 189, 248, 0.35), rgba(167, 139, 250, 0.22), rgba(15, 23, 42, 0.08));
            box-shadow:
                0 28px 90px rgba(0, 0, 0, 0.34),
                inset 0 1px 0 rgba(255, 255, 255, 0.06);
            margin-bottom: 22px;
        }

        .hero-card {
            position: relative;
            overflow: hidden;
            padding: 34px 36px;
            border-radius: 33px;
            background:
                radial-gradient(circle at 100% 0%, rgba(56, 189, 248, 0.22) 0%, transparent 32%),
                radial-gradient(circle at 0% 100%, rgba(167, 139, 250, 0.18) 0%, transparent 34%),
                linear-gradient(135deg, rgba(15, 23, 42, 0.90), rgba(17, 24, 39, 0.78));
            border: 1px solid rgba(255, 255, 255, 0.06);
        }

        .hero-card:before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
            transform: translateX(-100%);
            animation: shine 8s infinite;
        }

        @keyframes shine {
            0% { transform: translateX(-100%); }
            45% { transform: translateX(100%); }
            100% { transform: translateX(100%); }
        }

        .hero-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.55fr) minmax(300px, 0.7fr);
            gap: 28px;
            align-items: center;
            position: relative;
            z-index: 2;
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 12px;
            border-radius: 999px;
            background: rgba(56, 189, 248, 0.10);
            border: 1px solid rgba(125, 211, 252, 0.24);
            color: #bae6fd;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 14px;
        }

        .hero-title {
            font-size: clamp(38px, 4vw, 64px);
            font-weight: 900;
            letter-spacing: -0.07em;
            line-height: 0.98;
            margin: 0 0 14px 0;
            background: linear-gradient(90deg, #ffffff 0%, #bae6fd 38%, #c4b5fd 72%, #ffffff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            color: #cbd5e1;
            font-size: 16px;
            line-height: 1.8;
            max-width: 1000px;
        }

        .hero-panel {
            border-radius: 26px;
            padding: 22px;
            background:
                linear-gradient(135deg, rgba(2, 6, 23, 0.55), rgba(15, 23, 42, 0.70));
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
        }

        .hero-panel-title {
            color: #94a3b8;
            font-size: 13px;
            margin-bottom: 6px;
        }

        .hero-panel-value {
            color: white;
            font-size: 26px;
            font-weight: 850;
            letter-spacing: -0.04em;
            margin-bottom: 12px;
        }

        .hero-panel-note {
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.6;
        }

        .pill-row {
            margin-top: 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .pill {
            padding: 9px 13px;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(125, 211, 252, 0.20);
            color: #dbeafe;
            font-size: 13px;
            font-weight: 650;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
        }

        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 16px;
            margin: 18px 0 18px 0;
        }

        .kpi-card {
            position: relative;
            overflow: hidden;
            border-radius: 26px;
            padding: 20px 20px 18px 20px;
            background:
                radial-gradient(circle at 100% 0%, rgba(56, 189, 248, 0.12) 0%, transparent 42%),
                linear-gradient(145deg, rgba(15, 23, 42, 0.82), rgba(17, 24, 39, 0.62));
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow:
                0 22px 60px rgba(0, 0, 0, 0.22),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
        }

        .kpi-card:after {
            content: "";
            position: absolute;
            inset: auto 16px 0 16px;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(56,189,248,0.72), rgba(167,139,250,0.72), transparent);
            opacity: 0.55;
        }

        .kpi-icon {
            width: 34px;
            height: 34px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(125, 211, 252, 0.24);
            color: #7dd3fc;
            font-size: 16px;
            margin-bottom: 12px;
        }

        .kpi-label {
            color: #94a3b8;
            font-size: 13px;
            font-weight: 650;
            margin-bottom: 8px;
        }

        .kpi-value {
            color: #ffffff;
            font-size: 34px;
            font-weight: 900;
            letter-spacing: -0.06em;
            line-height: 1;
        }

        .kpi-sub {
            color: #64748b;
            font-size: 12px;
            margin-top: 8px;
        }

        .section-card {
            position: relative;
            border-radius: 30px;
            padding: 24px;
            background:
                linear-gradient(145deg, rgba(15, 23, 42, 0.76), rgba(2, 6, 23, 0.62));
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow:
                0 28px 84px rgba(0, 0, 0, 0.24),
                inset 0 1px 0 rgba(255,255,255,0.04);
            margin-top: 18px;
            margin-bottom: 18px;
        }

        .section-head {
            display: flex;
            justify-content: space-between;
            gap: 18px;
            align-items: flex-start;
            margin-bottom: 18px;
        }

        .section-title {
            color: #f8fafc;
            font-size: 26px;
            font-weight: 850;
            letter-spacing: -0.05em;
            margin-bottom: 4px;
        }

        .section-note {
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.7;
        }

        .legend-row {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: flex-end;
        }

        .legend-item {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 11px;
            border-radius: 999px;
            background: rgba(15,23,42,0.72);
            border: 1px solid rgba(148,163,184,0.14);
            color: #cbd5e1;
            font-size: 12px;
            font-weight: 650;
        }

        .dot {
            width: 9px;
            height: 9px;
            border-radius: 999px;
            display: inline-block;
        }

        .dot-red { background: #fb7185; box-shadow: 0 0 16px rgba(251,113,133,0.9); }
        .dot-blue { background: #38bdf8; box-shadow: 0 0 16px rgba(56,189,248,0.9); }
        .dot-line { background: #60a5fa; box-shadow: 0 0 16px rgba(96,165,250,0.9); }

        div[data-testid="stDataFrame"] {
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.20);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(2, 6, 23, 0.32);
            padding: 7px;
            border-radius: 999px;
            border: 1px solid rgba(148, 163, 184, 0.14);
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 999px;
            padding: 10px 20px;
            background: transparent;
            color: #cbd5e1;
            font-weight: 750;
        }

        .stTabs [aria-selected="true"] {
            background:
                linear-gradient(135deg, rgba(14, 165, 233, 0.34), rgba(168, 85, 247, 0.26));
            color: #ffffff;
            border: 1px solid rgba(125, 211, 252, 0.28);
            box-shadow: 0 12px 34px rgba(14, 165, 233, 0.14);
        }

        hr {
            border-color: rgba(148, 163, 184, 0.12);
        }

        .small-note {
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.7;
            margin-top: -2px;
            margin-bottom: 14px;
        }

        .footer-note {
            color: #64748b;
            font-size: 12px;
            text-align: right;
            margin-top: 8px;
        }

        @media (max-width: 1200px) {
            .hero-grid {
                grid-template-columns: 1fr;
            }

            .kpi-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 720px) {
            .kpi-grid {
                grid-template-columns: 1fr;
            }

            .hero-title {
                font-size: 38px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# DATABASE
# =========================

def get_database_url():
    try:
        if "DATABASE_URL" in st.secrets:
            return st.secrets["DATABASE_URL"]
    except Exception:
        pass

    return os.getenv("DATABASE_URL", "")


DATABASE_URL = get_database_url()

if DATABASE_URL.strip() == "":
    st.error("ยังไม่ได้ตั้งค่า DATABASE_URL ใน Streamlit Secrets")
    st.stop()


@st.cache_resource
def get_engine():
    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 30}
    )


engine = get_engine()


# =========================
# LOAD DATA
# =========================

@st.cache_data(ttl=600)
def load_data():
    query = """
    SELECT
        symbol,
        rank_no,
        shareholder_name,
        shares,
        percent_shares,
        as_of_date,
        source_url,
        created_at
    FROM set50
    WHERE shareholder_name IS NOT NULL
    ORDER BY symbol, CAST(rank_no AS INTEGER);
    """

    df = pd.read_sql(query, engine)

    df["symbol"] = df["symbol"].astype(str).str.strip()
    df["shareholder_name"] = df["shareholder_name"].astype(str).str.strip()

    df["rank_no_num"] = pd.to_numeric(df["rank_no"], errors="coerce")

    df["percent_num"] = (
        df["percent_shares"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["percent_num"] = pd.to_numeric(df["percent_num"], errors="coerce").fillna(0)

    df["shares_num"] = (
        df["shares"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["shares_num"] = pd.to_numeric(df["shares_num"], errors="coerce").fillna(0)

    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    return df


df = load_data()

if df.empty:
    st.warning("ยังไม่มีข้อมูลใน table set50")
    st.stop()


# =========================
# SIDEBAR FILTERS
# =========================

st.sidebar.markdown("## Control Panel")
st.sidebar.caption("ปรับมุมมองเครือข่ายและชุดข้อมูลที่ต้องการวิเคราะห์")

symbols = sorted(df["symbol"].dropna().unique().tolist())

quick_mode = st.sidebar.radio(
    "ชุดหุ้นเริ่มต้น",
    ["10 ตัวแรก", "ทั้งหมด", "เลือกเอง"],
    index=0
)

if quick_mode == "ทั้งหมด":
    default_symbols = symbols
elif quick_mode == "10 ตัวแรก":
    default_symbols = symbols[:10]
else:
    default_symbols = []

selected_symbols = st.sidebar.multiselect(
    "เลือกหุ้น",
    symbols,
    default=default_symbols
)

min_percent = st.sidebar.slider(
    "ขั้นต่ำสัดส่วนถือหุ้น (%)",
    min_value=0.0,
    max_value=float(max(df["percent_num"].max(), 1)),
    value=0.0,
    step=0.1
)

top_edges = st.sidebar.slider(
    "จำนวนเส้นสูงสุดในกราฟ",
    min_value=20,
    max_value=500,
    value=120,
    step=10
)

graph_mode = st.sidebar.radio(
    "รูปแบบเครือข่าย",
    [
        "หุ้น ↔ ผู้ถือหุ้น",
        "ผู้ถือหุ้น ↔ ผู้ถือหุ้นร่วม"
    ]
)

show_labels = st.sidebar.checkbox(
    "แสดงชื่อบนกราฟ",
    value=True
)

node_size_scale = st.sidebar.slider(
    "ขนาด node",
    min_value=1,
    max_value=8,
    value=4,
    step=1
)

st.sidebar.markdown("---")
st.sidebar.caption("แนะนำ: ถ้ากราฟรก ให้ลดจำนวนเส้น หรือเพิ่มขั้นต่ำสัดส่วนถือหุ้น")


# =========================
# FILTER DATA
# =========================

filtered = df.copy()

if selected_symbols:
    filtered = filtered[filtered["symbol"].isin(selected_symbols)]

filtered = filtered[filtered["percent_num"] >= min_percent]

if filtered.empty:
    st.warning("ไม่พบข้อมูลตามตัวกรองที่เลือก")
    st.stop()


# =========================
# KPI VALUES
# =========================

latest_update = filtered["created_at"].dropna().max()
latest_update_text = "-"
if pd.notna(latest_update):
    latest_update_text = latest_update.strftime("%Y-%m-%d %H:%M")

stock_count = filtered["symbol"].nunique()
holder_count = filtered["shareholder_name"].nunique()
edge_count = len(filtered)
total_percent = filtered["percent_num"].sum()


# =========================
# HERO
# =========================

st.markdown(
    f"""
    <div class="main-shell">
        <div class="hero-card">
            <div class="hero-grid">
                <div>
                    <div class="eyebrow">SET50 · CAPITAL NETWORK INTELLIGENCE</div>
                    <div class="hero-title">Social Analytics<br/>Dashboard</div>
                    <div class="hero-subtitle">
                        วิเคราะห์โครงข่ายผู้ถือหุ้น SET50 จาก Neon Database เพื่อค้นหา hub สำคัญ
                        กลุ่ม nominee ผู้ถือหุ้นร่วม และความสัมพันธ์เชิงอำนาจในเครือข่ายทุนไทย
                    </div>
                    <div class="pill-row">
                        <div class="pill">Interactive 3D Network</div>
                        <div class="pill">PageRank</div>
                        <div class="pill">Degree Centrality</div>
                        <div class="pill">Major Shareholders</div>
                        <div class="pill">Neon PostgreSQL</div>
                    </div>
                </div>
                <div class="hero-panel">
                    <div class="hero-panel-title">Current View</div>
                    <div class="hero-panel-value">{stock_count:,} Stocks · {holder_count:,} Holders</div>
                    <div class="hero-panel-note">
                        Mode: {graph_mode}<br/>
                        Edge limit: {top_edges:,}<br/>
                        Last sync: {latest_update_text}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# KPI CARDS
# =========================

st.markdown(
    f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-icon">◆</div>
            <div class="kpi-label">จำนวนหุ้นในมุมมองนี้</div>
            <div class="kpi-value">{stock_count:,}</div>
            <div class="kpi-sub">unique symbols</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">●</div>
            <div class="kpi-label">จำนวนผู้ถือหุ้น</div>
            <div class="kpi-value">{holder_count:,}</div>
            <div class="kpi-sub">unique shareholders</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">↔</div>
            <div class="kpi-label">จำนวนความเชื่อมโยง</div>
            <div class="kpi-value">{edge_count:,}</div>
            <div class="kpi-sub">stock-holder relations</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">%</div>
            <div class="kpi-label">สัดส่วนถือหุ้นรวม</div>
            <div class="kpi-value">{total_percent:,.2f}%</div>
            <div class="kpi-sub">sum of selected holdings</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">⏱</div>
            <div class="kpi-label">อัปเดตล่าสุด</div>
            <div class="kpi-value" style="font-size: 25px;">{latest_update_text}</div>
            <div class="kpi-sub">Neon table: set50</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# BUILD GRAPH
# =========================

def build_bipartite_graph(data):
    G = nx.Graph()

    data = data.sort_values("percent_num", ascending=False).head(top_edges)

    for _, row in data.iterrows():
        stock = f"หุ้น: {row['symbol']}"
        holder = f"ผู้ถือหุ้น: {row['shareholder_name']}"

        G.add_node(
            stock,
            node_type="stock",
            label=row["symbol"]
        )

        G.add_node(
            holder,
            node_type="holder",
            label=row["shareholder_name"]
        )

        G.add_edge(
            stock,
            holder,
            weight=max(float(row["percent_num"]), 0.01),
            percent=float(row["percent_num"]),
            shares=float(row["shares_num"])
        )

    return G


def build_coholder_graph(data):
    G = nx.Graph()

    grouped = data.groupby("symbol")

    for symbol, group in grouped:
        holder_list = (
            group["shareholder_name"]
            .dropna()
            .drop_duplicates()
            .tolist()
        )

        for holder in holder_list:
            G.add_node(
                holder,
                node_type="holder",
                label=holder
            )

        for i in range(len(holder_list)):
            for j in range(i + 1, len(holder_list)):
                h1 = holder_list[i]
                h2 = holder_list[j]

                if G.has_edge(h1, h2):
                    G[h1][h2]["weight"] += 1
                    G[h1][h2]["stocks"].append(symbol)
                else:
                    G.add_edge(
                        h1,
                        h2,
                        weight=1,
                        stocks=[symbol]
                    )

    edges_sorted = sorted(
        G.edges(data=True),
        key=lambda x: x[2].get("weight", 0),
        reverse=True
    )[:top_edges]

    H = nx.Graph()

    for u, v, attr in edges_sorted:
        H.add_node(
            u,
            node_type="holder",
            label=u
        )
        H.add_node(
            v,
            node_type="holder",
            label=v
        )
        H.add_edge(u, v, **attr)

    return H


if graph_mode == "หุ้น ↔ ผู้ถือหุ้น":
    G = build_bipartite_graph(filtered)
else:
    G = build_coholder_graph(filtered)

if G.number_of_nodes() == 0:
    st.warning("ไม่มีข้อมูลพอสำหรับสร้างกราฟ")
    st.stop()

degree_centrality = nx.degree_centrality(G)

try:
    pagerank = nx.pagerank(G, weight="weight")
except Exception:
    pagerank = {node: 0 for node in G.nodes()}


# =========================
# DATAFRAMES
# =========================

holder_summary = (
    filtered
    .groupby("shareholder_name")
    .agg(
        stock_count=("symbol", "nunique"),
        total_percent=("percent_num", "sum"),
        total_shares=("shares_num", "sum")
    )
    .reset_index()
    .sort_values(["stock_count", "total_percent"], ascending=False)
)

holder_summary_show = holder_summary.rename(columns={
    "shareholder_name": "ชื่อผู้ถือหุ้น",
    "stock_count": "จำนวนหุ้นที่ถือใน SET50",
    "total_percent": "สัดส่วนถือหุ้นรวม (%)",
    "total_shares": "จำนวนหุ้นรวม"
})

centrality_df = pd.DataFrame({
    "node": list(G.nodes()),
    "node_type": [G.nodes[n].get("node_type", "") for n in G.nodes()],
    "degree": [G.degree(n) for n in G.nodes()],
    "degree_centrality": [degree_centrality.get(n, 0) for n in G.nodes()],
    "pagerank": [pagerank.get(n, 0) for n in G.nodes()],
})

centrality_df = centrality_df.sort_values("pagerank", ascending=False)

centrality_df_show = centrality_df.rename(columns={
    "node": "ชื่อโหนด",
    "node_type": "ประเภทโหนด",
    "degree": "จำนวนเส้นเชื่อม",
    "degree_centrality": "ค่าความเป็นศูนย์กลาง",
    "pagerank": "ค่า PageRank"
})

centrality_df_show["ประเภทโหนด"] = centrality_df_show["ประเภทโหนด"].replace({
    "stock": "หุ้น",
    "holder": "ผู้ถือหุ้น"
})

raw_show = filtered.rename(columns={
    "symbol": "หุ้น",
    "rank_no": "ลำดับ",
    "shareholder_name": "ชื่อผู้ถือหุ้น",
    "shares": "จำนวนหุ้น",
    "percent_shares": "สัดส่วนหุ้น (%)",
    "as_of_date": "วันที่ข้อมูล",
    "source_url": "แหล่งข้อมูล",
    "created_at": "วันที่บันทึกข้อมูล",
    "rank_no_num": "ลำดับตัวเลข",
    "percent_num": "สัดส่วนหุ้นแบบตัวเลข",
    "shares_num": "จำนวนหุ้นแบบตัวเลข"
})


# =========================
# TABS
# =========================

tab1, tab2, tab3 = st.tabs([
    "ภาพรวมผู้ถือหุ้น",
    "Network Graph 3D",
    "ข้อมูลดิบ"
])


with tab1:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-head">
                <div>
                    <div class="section-title">Major Shareholder Ranking</div>
                    <div class="section-note">
                        จัดอันดับผู้ถือหุ้นตามจำนวนหุ้น SET50 ที่เชื่อมโยง และสัดส่วนถือหุ้นรวมในชุดข้อมูลที่เลือก
                    </div>
                </div>
                <div class="legend-row">
                    <div class="legend-item"><span class="dot dot-blue"></span> Shareholder</div>
                    <div class="legend-item"><span class="dot dot-red"></span> Stock</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        holder_summary_show,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ชื่อผู้ถือหุ้น": st.column_config.TextColumn("ชื่อผู้ถือหุ้น", width="large"),
            "จำนวนหุ้นที่ถือใน SET50": st.column_config.NumberColumn("จำนวนหุ้นที่ถือใน SET50", format="%d"),
            "สัดส่วนถือหุ้นรวม (%)": st.column_config.NumberColumn("สัดส่วนถือหุ้นรวม (%)", format="%.2f"),
            "จำนวนหุ้นรวม": st.column_config.NumberColumn("จำนวนหุ้นรวม", format="%d"),
        }
    )

    st.markdown("<br/>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-card">
            <div class="section-head">
                <div>
                    <div class="section-title">Network Centrality</div>
                    <div class="section-note">
                        PageRank ใช้มอง node ที่มีอิทธิพลเชิงโครงข่าย ส่วน Degree ใช้มองจำนวนการเชื่อมโดยตรง
                    </div>
                </div>
                <div class="legend-row">
                    <div class="legend-item">PageRank</div>
                    <div class="legend-item">Degree Centrality</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        centrality_df_show,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ชื่อโหนด": st.column_config.TextColumn("ชื่อโหนด", width="large"),
            "ประเภทโหนด": st.column_config.TextColumn("ประเภทโหนด"),
            "จำนวนเส้นเชื่อม": st.column_config.NumberColumn("จำนวนเส้นเชื่อม", format="%d"),
            "ค่าความเป็นศูนย์กลาง": st.column_config.NumberColumn("ค่าความเป็นศูนย์กลาง", format="%.6f"),
            "ค่า PageRank": st.column_config.NumberColumn("ค่า PageRank", format="%.6f"),
        }
    )


with tab2:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-head">
                <div>
                    <div class="section-title">Interactive 3D Network</div>
                    <div class="section-note">
                        ลากเพื่อหมุน · Scroll เพื่อซูม · Hover เพื่อดูรายละเอียด node และ edge
                    </div>
                </div>
                <div class="legend-row">
                    <div class="legend-item"><span class="dot dot-red"></span> หุ้น</div>
                    <div class="legend-item"><span class="dot dot-blue"></span> ผู้ถือหุ้น</div>
                    <div class="legend-item"><span class="dot dot-line"></span> ความเชื่อมโยง</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    pos = nx.spring_layout(
        G,
        dim=3,
        k=0.95,
        iterations=140,
        seed=42,
        weight="weight"
    )

    edge_traces = []

    for u, v, attr in G.edges(data=True):
        x0, y0, z0 = pos[u]
        x1, y1, z1 = pos[v]

        weight = float(attr.get("weight", 1))
        edge_width = min(max(weight / 5, 1.2), 7)

        if graph_mode == "หุ้น ↔ ผู้ถือหุ้น":
            hover_text = (
                f"<b>{G.nodes[u].get('label', u)}</b>"
                f" ↔ "
                f"<b>{G.nodes[v].get('label', v)}</b><br>"
                f"ถือหุ้น: {attr.get('percent', 0):,.2f}%<br>"
                f"จำนวนหุ้น: {attr.get('shares', 0):,.0f}"
            )
        else:
            stocks = ", ".join(attr.get("stocks", []))
            hover_text = (
                f"<b>{G.nodes[u].get('label', u)}</b>"
                f" ↔ "
                f"<b>{G.nodes[v].get('label', v)}</b><br>"
                f"ถือหุ้นร่วมกัน: {attr.get('weight', 0)} ตัว<br>"
                f"หุ้นร่วม: {stocks}"
            )

        edge_traces.append(
            go.Scatter3d(
                x=[x0, x1, None],
                y=[y0, y1, None],
                z=[z0, z1, None],
                mode="lines",
                line=dict(
                    width=edge_width,
                    color="rgba(96, 165, 250, 0.38)"
                ),
                hoverinfo="text",
                hovertext=hover_text,
                showlegend=False
            )
        )

    node_x = []
    node_y = []
    node_z = []
    node_text = []
    node_label = []
    node_size = []
    node_color = []

    for node in G.nodes():
        x, y, z = pos[node]

        deg = G.degree(node)
        pr = pagerank.get(node, 0)
        node_type = G.nodes[node].get("node_type", "")
        label = G.nodes[node].get("label", str(node))

        node_x.append(x)
        node_y.append(y)
        node_z.append(z)

        node_size.append(9 + deg * node_size_scale)

        if node_type == "stock":
            node_color.append("#fb7185")
        else:
            node_color.append("#38bdf8")

        node_label.append(label[:22] if show_labels else "")

        node_text.append(
            f"<b>{label}</b><br>"
            f"ประเภท: {'หุ้น' if node_type == 'stock' else 'ผู้ถือหุ้น'}<br>"
            f"จำนวนเส้นเชื่อม: {deg}<br>"
            f"Degree Centrality: {degree_centrality.get(node, 0):.6f}<br>"
            f"PageRank: {pr:.6f}"
        )

    node_trace = go.Scatter3d(
        x=node_x,
        y=node_y,
        z=node_z,
        mode="markers+text",
        text=node_label,
        textposition="top center",
        hovertext=node_text,
        hoverinfo="text",
        marker=dict(
            size=node_size,
            color=node_color,
            opacity=0.96,
            line=dict(
                width=1.5,
                color="rgba(255,255,255,0.95)"
            )
        ),
        textfont=dict(
            size=11,
            color="white"
        ),
        showlegend=False
    )

    fig = go.Figure(
        data=edge_traces + [node_trace]
    )

    fig.update_layout(
        height=880,
        showlegend=False,
        hovermode="closest",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, b=0, t=32),
        scene=dict(
            bgcolor="rgba(0,0,0,0)",
            xaxis=dict(visible=False, showbackground=False, showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(visible=False, showbackground=False, showgrid=False, showticklabels=False, zeroline=False),
            zaxis=dict(visible=False, showbackground=False, showgrid=False, showticklabels=False, zeroline=False),
            camera=dict(
                eye=dict(x=1.65, y=1.65, z=1.30)
            )
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "scrollZoom": True,
            "displayModeBar": True,
            "displaylogo": False,
            "modeBarButtonsToRemove": [
                "select2d",
                "lasso2d"
            ]
        }
    )

    st.markdown(
        '<div class="footer-note">Tip: ลดจำนวนเส้นหรือเพิ่มขั้นต่ำ % หุ้น เพื่อให้ network อ่านง่ายขึ้น</div>',
        unsafe_allow_html=True
    )


with tab3:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-head">
                <div>
                    <div class="section-title">Raw Data from Neon</div>
                    <div class="section-note">
                        ข้อมูลดิบที่ผ่านตัวกรองปัจจุบัน ใช้ตรวจสอบรายละเอียดรายหุ้น ผู้ถือหุ้น และแหล่งข้อมูล
                    </div>
                </div>
                <div class="legend-row">
                    <div class="legend-item">PostgreSQL</div>
                    <div class="legend-item">Table: set50</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        raw_show,
        use_container_width=True,
        hide_index=True,
        column_config={
            "หุ้น": st.column_config.TextColumn("หุ้น"),
            "ลำดับ": st.column_config.TextColumn("ลำดับ"),
            "ชื่อผู้ถือหุ้น": st.column_config.TextColumn("ชื่อผู้ถือหุ้น", width="large"),
            "จำนวนหุ้น": st.column_config.TextColumn("จำนวนหุ้น"),
            "สัดส่วนหุ้น (%)": st.column_config.TextColumn("สัดส่วนหุ้น (%)"),
            "วันที่ข้อมูล": st.column_config.TextColumn("วันที่ข้อมูล"),
            "แหล่งข้อมูล": st.column_config.LinkColumn("แหล่งข้อมูล"),
            "วันที่บันทึกข้อมูล": st.column_config.DatetimeColumn("วันที่บันทึกข้อมูล"),
            "ลำดับตัวเลข": st.column_config.NumberColumn("ลำดับตัวเลข"),
            "สัดส่วนหุ้นแบบตัวเลข": st.column_config.NumberColumn("สัดส่วนหุ้นแบบตัวเลข", format="%.2f"),
            "จำนวนหุ้นแบบตัวเลข": st.column_config.NumberColumn("จำนวนหุ้นแบบตัวเลข", format="%d"),
        }
    )
