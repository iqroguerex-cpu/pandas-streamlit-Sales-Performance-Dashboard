# 📊 IQROGUEREX Sales Intelligence Dashboard

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data-blue?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-blue?logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20App-brightgreen?logo=rocket)](https://your-streamlit-app-link.streamlit.app)

</p>

---

## 🚀 Overview

A **premium sales analytics dashboard** built with Streamlit that delivers real-time business insights using data directly loaded from GitHub.

Designed with a modern **glassmorphism UI**, this dashboard provides a clean and interactive experience for analyzing revenue, customer behavior, and sales performance.

---

## ✨ Features

* 🌐 Automatic data loading from GitHub
* 🎛️ Dynamic filters:

  * Date range
  * Region
  * Category
* 📊 KPI metrics:

  * Revenue
  * Orders
  * Customers
  * Average Order Value (AOV)
* 📈 Monthly revenue trend (interactive)
* 🧾 Category distribution (donut chart)
* 🏆 Top customers analysis
* 📥 Download filtered report
* 🎨 Premium UI (glassmorphism + dark theme)

---

## 🛠️ Tech Stack

* Python 3.x
* Streamlit
* Pandas
* Plotly
* Requests

---

## 📂 Project Structure

```bash
.
├── app.py
├── sales_data.csv (optional fallback)
├── requirements.txt
├── README.md
```

---

## ⚙️ Setup

### 1. Add dataset to GitHub

Upload your dataset to your repository.

### 2. Get raw file URL

Example:

```bash
https://raw.githubusercontent.com/username/repo/main/sales_data.csv
```

### 3. Update in code

```python
GITHUB_URL = "your-raw-github-url"
```

---

## ▶️ Run Locally

```bash
streamlit run app.py
```

---

## 📊 Key Insights

* 💰 Total revenue generated
* 📦 Number of orders
* 👥 Unique customers
* 📊 Average order value
* 📈 Revenue trends over time
* 🏆 Top performing customers

---

## 📈 Visualizations

* 📈 Monthly revenue trend (line chart)
* 🧾 Category distribution (donut chart)
* 📊 KPI cards

---

## 🧠 Data Processing

* Loads data from GitHub API
* Cleans and converts columns
* Calculates total sales dynamically
* Applies real-time filtering

---

## 📁 Dataset Requirements

Your dataset should include:

* Order_ID
* Order_Date
* Region
* Category
* Customer_Name
* Quantity
* Price

---

## 🚀 Deployment

Deploy easily using **Streamlit Cloud**:

1. Push project to GitHub
2. Go to https://streamlit.io/cloud
3. Create new app
4. Select repository
5. Deploy 🎉

---

## 🔮 Future Improvements

* 📊 Real-time data streaming
* 📉 Forecasting models
* 🧠 Customer segmentation
* 📊 Multi-dashboard navigation
* 🔔 Alerts & anomaly detection

---

## 👨‍💻 Author

**Chinmay V Chatradamath**
---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
