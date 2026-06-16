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
    layout="wide"
)

st.title("SET50 Social Analytics")
st.caption("วิเคราะห์เครือข่ายความเชื่อมโยงระหว่างหุ้น SET50 และผู้ถือหุ้นใหญ่")


# =========================
# CUSTOM CSS
# =========================

st.markdown(
    """
    <style>
        .main {
            background: radial-gradient(circle at top left, #1f2937 0%, #111827 35%, #020617 100%);
        }

        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.045);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 18px;
            border-radius: 18px;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
        }

        h1, h2, h3 {
            letter-spacing: -0.03em;
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


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 30}
)


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

    return df


df = load_data()

if df.empty:
    st.warning("ยังไม่มีข้อมูลใน table set50")
    st.stop()


# =========================
# SIDEBAR FILTERS
# =========================

st.sidebar.header("ตัวกรอง")

symbols = sorted(df["symbol"].dropna().unique().tolist())

selected_symbols = st.sidebar.multiselect(
    "เลือกหุ้น",
    symbols,
    default=symbols[:10]
)

min_percent = st.sidebar.slider(
    "ขั้นต่ำ % หุ้น",
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

col1, col2, col3, col4 = st.columns(4)

col1.metric("จำนวนหุ้น", filtered["symbol"].nunique())
col2.metric("จำนวนผู้ถือหุ้น", filtered["shareholder_name"].nunique())
col3.metric("จำนวนความเชื่อมโยง", len(filtered))
col4.metric("ค่า % หุ้นรวม", f"{filtered['percent_num'].sum():,.2f}")


# =========================
# HOLDER SUMMARY
# =========================

st.subheader("อันดับผู้ถือหุ้นที่เชื่อมโยงกับ SET50 มากที่สุด")

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

st.dataframe(
    holder_summary,
    use_container_width=True,
    hide_index=True
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


# =========================
# CENTRALITY
# =========================

st.subheader("Network Centrality")

if G.number_of_nodes() == 0:
    st.warning("ไม่มีข้อมูลพอสำหรับสร้างกราฟ")
    st.stop()

degree_centrality = nx.degree_centrality(G)

try:
    pagerank = nx.pagerank(G, weight="weight")
except Exception:
    pagerank = {node: 0 for node in G.nodes()}

centrality_df = pd.DataFrame({
    "node": list(G.nodes()),
    "node_type": [G.nodes[n].get("node_type", "") for n in G.nodes()],
    "degree": [G.degree(n) for n in G.nodes()],
    "degree_centrality": [degree_centrality.get(n, 0) for n in G.nodes()],
    "pagerank": [pagerank.get(n, 0) for n in G.nodes()],
})

centrality_df = centrality_df.sort_values("pagerank", ascending=False)

st.dataframe(
    centrality_df,
    use_container_width=True,
    hide_index=True
)


# =========================
# 3D NETWORK GRAPH
# =========================

st.subheader("Network Graph 3D")
st.caption("ลากเพื่อหมุน | Scroll เพื่อซูม | Hover เพื่อดูรายละเอียด")

pos = nx.spring_layout(
    G,
    dim=3,
    k=0.9,
    iterations=120,
    seed=42,
    weight="weight"
)


# ---------- EDGES ----------

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


# ---------- NODES ----------

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
        node_color.append("#ff4b4b")
    else:
        node_color.append("#38bdf8")

    if show_labels:
        node_label.append(label[:22])
    else:
        node_label.append("")

    node_text.append(
        f"<b>{label}</b><br>"
        f"ประเภท: {node_type}<br>"
        f"Degree: {deg}<br>"
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
        opacity=0.92,
        line=dict(
            width=1.2,
            color="rgba(255,255,255,0.9)"
        )
    ),
    textfont=dict(
        size=11,
        color="white"
    ),
    showlegend=False
)


# ---------- FIGURE ----------

fig = go.Figure(
    data=edge_traces + [node_trace]
)

fig.update_layout(
    height=850,
    showlegend=False,
    hovermode="closest",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, b=0, t=40),
    scene=dict(
        bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            visible=False,
            showbackground=False,
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        yaxis=dict(
            visible=False,
            showbackground=False,
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        zaxis=dict(
            visible=False,
            showbackground=False,
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        camera=dict(
            eye=dict(x=1.55, y=1.65, z=1.25)
        )
    ),
    title=dict(
        text="Interactive 3D Network",
        x=0.02,
        y=0.98,
        font=dict(
            size=22,
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


# =========================
# RAW DATA
# =========================

with st.expander("ดูข้อมูลดิบ"):
    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )
