import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="IQROGUEREX Analytics",
    layout="wide",
    page_icon="📊"
)

# ---------------- PREMIUM UI STYLE ----------------
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #0E1117 0%, #111827 100%);
    color: #E5E7EB;
}

/* Glass Card */
.card {
    background: rgba(255, 255, 255, 0.04);
    border-radius: 16px;
    padding: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* KPI Metric */
[data-testid="stMetricValue"] {
    font-size: 2rem;
    font-weight: 600;
    color: #22d3ee;
}

/* Titles */
h1, h2, h3 {
    font-weight: 600;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
    color: white;
    border-radius: 10px;
    border: none;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0B0F19;
}

/* Table */
.stDataFrame {
    background: rgba(255,255,255,0.02);
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
GITHUB_URL = "https://raw.githubusercontent.com/iqroguerex-cpu/iqroguerex-cpu/main/sales_data.csv"

@st.cache_data
def load_data():
    try:
        response = requests.get(GITHUB_URL)
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
        else:
            df = pd.read_csv("sales_data.csv")

        df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
        df = df.dropna(subset=["Order_Date"])

        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce").fillna(0)

        df["Total_Sales"] = df["Quantity"] * df["Price"]

        return df

    except:
        return pd.DataFrame()

df = load_data()

# ---------------- HEADER ----------------
st.title("📊 IQROGUEREX Sales Intelligence")
st.caption("Real-time performance analytics dashboard")
st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔎 Filters")

if not df.empty:
    min_date = df["Order_Date"].min().date()
    max_date = df["Order_Date"].max().date()

    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date)
    )

    region = st.sidebar.multiselect(
        "Region",
        df["Region"].unique(),
        default=df["Region"].unique()
    )

    category = st.sidebar.multiselect(
        "Category",
        df["Category"].unique(),
        default=df["Category"].unique()
    )

    # FILTER
    if isinstance(date_range, tuple):
        start, end = date_range
        f_df = df[
            (df["Order_Date"] >= pd.Timestamp(start)) &
            (df["Order_Date"] <= pd.Timestamp(end)) &
            (df["Region"].isin(region)) &
            (df["Category"].isin(category))
        ]
    else:
        f_df = df

else:
    f_df = pd.DataFrame()

# ---------------- KPI SECTION ----------------
if not f_df.empty:

    col1, col2, col3, col4 = st.columns(4)

    revenue = f_df["Total_Sales"].sum()
    orders = f_df["Order_ID"].nunique()
    customers = f_df["Customer_Name"].nunique()
    aov = revenue / orders if orders else 0

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("💰 Revenue", f"${revenue:,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("📦 Orders", orders)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("👥 Customers", customers)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("📊 AOV", f"${aov:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("## 📈 Performance Overview")

    left, right = st.columns([7, 3])

    # -------- LINE CHART --------
    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        trend = f_df.groupby(
            f_df["Order_Date"].dt.to_period("M")
        )["Total_Sales"].sum().reset_index()

        trend["Order_Date"] = trend["Order_Date"].astype(str)

        fig = px.line(
            trend,
            x="Order_Date",
            y="Total_Sales",
            template="plotly_dark",
            markers=True
        )

        fig.update_layout(
            margin=dict(l=10, r=10, t=30, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # -------- PIE CHART --------
    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        fig2 = px.pie(
            f_df,
            values="Total_Sales",
            names="Category",
            hole=0.5,
            template="plotly_dark"
        )

        fig2.update_layout(
            margin=dict(l=10, r=10, t=30, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # -------- TOP CUSTOMERS --------
    st.markdown("## 🏆 Top Customers")

    top = (
        f_df.groupby("Customer_Name")["Total_Sales"]
        .sum()
        .nlargest(5)
        .reset_index()
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(top, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # -------- DOWNLOAD --------
    csv = f_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Report",
        csv,
        "IQROGUEREX_Report.csv",
        "text/csv"
    )

# ---------------- EMPTY STATE ----------------
else:
    st.markdown("""
    <div style="text-align:center; padding:80px;">
        <h2>📭 No Data Available</h2>
        <p style="color:gray;">Try adjusting your filters or check your data source.</p>
    </div>
    """, unsafe_allow_html=True)
