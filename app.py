import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration & Theming
st.set_page_config(page_title="IQROGUEREX Sales Insights", layout="wide", page_icon="📊")

# Professional Dark Theme CSS
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #00d4ff; }
    .main { background-color: #0E1117; }
    div.stButton > button:first-child { background-color: #00d4ff; color:white; border:none; }
    .stTable { background-color: #1E222A; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# 2. Data Connection (Updated with exact Raw URL structure)
DATA_URL = "https://raw.githubusercontent.com/iqroguerex-cpu/iqroguerex-cpu/main/sales_data.csv"

@st.cache_data
def load_data():
    try:
        # storage_options helps bypass some security blocks on raw requests
        data = pd.read_csv(DATA_URL)
        data["Order_Date"] = pd.to_datetime(data["Order_Date"])
        data["Total_Sales"] = data["Quantity"] * data["Price"]
        return data
    except Exception as e:
        # If the file isn't found, we show a clear error
        st.error("🚨 **Data Connection Failed**")
        st.info(f"Please ensure your repository is **Public** and the file name is **sales_data.csv**.")
        return None

df = load_data()

if df is not None:
    # --- SIDEBAR ---
    st.sidebar.header("📊 Filter Analytics")
    
    min_date, max_date = df["Order_Date"].min(), df["Order_Date"].max()
    
    date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
    
    region = st.sidebar.multiselect("Region", options=df["Region"].unique(), default=df["Region"].unique())
    category = st.sidebar.multiselect("Category", options=df["Category"].unique(), default=df["Category"].unique())

    # Ensure range is fully selected
    if isinstance(date_range, list) or isinstance(date_range, tuple):
        if len(date_range) == 2:
            mask = (df["Order_Date"] >= pd.Timestamp(date_range[0])) & \
                   (df["Order_Date"] <= pd.Timestamp(date_range[1])) & \
                   (df["Region"].isin(region)) & \
                   (df["Category"].isin(category))
            f_df = df.loc[mask]
        else:
            f_df = df
    else:
        f_df = df

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

    # Visuals
    col_left, col_right = st.columns([7, 3])

    with col_left:
        st.subheader("Revenue Trend")
        trend = f_df.groupby(f_df['Order_Date'].dt.to_period('M'))['Total_Sales'].sum().reset_index()
        trend['Order_Date'] = trend['Order_Date'].astype(str)
        fig_line = px.line(trend, x='Order_Date', y='Total_Sales', template="plotly_dark", markers=True)
        fig_line.update_traces(line_color='#00d4ff')
        st.plotly_chart(fig_line, use_container_width=True)

    with col_right:
        st.subheader("Category Split")
        fig_pie = px.pie(f_df, values='Total_Sales', names='Category', hole=0.4, template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    # Bottom Row
    st.subheader("🏆 Top performing Customers")
    top_df = f_df.groupby("Customer_Name")["Total_Sales"].sum().nlargest(5).reset_index()
    st.table(top_df.style.format({"Total_Sales": "${:,.2f}"}))

    # Export
    csv = f_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Filtered CSV", data=csv, file_name="IQ_Sales_Report.csv")
