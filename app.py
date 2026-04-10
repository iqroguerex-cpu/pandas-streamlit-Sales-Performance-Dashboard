import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration & Theming
st.set_page_config(
    page_title="IQROGUEREX Sales Insights",
    layout="wide",
    page_icon="📊"
)

# Dark Theme Styling
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #00d4ff; }
    .main { background-color: #0E1117; }
    div.stButton > button:first-child { background-color: #00d4ff; color:white; border:none; }
    .stTable { background-color: #1E222A; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# 2. Data Source
DATA_URL = "https://raw.githubusercontent.com/iqroguerex-cpu/iqroguerex-cpu/main/sales_data.csv"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(DATA_URL)

        # Ensure required columns exist
        required_cols = ["Order_Date", "Quantity", "Price", "Order_ID", "Customer_Name", "Region", "Category"]
        for col in required_cols:
            if col not in df.columns:
                st.error(f"Missing column: {col}")
                return None

        # Data cleaning
        df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
        df = df.dropna(subset=["Order_Date"])

        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce").fillna(0)

        df["Total_Sales"] = df["Quantity"] * df["Price"]

        return df

    except Exception as e:
        st.error("🚨 Data Connection Failed")
        st.exception(e)
        return None

df = load_data()

if df is not None and not df.empty:

    # --- SIDEBAR ---
    st.sidebar.header("📊 Filter Analytics")

    min_date = df["Order_Date"].min().date()
    max_date = df["Order_Date"].max().date()

    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    region = st.sidebar.multiselect(
        "Region",
        options=df["Region"].dropna().unique(),
        default=df["Region"].dropna().unique()
    )

    category = st.sidebar.multiselect(
        "Category",
        options=df["Category"].dropna().unique(),
        default=df["Category"].dropna().unique()
    )

    # --- FILTER LOGIC ---
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range

        mask = (
            (df["Order_Date"] >= pd.Timestamp(start_date)) &
            (df["Order_Date"] <= pd.Timestamp(end_date)) &
            (df["Region"].isin(region)) &
            (df["Category"].isin(category))
        )
        f_df = df.loc[mask]
    else:
        f_df = df.copy()

    # --- MAIN CONTENT ---
    st.title("📊 Sales Performance Analytics")
    st.caption("Powered by IQROGUEREX Data Engine")
    st.divider()

    # KPI Metrics
    m1, m2, m3, m4 = st.columns(4)

    rev = f_df["Total_Sales"].sum()
    orders = f_df["Order_ID"].nunique()
    cust = f_df["Customer_Name"].nunique()
    aov = rev / orders if orders > 0 else 0

    m1.metric("Gross Revenue", f"${rev:,.0f}")
    m2.metric("Orders", f"{orders:,}")
    m3.metric("Customers", f"{cust:,}")
    m4.metric("Avg. Order Value", f"${aov:,.2f}")

    # --- CHARTS ---
    col_left, col_right = st.columns([7, 3])

    with col_left:
        st.subheader("Revenue Trend")

        trend = (
            f_df.groupby(f_df['Order_Date'].dt.to_period('M'))['Total_Sales']
            .sum()
            .reset_index()
        )

        trend['Order_Date'] = trend['Order_Date'].astype(str)

        fig_line = px.line(
            trend,
            x='Order_Date',
            y='Total_Sales',
            template="plotly_dark",
            markers=True
        )

        fig_line.update_traces(line_color='#00d4ff')
        st.plotly_chart(fig_line, use_container_width=True)

    with col_right:
        st.subheader("Category Split")

        if not f_df.empty:
            fig_pie = px.pie(
                f_df,
                values='Total_Sales',
                names='Category',
                hole=0.4,
                template="plotly_dark"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("No data available for selected filters.")

    # --- TOP CUSTOMERS ---
    st.subheader("🏆 Top Performing Customers")

    if not f_df.empty:
        top_df = (
            f_df.groupby("Customer_Name")["Total_Sales"]
            .sum()
            .nlargest(5)
            .reset_index()
        )

        st.dataframe(top_df.style.format({"Total_Sales": "${:,.2f}"}))
    else:
        st.warning("No data to display.")

    # --- EXPORT ---
    csv = f_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Filtered CSV",
        data=csv,
        file_name="IQ_Sales_Report.csv",
        mime="text/csv"
    )

else:
    st.warning("No data loaded. Please check your data source.")
