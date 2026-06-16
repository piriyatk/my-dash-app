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
# CSS
# =========================

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;500;600;700;800;900&display=swap');

        * {
            font-family: 'Noto Sans Thai', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 12% 8%, rgba(56, 189, 248, 0.22) 0%, transparent 28%),
                radial-gradient(circle at 85% 10%, rgba(168, 85, 247, 0.20) 0%, transparent 30%),
                radial-gradient(circle at 80% 85%, rgba(34, 211, 238, 0.10) 0%, transparent 28%),
                linear-gradient(135deg, #020617 0%, #07111f 45%, #020617 100%);
            color: #f8fafc;
        }

        .block-container {
            max-width: 1500px;
            padding-top: 1.2rem;
            padding-bottom: 4rem;
        }

        header[data-testid="stHeader"] {
            background: rgba(2, 6, 23, 0.55);
            backdrop-filter: blur(18px);
            border-bottom: 1px solid rgba(148, 163, 184, 0.10);
        }

        section[data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 20% 0%, rgba(56, 189, 248, 0.16) 0%, transparent 30%),
                linear-gradient(180deg, rgba(15, 23, 42, 0.98), rgba(2, 6, 23, 0.98));
            border-right: 1px solid rgba(148, 163, 184, 0.18);
        }

        .hero-shell {
            border-radius: 34px;
            padding: 1px;
            background:
                linear-gradient(135deg, rgba(56, 189, 248, 0.42), rgba(168, 85, 247, 0.30), rgba(15, 23, 42, 0.06));
            box-shadow:
                0 32px 100px rgba(0, 0, 0, 0.35),
                inset 0 1px 0 rgba(255, 255, 255, 0.06);
            margin-bottom: 26px;
        }

        .hero-card {
            position: relative;
            overflow: hidden;
            border-radius: 33px;
            padding: 42px;
            background:
                radial-gradient(circle at 100% 0%, rgba(56, 189, 248, 0.23) 0%, transparent 34%),
                radial-gradient(circle at 0% 100%, rgba(168, 85, 247, 0.20) 0%, transparent 36%),
                linear-gradient(135deg, rgba(15, 23, 42, 0.92), rgba(17, 24, 39, 0.80));
            border: 1px solid rgba(255, 255, 255, 0.06);
        }

        .hero-card::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent);
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
            grid-template-columns: minmax(0, 1.45fr) minmax(320px, 0.75fr);
            gap: 34px;
            align-items: center;
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            padding: 7px 13px;
            border-radius: 999px;
            background: rgba(56, 189, 248, 0.10);
            border: 1px solid rgba(125, 211, 252, 0.24);
            color: #bae6fd;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.09em;
            text-transform: uppercase;
            margin-bottom: 16px;
        }

        .hero-title {
            font-size: clamp(44px, 5.4vw, 78px);
            font-weight: 900;
            letter-spacing: -0.078em;
            line-height: 0.96;
            margin-bottom: 18px;
            background: linear-gradient(90deg, #ffffff 0%, #bae6fd 36%, #c4b5fd 76%, #ffffff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            color: #cbd5e1;
            font-size: 17px;
            line-height: 1.9;
            max-width: 980px;
        }

        .pill-row {
            margin-top: 22px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .pill {
            padding: 9px 14px;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(125, 211, 252, 0.20);
            color: #dbeafe;
            font-size: 13px;
            font-weight: 700;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
        }

        .hero-panel {
            border-radius: 28px;
            padding: 25px;
            background:
                linear-gradient(135deg, rgba(2, 6, 23, 0.60), rgba(15, 23, 42, 0.78));
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.05),
                0 22px 60px rgba(0,0,0,0.20);
        }

        .panel-label {
            color: #94a3b8;
            font-size: 13px;
            font-weight: 750;
            margin-bottom: 8px;
        }

        .panel-value {
            color: #ffffff;
            font-size: 30px;
            font-weight: 900;
            letter-spacing: -0.05em;
            line-height: 1.15;
            margin-bottom: 14px;
        }

        .panel-note {
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.75;
        }

        .section-title {
            color: #f8fafc;
            font-size: 30px;
            font-weight: 900;
            letter-spacing: -0.06em;
            margin: 28px 0 6px 0;
        }

        .section-subtitle {
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.75;
            margin-bottom: 18px;
        }

        .menu-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 18px;
            margin-top: 18px;
            margin-bottom: 26px;
        }

        .menu-card {
            position: relative;
            overflow: hidden;
            min-height: 245px;
            border-radius: 30px;
            padding: 25px;
            background:
                radial-gradient(circle at 100% 0%, rgba(56, 189, 248, 0.14) 0%, transparent 42%),
                linear-gradient(145deg, rgba(15, 23, 42, 0.86), rgba(17, 24, 39, 0.66));
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow:
                0 24px 70px rgba(0, 0, 0, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
            transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
        }

        .menu-card:hover {
            transform: translateY(-5px);
            border-color: rgba(125, 211, 252, 0.35);
            box-shadow: 0 30px 90px rgba(14, 165, 233, 0.16);
        }

        .menu-card::after {
            content: "";
            position: absolute;
            inset: auto 18px 0 18px;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(56,189,248,0.78), rgba(168,85,247,0.78), transparent);
            opacity: 0.70;
        }

        .menu-icon {
            width: 44px;
            height: 44px;
            border-radius: 17px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(125, 211, 252, 0.24);
            color: #7dd3fc;
            font-size: 20px;
            font-weight: 900;
            margin-bottom: 18px;
        }

        .menu-title {
            color: #ffffff;
            font-size: 21px;
            font-weight: 900;
            letter-spacing: -0.05em;
            margin-bottom: 10px;
        }

        .menu-desc {
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.75;
            min-height: 86px;
        }

        .status {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            padding: 7px 11px;
            border-radius: 999px;
            background: rgba(34, 197, 94, 0.10);
            border: 1px solid rgba(74, 222, 128, 0.20);
            color: #bbf7d0;
            font-size: 12px;
            font-weight: 800;
            margin-top: 16px;
        }

        .status-wip {
            background: rgba(251, 191, 36, 0.10);
            border: 1px solid rgba(251, 191, 36, 0.20);
            color: #fde68a;
        }

        .insight-grid {
            display: grid;
            grid-template-columns: 1.1fr 0.9fr;
            gap: 18px;
            margin-top: 20px;
        }

        .info-card {
            border-radius: 30px;
            padding: 28px;
            background:
                linear-gradient(145deg, rgba(15, 23, 42, 0.82), rgba(2, 6, 23, 0.64));
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow:
                0 26px 80px rgba(0, 0, 0, 0.24),
                inset 0 1px 0 rgba(255,255,255,0.04);
        }

        .info-title {
            color: #f8fafc;
            font-size: 25px;
            font-weight: 900;
            letter-spacing: -0.055em;
            margin-bottom: 10px;
        }

        .info-desc {
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.85;
        }

        .step-list {
            display: grid;
            gap: 13px;
            margin-top: 18px;
        }

        .step {
            display: grid;
            grid-template-columns: 38px 1fr;
            gap: 13px;
            align-items: start;
            padding: 15px;
            border-radius: 20px;
            background: rgba(15, 23, 42, 0.60);
            border: 1px solid rgba(148, 163, 184, 0.12);
        }

        .step-no {
            width: 38px;
            height: 38px;
            border-radius: 15px;
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(125, 211, 252, 0.20);
            color: #7dd3fc;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            font-size: 13px;
        }

        .step-text {
            color: #cbd5e1;
            font-size: 13px;
            line-height: 1.75;
        }

        .cta-card {
            border-radius: 32px;
            padding: 30px;
            background:
                radial-gradient(circle at 0% 0%, rgba(56, 189, 248, 0.20), transparent 36%),
                radial-gradient(circle at 100% 100%, rgba(168, 85, 247, 0.20), transparent 36%),
                linear-gradient(135deg, rgba(15, 23, 42, 0.90), rgba(17, 24, 39, 0.74));
            border: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow: 0 28px 84px rgba(0,0,0,0.26);
            margin-top: 22px;
        }

        .cta-title {
            color: white;
            font-size: 27px;
            font-weight: 900;
            letter-spacing: -0.055em;
            margin-bottom: 8px;
        }

        .cta-desc {
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.85;
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
st.sidebar.caption("Data Source: Neon PostgreSQL")
st.sidebar.caption("Automation: GitHub Actions")
st.sidebar.caption("Frontend: Streamlit Cloud")


# =========================
# MAIN HTML
# =========================

st.markdown(
    """
    <div class="hero-shell">
        <div class="hero-card">
            <div class="hero-grid">
                <div>
                    <div class="eyebrow">SET50 · CAPITAL NETWORK INTELLIGENCE</div>
                    <div class="hero-title">SET50<br>Dashboard</div>
                    <div class="hero-subtitle">
                        ระบบวิเคราะห์ข้อมูลผู้ถือหุ้น SET50 จาก Neon Database สำหรับสำรวจความสัมพันธ์
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
                    <div class="panel-value">Social Analytics<br>พร้อมใช้งาน</div>
                    <div class="panel-note">
                        ใช้เมนูด้านซ้ายเพื่อเข้าสู่หน้า SET50 Social Analytics
                        และในอนาคตสามารถเพิ่มหน้าใหม่ในโฟลเดอร์ pages ได้ทันที
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="section-title">เมนูหลัก</div>
    <div class="section-subtitle">
        เลือกหน้าวิเคราะห์จากเมนูด้านซ้าย หรือใช้การ์ดด้านล่างเป็นแผนผังระบบ
    </div>

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

    <div class="section-title">ออกแบบมาเพื่อวิเคราะห์อะไร</div>
    <div class="section-subtitle">
        เปลี่ยนข้อมูลผู้ถือหุ้นแบบตาราง ให้กลายเป็นภาพเครือข่ายที่อ่านความสัมพันธ์ได้เร็วขึ้น
    </div>

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
