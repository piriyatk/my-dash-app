import streamlit as st


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="SET50 Dashboard",
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
                radial-gradient(circle at 10% 8%, rgba(56, 189, 248, 0.20) 0%, transparent 28%),
                radial-gradient(circle at 86% 10%, rgba(167, 139, 250, 0.20) 0%, transparent 32%),
                radial-gradient(circle at 82% 86%, rgba(34, 211, 238, 0.10) 0%, transparent 30%),
                linear-gradient(135deg, #030712 0%, #07111f 48%, #020617 100%);
            color: var(--text);
        }

        .block-container {
            max-width: 1520px;
            padding-top: 1.4rem;
            padding-bottom: 3.5rem;
        }

        header[data-testid="stHeader"] {
            background: rgba(2, 6, 23, 0.50);
            backdrop-filter: blur(18px);
            border-bottom: 1px solid rgba(148, 163, 184, 0.10);
        }

        section[data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 20% 0%, rgba(56, 189, 248, 0.16) 0%, transparent 30%),
                linear-gradient(180deg, rgba(15, 23, 42, 0.98), rgba(2, 6, 23, 0.98));
            border-right: 1px solid rgba(148, 163, 184, 0.16);
        }

        .hero-shell {
            border-radius: 34px;
            padding: 1px;
            background:
                linear-gradient(135deg, rgba(56, 189, 248, 0.38), rgba(167, 139, 250, 0.24), rgba(15, 23, 42, 0.08));
            box-shadow:
                0 30px 90px rgba(0, 0, 0, 0.36),
                inset 0 1px 0 rgba(255, 255, 255, 0.06);
            margin-bottom: 22px;
        }

        .hero-card {
            position: relative;
            overflow: hidden;
            border-radius: 33px;
            padding: 42px 42px;
            background:
                radial-gradient(circle at 100% 0%, rgba(56, 189, 248, 0.22) 0%, transparent 34%),
                radial-gradient(circle at 0% 100%, rgba(167, 139, 250, 0.20) 0%, transparent 36%),
                linear-gradient(135deg, rgba(15, 23, 42, 0.92), rgba(17, 24, 39, 0.80));
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
            position: relative;
            z-index: 2;
            display: grid;
            grid-template-columns: minmax(0, 1.45fr) minmax(300px, 0.8fr);
            gap: 32px;
            align-items: center;
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
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 16px;
        }

        .hero-title {
            font-size: clamp(42px, 5vw, 76px);
            font-weight: 900;
            letter-spacing: -0.075em;
            line-height: 0.98;
            margin: 0 0 18px 0;
            background: linear-gradient(90deg, #ffffff 0%, #bae6fd 34%, #c4b5fd 72%, #ffffff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            color: #cbd5e1;
            font-size: 17px;
            line-height: 1.85;
            max-width: 960px;
        }

        .hero-panel {
            border-radius: 28px;
            padding: 24px;
            background:
                linear-gradient(135deg, rgba(2, 6, 23, 0.55), rgba(15, 23, 42, 0.72));
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.05),
                0 22px 60px rgba(0,0,0,0.20);
        }

        .panel-label {
            color: #94a3b8;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .panel-value {
            color: #ffffff;
            font-size: 30px;
            font-weight: 900;
            letter-spacing: -0.05em;
            line-height: 1.12;
            margin-bottom: 14px;
        }

        .panel-note {
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.7;
        }

        .pill-row {
            margin-top: 22px;
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
            font-weight: 700;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
        }

        .section-title {
            font-size: 28px;
            font-weight: 900;
            letter-spacing: -0.055em;
            color: #f8fafc;
            margin: 26px 0 6px 0;
        }

        .section-subtitle {
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.7;
            margin-bottom: 18px;
        }

        .menu-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 16px;
            margin-top: 18px;
            margin-bottom: 22px;
        }

        .menu-card {
            position: relative;
            overflow: hidden;
            min-height: 210px;
            border-radius: 28px;
            padding: 24px;
            background:
                radial-gradient(circle at 100% 0%, rgba(56, 189, 248, 0.12) 0%, transparent 42%),
                linear-gradient(145deg, rgba(15, 23, 42, 0.82), rgba(17, 24, 39, 0.62));
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow:
                0 24px 70px rgba(0, 0, 0, 0.24),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
        }

        .menu-card:after {
            content: "";
            position: absolute;
            inset: auto 18px 0 18px;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(56,189,248,0.72), rgba(167,139,250,0.72), transparent);
            opacity: 0.55;
        }

        .menu-icon {
            width: 42px;
            height: 42px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(125, 211, 252, 0.24);
            color: #7dd3fc;
            font-size: 19px;
            margin-bottom: 18px;
        }

        .menu-title {
            color: #ffffff;
            font-size: 20px;
            font-weight: 850;
            letter-spacing: -0.045em;
            margin-bottom: 10px;
        }

        .menu-desc {
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.7;
            min-height: 66px;
        }

        .status {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            padding: 7px 10px;
            border-radius: 999px;
            background: rgba(34, 197, 94, 0.10);
            border: 1px solid rgba(74, 222, 128, 0.18);
            color: #bbf7d0;
            font-size: 12px;
            font-weight: 750;
            margin-top: 14px;
        }

        .status-wip {
            background: rgba(251, 191, 36, 0.10);
            border: 1px solid rgba(251, 191, 36, 0.18);
            color: #fde68a;
        }

        .insight-grid {
            display: grid;
            grid-template-columns: 1.1fr 0.9fr;
            gap: 16px;
            margin-top: 18px;
        }

        .info-card {
            border-radius: 28px;
            padding: 26px;
            background:
                linear-gradient(145deg, rgba(15, 23, 42, 0.78), rgba(2, 6, 23, 0.62));
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow:
                0 26px 80px rgba(0, 0, 0, 0.22),
                inset 0 1px 0 rgba(255,255,255,0.04);
        }

        .info-title {
            color: #f8fafc;
            font-size: 24px;
            font-weight: 900;
            letter-spacing: -0.055em;
            margin-bottom: 10px;
        }

        .info-desc {
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.8;
        }

        .step-list {
            display: grid;
            gap: 12px;
            margin-top: 16px;
        }

        .step {
            display: grid;
            grid-template-columns: 34px 1fr;
            gap: 12px;
            align-items: start;
            padding: 14px;
            border-radius: 18px;
            background: rgba(15, 23, 42, 0.58);
            border: 1px solid rgba(148, 163, 184, 0.12);
        }

        .step-no {
            width: 34px;
            height: 34px;
            border-radius: 13px;
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(125, 211, 252, 0.20);
            color: #7dd3fc;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
        }

        .step-text {
            color: #cbd5e1;
            font-size: 13px;
            line-height: 1.7;
        }

        .cta-card {
            border-radius: 30px;
            padding: 28px;
            background:
                radial-gradient(circle at 0% 0%, rgba(56, 189, 248, 0.18), transparent 36%),
                radial-gradient(circle at 100% 100%, rgba(167, 139, 250, 0.18), transparent 36%),
                linear-gradient(135deg, rgba(15, 23, 42, 0.88), rgba(17, 24, 39, 0.72));
            border: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow: 0 28px 84px rgba(0,0,0,0.24);
            margin-top: 18px;
        }

        .cta-title {
            color: white;
            font-size: 25px;
            font-weight: 900;
            letter-spacing: -0.055em;
            margin-bottom: 8px;
        }

        .cta-desc {
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.8;
        }

        @media (max-width: 1200px) {
            .hero-grid,
            .insight-grid {
                grid-template-columns: 1fr;
            }

            .menu-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 720px) {
            .menu-grid {
                grid-template-columns: 1fr;
            }

            .hero-title {
                font-size: 42px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# SIDEBAR
# =========================

st.sidebar.markdown("## SET50 Dashboard")
st.sidebar.caption("ระบบวิเคราะห์ข้อมูลผู้ถือหุ้น SET50 จาก Neon Database")

st.sidebar.markdown("---")
st.sidebar.markdown("### สถานะระบบ")
st.sidebar.success("Dashboard พร้อมใช้งาน")
st.sidebar.info("เลือกหน้าได้จากเมนูด้านซ้าย")

st.sidebar.markdown("---")
st.sidebar.caption("Data Source: Neon PostgreSQL · Updated by GitHub Actions")


# =========================
# HERO
# =========================

st.markdown(
    """
    <div class="hero-shell">
        <div class="hero-card">
            <div class="hero-grid">
                <div>
                    <div class="eyebrow">SET50 · CAPITAL NETWORK INTELLIGENCE</div>
                    <div class="hero-title">SET50<br/>Dashboard</div>
                    <div class="hero-subtitle">
                        ระบบวิเคราะห์ข้อมูลผู้ถือหุ้น SET50 จาก Neon Database ออกแบบสำหรับสำรวจความสัมพันธ์
                        ระหว่างหุ้น ผู้ถือหุ้นรายใหญ่ กลุ่ม nominee และ node สำคัญในเครือข่ายทุนไทย
                    </div>
                    <div class="pill-row">
                        <div class="pill">Social Network Analysis</div>
                        <div class="pill">Major Shareholders</div>
                        <div class="pill">Interactive 3D Graph</div>
                        <div class="pill">Neon PostgreSQL</div>
                        <div class="pill">GitHub Actions</div>
                    </div>
                </div>
                <div class="hero-panel">
                    <div class="panel-label">Current Module</div>
                    <div class="panel-value">Social Analytics<br/>พร้อมใช้งาน</div>
                    <div class="panel-note">
                        ใช้เมนูด้านซ้ายเพื่อเข้าสู่หน้า SET50 Social Analytics
                        และในอนาคตสามารถเพิ่มหน้าใหม่ในโฟลเดอร์ pages ได้ทันที
                    </div>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# MENU CARDS
# =========================

st.markdown('<div class="section-title">เมนูหลัก</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">เลือกหน้าวิเคราะห์จากเมนูด้านซ้าย หรือใช้การ์ดด้านล่างเป็นแผนผังระบบ</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="menu-grid">
        <div class="menu-card">
            <div class="menu-icon">◎</div>
            <div class="menu-title">SET50 Social Analytics</div>
            <div class="menu-desc">
                วิเคราะห์เครือข่ายความเชื่อมโยงระหว่างหุ้น SET50 และผู้ถือหุ้นใหญ่
                พร้อม PageRank, Degree Centrality และกราฟ 3D หมุนได้
            </div>
            <div class="status">● พร้อมใช้งาน</div>
        </div>

        <div class="menu-card">
            <div class="menu-icon">◈</div>
            <div class="menu-title">Major Holders</div>
            <div class="menu-desc">
                วิเคราะห์ผู้ถือหุ้นรายใหญ่ที่ถือหุ้นหลายตัวใน SET50
                เพื่อค้นหากลุ่มทุนและ nominee ที่ปรากฏซ้ำ
            </div>
            <div class="status status-wip">● Coming soon</div>
        </div>

        <div class="menu-card">
            <div class="menu-icon">⌁</div>
            <div class="menu-title">Stock Comparison</div>
            <div class="menu-desc">
                เปรียบเทียบโครงสร้างผู้ถือหุ้นรายบริษัท
                ดูหุ้นที่มีผู้ถือหุ้นร่วมกันและกลุ่มความสัมพันธ์ที่ซ่อนอยู่
            </div>
            <div class="status status-wip">● Coming soon</div>
        </div>

        <div class="menu-card">
            <div class="menu-icon">▣</div>
            <div class="menu-title">Nominee Intelligence</div>
            <div class="menu-desc">
                เจาะกลุ่ม nominee, custodian, foreign branch และ institutional holders
                เพื่อดูอิทธิพลเชิงโครงข่าย
            </div>
            <div class="status status-wip">● Coming soon</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# INSIGHT SECTION
# =========================

st.markdown('<div class="section-title">ออกแบบมาเพื่อวิเคราะห์อะไร</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="insight-grid">
        <div class="info-card">
            <div class="info-title">จากตารางผู้ถือหุ้น → เครือข่ายทุน</div>
            <div class="info-desc">
                ข้อมูลผู้ถือหุ้นแบบตารางมักอ่านยากเมื่อมีหลายบริษัท แต่เมื่อนำมาสร้างเป็นเครือข่าย
                จะเห็นความสัมพันธ์ที่ซ่อนอยู่ เช่น ผู้ถือหุ้นรายเดียวกันที่ปรากฏในหลายหุ้น,
                หุ้นที่มีผู้ถือหุ้นร่วมกัน และ node ที่เป็นศูนย์กลางของระบบ
            </div>

            <div class="step-list">
                <div class="step">
                    <div class="step-no">1</div>
                    <div class="step-text">
                        GitHub Actions ดึงข้อมูล SET50 และผู้ถือหุ้นใหญ่แบบอัตโนมัติทุกวัน
                    </div>
                </div>
                <div class="step">
                    <div class="step-no">2</div>
                    <div class="step-text">
                        Neon PostgreSQL เก็บข้อมูลล่าสุดในตาราง set50 เพื่อให้ dashboard ดึงมาใช้งาน
                    </div>
                </div>
                <div class="step">
                    <div class="step-no">3</div>
                    <div class="step-text">
                        Streamlit แปลงข้อมูลเป็น Social Network Analysis พร้อมกราฟ interactive
                    </div>
                </div>
            </div>
        </div>

        <div class="info-card">
            <div class="info-title">ตัวชี้วัดที่ใช้</div>
            <div class="info-desc">
                ระบบรองรับการดูทั้งภาพรวมผู้ถือหุ้นและความเป็นศูนย์กลางของ node
                เพื่อช่วยแยกผู้ถือหุ้นที่แค่มีสัดส่วนสูง ออกจากผู้ถือหุ้นที่มีอิทธิพลเชิงเครือข่าย
            </div>

            <div class="step-list">
                <div class="step">
                    <div class="step-no">PR</div>
                    <div class="step-text">
                        PageRank: ใช้ดู node ที่มีอิทธิพลในเครือข่ายจากคุณภาพของความเชื่อมโยง
                    </div>
                </div>
                <div class="step">
                    <div class="step-no">DC</div>
                    <div class="step-text">
                        Degree Centrality: ใช้ดู node ที่เชื่อมโยงกับ node อื่นโดยตรงจำนวนมาก
                    </div>
                </div>
                <div class="step">
                    <div class="step-no">3D</div>
                    <div class="step-text">
                        Interactive 3D Network: ใช้สำรวจ node และ edge ด้วยการหมุน ซูม และ hover
                    </div>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# CTA
# =========================

st.markdown(
    """
    <div class="cta-card">
        <div class="cta-title">เริ่มใช้งาน</div>
        <div class="cta-desc">
            ไปที่เมนูด้านซ้าย แล้วเลือก <b>SET50 Social Analytics</b>
            เพื่อเข้าสู่หน้าวิเคราะห์เครือข่ายผู้ถือหุ้นแบบเต็มรูปแบบ
            หากต้องการเพิ่มหน้าใหม่ในอนาคต ให้สร้างไฟล์เพิ่มในโฟลเดอร์ <b>pages/</b>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
