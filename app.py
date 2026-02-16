import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: white;
    }
    .stMetric {
        background-color: #1E222A;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Sales Performance Dashboard")

uploaded_file = st.file_uploader("Upload Sales CSV File", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Total_Sales"] = df["Quantity"] * df["Price"]

    min_date = df["Order_Date"].min()
    max_date = df["Order_Date"].max()

    st.sidebar.header("Filters")

    date_range = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    region_filter = st.sidebar.multiselect(
        "Select Region",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )

    category_filter = st.sidebar.multiselect(
        "Select Category",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    filtered_df = df[
        (df["Order_Date"] >= pd.to_datetime(date_range[0])) &
        (df["Order_Date"] <= pd.to_datetime(date_range[1])) &
        (df["Region"].isin(region_filter)) &
        (df["Category"].isin(category_filter))
    ]

    total_revenue = filtered_df["Total_Sales"].sum()
    total_orders = filtered_df["Order_ID"].nunique()
    total_customers = filtered_df["Customer_Name"].nunique()

    previous_period = df[
        (df["Order_Date"] < pd.to_datetime(date_range[0])) &
        (df["Region"].isin(region_filter)) &
        (df["Category"].isin(category_filter))
    ]

    previous_revenue = previous_period["Total_Sales"].sum()

    revenue_change = total_revenue - previous_revenue

    st.subheader("Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"${total_revenue:,.0f}", f"{revenue_change:,.0f}")
    col2.metric("Total Orders", total_orders)
    col3.metric("Total Customers", total_customers)

    col4, col5 = st.columns(2)

    with col4:
        st.subheader("Revenue by Region")
        region_revenue = filtered_df.groupby("Region")["Total_Sales"].sum()
        fig1, ax1 = plt.subplots()
        region_revenue.plot(kind="bar", ax=ax1)
        ax1.set_ylabel("Revenue")
        st.pyplot(fig1)

    with col5:
        st.subheader("Revenue Distribution by Category")
        category_revenue = filtered_df.groupby("Category")["Total_Sales"].sum()
        fig2, ax2 = plt.subplots()
        category_revenue.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
        ax2.set_ylabel("")
        st.pyplot(fig2)

    st.subheader("Monthly Revenue Trend")
    filtered_df["Month"] = filtered_df["Order_Date"].dt.to_period("M")
    monthly_revenue = filtered_df.groupby("Month")["Total_Sales"].sum()

    fig3, ax3 = plt.subplots()
    monthly_revenue.plot(kind="line", marker="o", ax=ax3)
    ax3.set_ylabel("Revenue")
    st.pyplot(fig3)

    st.subheader("Top 5 Customers")
    top_customers = filtered_df.groupby("Customer_Name")["Total_Sales"].sum() \
                                .sort_values(ascending=False).head(5)
    st.dataframe(top_customers)

    st.subheader("Download Filtered Report")

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download CSV Report",
        data=csv,
        file_name="filtered_sales_report.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload a CSV file to view the dashboard.")
