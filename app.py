import streamlit as st


st.set_page_config(
    page_title="SET50 Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================
# CSS
# =========================

st.html(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;500;600;700;800;900&display=swap');

        * {
            font-family: 'Noto Sans Thai', sans-serif !important;
        }

        .stApp {
            background:
                radial-gradient(circle at 14% 8%, rgba(56, 189, 248, 0.20) 0%, transparent 28%),
                radial-gradient(circle at 86% 12%, rgba(168, 85, 247, 0.18) 0%, transparent 30%),
                radial-gradient(circle at 50% 100%, rgba(14, 165, 233, 0.10) 0%, transparent 34%),
                linear-gradient(135deg, #020617 0%, #07111f 46%, #020617 100%);
            color: #f8fafc;
        }

        .block-container {
            max-width: 1500px;
            padding-top: 1.4rem;
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

        section[data-testid="stSidebar"] * {
            color: #e5e7eb;
        }

        .page {
            width: 100%;
        }

        .hero-shell {
            border-radius: 34px;
            padding: 1px;
            background:
                linear-gradient(135deg, rgba(56, 189, 248, 0.48), rgba(168, 85, 247, 0.32), rgba(15, 23, 42, 0.06));
            box-shadow:
                0 36px 100px rgba(0, 0, 0, 0.35),
                inset 0 1px 0 rgba(255, 255, 255, 0.06);
            margin-bottom: 28px;
        }

        .hero-card {
            position: relative;
            overflow: hidden;
            border-radius: 33px;
            padding: 44px;
            background:
                radial-gradient(circle at 100% 0%, rgba(56, 189, 248, 0.24) 0%, transparent 34%),
                radial-gradient(circle at 0% 100%, rgba(168, 85, 247, 0.20) 0%, transparent 36%),
                linear-gradient(135deg, rgba(15, 23, 42, 0.94), rgba(17, 24, 39, 0.82));
            border: 1px solid rgba(255, 255, 255, 0.08);
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
            grid-template-columns: minmax(0, 1.55fr) minmax(330px, 0.75fr);
            gap: 34px;
            align-items: center;
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            padding: 8px 14px;
            border-radius: 999px;
            background: rgba(56, 189, 248, 0.11);
            border: 1px solid rgba(125, 211, 252, 0.28);
            color: #bae6fd;
            font-size: 12px;
            font-weight: 900;
            letter-spacing: 0.09em;
            text-transform: uppercase;
            margin-bottom: 18px;
        }

        .hero-title {
            font-size: clamp(46px, 5.4vw, 82px);
            font-weight: 900;
            letter-spacing: -0.08em;
            line-height: 0.96;
            margin-bottom: 20px;
            background: linear-gradient(90deg, #ffffff 0%, #bae6fd 34%, #c4b5fd 72%, #ffffff 100%);
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
            margin-top: 24px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .pill {
            padding: 10px 15px;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.76);
            border: 1px solid rgba(125, 211, 252, 0.22);
            color: #dbeafe;
            font-size: 13px;
            font-weight: 750;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
        }

        .hero-panel {
            border-radius: 30px;
            padding: 26px;
            background:
                radial-gradient(circle at 100% 0%, rgba(56, 189, 248, 0.12), transparent 40%),
                linear-gradient(135deg, rgba(2, 6, 23, 0.66), rgba(15, 23, 42, 0.82));
            border: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.06),
                0 24px 64px rgba(0,0,0,0.22);
        }

        .panel-label {
            color: #94a3b8;
            font-size: 13px;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .panel-value {
            color: #ffffff;
            font-size: 31px;
            font-weight: 900;
            letter-spacing: -0.055em;
            line-height: 1.16;
            margin-bottom: 15px;
        }

        .panel-note {
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.8;
        }

        .section-title {
            color: #f8fafc;
            font-size: 31px;
            font-weight: 900;
            letter-spacing: -0.06em;
            margin: 30px 0 6px 0;
        }

        .section-subtitle {
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.75;
            margin-bottom: 20px;
        }

        .menu-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 18px;
            margin-top: 18px;
            margin-bottom: 30px;
        }

        .menu-card {
            position: relative;
            overflow: hidden;
            min-height: 255px;
            border-radius: 30px;
            padding: 26px;
            background:
                radial-gradient(circle at 100% 0%, rgba(56, 189, 248, 0.15) 0%, transparent 42%),
                linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(17, 24, 39, 0.68));
            border: 1px solid rgba(148, 163, 184, 0.17);
            box-shadow:
                0 24px 70px rgba(0, 0, 0, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
            transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
        }

        .menu-card:hover {
            transform: translateY(-6px);
            border-color: rgba(125, 211, 252, 0.38);
            box-shadow: 0 32px 94px rgba(14, 165, 233, 0.17);
        }

        .menu-card::after {
            content: "";
            position: absolute;
            inset: auto 18px 0 18px;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(56,189,248,0.80), rgba(168,85,247,0.80), transparent);
            opacity: 0.75;
        }

        .menu-icon {
            width: 46px;
            height: 46px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(56, 189, 248, 0.13);
            border: 1px solid rgba(125, 211, 252, 0.26);
            color: #7dd3fc;
            font-size: 21px;
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
            line-height: 1.78;
            min-height: 92px;
        }

        .status {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            padding: 7px 12px;
            border-radius: 999px;
            background: rgba(34, 197, 94, 0.10);
            border: 1px solid rgba(74, 222, 128, 0.22);
            color: #bbf7d0;
            font-size: 12px;
            font-weight: 850;
            margin-top: 18px;
        }

        .status-wip {
            background: rgba(251, 191, 36, 0.10);
            border: 1px solid rgba(251, 191, 36, 0.22);
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
            padding: 30px;
            background:
                radial-gradient(circle at 100% 0%, rgba(56, 189, 248, 0.08), transparent 38%),
                linear-gradient(145deg, rgba(15, 23, 42, 0.84), rgba(2, 6, 23, 0.66));
            border: 1px solid rgba(148, 163, 184, 0.17);
            box-shadow:
                0 28px 84px rgba(0, 0, 0, 0.25),
                inset 0 1px 0 rgba(255,255,255,0.04);
        }

        .info-title {
            color: #f8fafc;
            font-size: 26px;
            font-weight: 900;
            letter-spacing: -0.055em;
            margin-bottom: 11px;
        }

        .info-desc {
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.88;
        }

        .step-list {
            display: grid;
            gap: 13px;
            margin-top: 20px;
        }

        .step {
            display: grid;
            grid-template-columns: 40px 1fr;
            gap: 13px;
            align-items: start;
            padding: 15px;
            border-radius: 20px;
            background: rgba(15, 23, 42, 0.62);
            border: 1px solid rgba(148, 163, 184, 0.13);
        }

        .step-no {
            width: 40px;
            height: 40px;
            border-radius: 15px;
            background: rgba(56, 189, 248, 0.13);
            border: 1px solid rgba(125, 211, 252, 0.22);
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
            line-height: 1.78;
        }

        .cta-card {
            border-radius: 32px;
            padding: 31px;
            background:
                radial-gradient(circle at 0% 0%, rgba(56, 189, 248, 0.20), transparent 36%),
                radial-gradient(circle at 100% 100%, rgba(168, 85, 247, 0.20), transparent 36%),
                linear-gradient(135deg, rgba(15, 23, 42, 0.92), rgba(17, 24, 39, 0.76));
            border: 1px solid rgba(148, 163, 184, 0.19);
            box-shadow: 0 30px 90px rgba(0,0,0,0.28);
            margin-top: 24px;
        }

        .cta-title {
            color: white;
            font-size: 28px;
            font-weight: 900;
            letter-spacing: -0.055em;
            margin-bottom: 8px;
        }

        .cta-desc {
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.88;
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
    """
)


# =========================
# SIDEBAR
# =========================

st.sidebar.title("SET50 Dashboard")
st.sidebar.caption("ระบบวิเคราะห์ข้อมูลผู้ถือหุ้น SET50 จาก Neon Database")

st.sidebar.divider()
st.sidebar.subheader("สถานะระบบ")
st.sidebar.success("Dashboard พร้อมใช้งาน")
st.sidebar.info("เลือกหน้าได้จากเมนูด้านซ้าย")

st.sidebar.divider()
st.sidebar.caption("Data Source: Neon PostgreSQL")
st.sidebar.caption("Automation: GitHub Actions")
st.sidebar.caption("Frontend: Streamlit Cloud")


# =========================
# MAIN CONTENT
# =========================

st.html(
    """
    <div class="page">

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

    </div>
    """
)
