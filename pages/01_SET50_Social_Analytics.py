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
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Noto Sans Thai', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 8% 8%, rgba(56, 189, 248, 0.18) 0%, transparent 32%),
                radial-gradient(circle at 90% 12%, rgba(168, 85, 247, 0.16) 0%, transparent 34%),
                radial-gradient(circle at 50% 95%, rgba(34, 197, 94, 0.10) 0%, transparent 35%),
                linear-gradient(135deg, #020617 0%, #0f172a 48%, #020617 100%);
            color: #e5e7eb;
        }

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(15, 23, 42, 0.96), rgba(2, 6, 23, 0.96));
            border-right: 1px solid rgba(148, 163, 184, 0.18);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .hero-card {
            padding: 30px 32px;
            border-radius: 28px;
            background:
                linear-gradient(135deg, rgba(15, 23, 42, 0.88), rgba(30, 41, 59, 0.55)),
                radial-gradient(circle at top right, rgba(56, 189, 248, 0.22), transparent 35%);
            border: 1px solid rgba(148, 163, 184, 0.20);
            box-shadow: 0 24px 70px rgba(0, 0, 0, 0.32);
            margin-bottom: 22px;
        }

        .hero-title {
            font-size: 48px;
            font-weight: 800;
            letter-spacing: -0.06em;
            margin-bottom: 6px;
            line-height: 1.06;
            background: linear-gradient(90deg, #ffffff, #bae6fd, #c4b5fd);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            color: #cbd5e1;
            font-size: 16px;
            line-height: 1.7;
            max-width: 980px;
        }

        .pill-row {
            margin-top: 18px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .pill {
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(125, 211, 252, 0.20);
            color: #dbeafe;
            font-size: 13px;
        }

        div[data-testid="stMetric"] {
            background:
                linear-gradient(135deg, rgba(15, 23, 42, 0.82), rgba(30, 41, 59, 0.58));
            border: 1px solid rgba(148, 163, 184, 0.18);
            padding: 18px 18px;
            border-radius: 22px;
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.22);
        }

        div[data-testid="stMetric"] label {
            color: #cbd5e1 !important;
            font-weight: 600;
        }

        div[data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-weight: 800;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow: 0 16px 42px rgba(0, 0, 0, 0.18);
        }

        .section-card {
            padding: 22px;
            border-radius: 24px;
            background: rgba(15, 23, 42, 0.54);
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: 0 20px 54px rgba(0, 0, 0, 0.18);
            margin-top: 18px;
            margin-bottom: 18px;
        }

        h1, h2, h3 {
            letter-spacing: -0.04em;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 999px;
            padding: 10px 18px;
            background: rgba(15, 23, 42, 0.64);
            border: 1px solid rgba(148, 163, 184, 0.14);
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(14, 165, 233, 0.30), rgba(168, 85, 247, 0.24));
            border: 1px solid rgba(125, 211, 252, 0.35);
        }

        .small-note {
            color: #94a3b8;
            font-size: 13px;
            margin-top: -6px;
            margin-bottom: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# HERO
# =========================

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">SET50 Social Analytics</div>
        <div class="hero-subtitle">
            Dashboard วิเคราะห์เครือข่ายผู้ถือหุ้น SET50 จาก Neon Database
            เพื่อดูความเชื่อมโยงระหว่างหุ้น ผู้ถือหุ้นรายใหญ่ กลุ่ม nominee และ node ที่มีอิทธิพลในเครือข่ายทุน
        </div>
        <div class="pill-row">
            <div class="pill">Interactive 3D Network</div>
            <div class="pill">PageRank</div>
            <div class="pill">Degree Centrality</div>
            <div class="pill">Major Shareholders</div>
            <div class="pill">Neon PostgreSQL</div>
        </div>
    </div>
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

st.sidebar.header("ตัวกรองข้อมูล")

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
    value=150,
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
# KPI
# =========================

latest_update = filtered["created_at"].dropna().max()
latest_update_text = "-"
if pd.notna(latest_update):
    latest_update_text = latest_update.strftime("%Y-%m-%d %H:%M")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("จำนวนหุ้น", f"{filtered['symbol'].nunique():,}")
col2.metric("จำนวนผู้ถือหุ้น", f"{filtered['shareholder_name'].nunique():,}")
col3.metric("จำนวนความเชื่อมโยง", f"{len(filtered):,}")
col4.metric("สัดส่วนถือหุ้นรวม", f"{filtered['percent_num'].sum():,.2f}%")
col5.metric("อัปเดตล่าสุด", latest_update_text)


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
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("อันดับผู้ถือหุ้นที่เชื่อมโยงกับ SET50 มากที่สุด")
    st.markdown(
        '<div class="small-note">เรียงตามจำนวนหุ้น SET50 ที่ถือร่วม และสัดส่วนถือหุ้นรวม</div>',
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
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Network Centrality")
    st.markdown(
        '<div class="small-note">ค่า PageRank และ Degree Centrality ใช้ช่วยดู node ที่มีอิทธิพลในเครือข่าย</div>',
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
    st.markdown('</div>', unsafe_allow_html=True)


with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Interactive 3D Network")
    st.markdown(
        '<div class="small-note">ลากเพื่อหมุน | Scroll เพื่อซูม | Hover เพื่อดูรายละเอียด | หุ้น = แดง | ผู้ถือหุ้น = ฟ้า</div>',
        unsafe_allow_html=True
    )

    pos = nx.spring_layout(
        G,
        dim=3,
        k=0.9,
        iterations=120,
        seed=42,
        weight="weight"
    )

    edge_traces = []

    for u, v, attr in G.edges(data=True):
        x0, y0, z0 = pos[u]
        x1, y1, z1 = pos[v]

        weight = float(attr.get("weight", 1))
        edge_width = min(max(weight / 4, 1), 7)

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
                    color="rgba(96, 165, 250, 0.35)"
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

        node_size.append(8 + deg * node_size_scale)

        if node_type == "stock":
            node_color.append("#fb7185")
        else:
            node_color.append("#38bdf8")

        if show_labels:
            node_label.append(label[:22])
        else:
            node_label.append("")

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
            opacity=0.94,
            line=dict(
                width=1.4,
                color="rgba(255,255,255,0.9)"
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
        height=860,
        showlegend=False,
        hovermode="closest",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, b=0, t=42),
        scene=dict(
            bgcolor="rgba(0,0,0,0)",
            xaxis=dict(visible=False, showbackground=False, showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(visible=False, showbackground=False, showgrid=False, showticklabels=False, zeroline=False),
            zaxis=dict(visible=False, showbackground=False, showgrid=False, showticklabels=False, zeroline=False),
            camera=dict(
                eye=dict(x=1.55, y=1.65, z=1.25)
            )
        ),
        title=dict(
            text="Interactive 3D Network",
            x=0.02,
            y=0.98,
            font=dict(
                size=24,
                color="white"
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

    st.markdown('</div>', unsafe_allow_html=True)


with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("ข้อมูลดิบจาก Neon")
    st.markdown(
        '<div class="small-note">ข้อมูลที่ผ่านตัวกรองปัจจุบัน ใช้ตรวจสอบรายละเอียดรายหุ้นและแหล่งข้อมูล</div>',
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
    st.markdown('</div>', unsafe_allow_html=True)
