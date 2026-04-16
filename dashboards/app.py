import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Analytics Dashboard", layout="wide")

# ------------------ UI ------------------
st.markdown("""
<div style="display:flex; align-items:center; gap:10px;">
    <span style="font-size:30px;">📊</span>
    <h2 style="margin:0;">Analytics Dashboard</h2>
</div>
""", unsafe_allow_html=True)

# ------------------ LOGIN ------------------
def login():
    st.title("🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "1234":
            st.session_state["login"] = True
        else:
            st.error("Wrong credentials")

if "login" not in st.session_state:
    st.session_state["login"] = False

if not st.session_state["login"]:
    login()
    st.stop()

# ------------------ LOAD DATA ------------------
import os
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(__file__)

    file_path = os.path.join(BASE_DIR, "..", "data", "SampleSuperstore.csv")
    file_path = os.path.abspath(file_path)

    df = pd.read_csv(file_path)

    # clean columns
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    return df

# ------------------ SMART DETECTION ------------------
def detect_columns(df):
    cols = df.columns

    sales = next((c for c in cols if "sales" in c), None)
    profit = next((c for c in cols if "profit" in c), None)
    date = next((c for c in cols if "date" in c), None)
    category = next((c for c in cols if "category" in c), None)
    region = next((c for c in cols if "region" in c), None)

    return sales, profit, date, category, region

sales_col, profit_col, date_col, category_col, region_col = detect_columns(df)

# ------------------ HEADER ------------------
st.markdown("## 📊 Dashboard")
st.markdown("---")

# ------------------ SIDEBAR ------------------
st.sidebar.title("📌 Menu")

page = st.sidebar.radio("Navigate", [
    "🏠 Overview",
    "📊 Sales Dashboard",
    "📈 Profit Dashboard",
    "🎛 Custom Dashboard",
    "📂 Data Explorer"
])

# ------------------ FILTERS ------------------
st.sidebar.markdown("### 🔍 Filters")

filtered_df = df.copy()

for col in df.select_dtypes(include="object").columns:
    vals = df[col].dropna().unique()
    if len(vals) < 50:
        selected = st.sidebar.multiselect(col, vals, default=vals)
        filtered_df = filtered_df[filtered_df[col].isin(selected)]

# ------------------ KPI ------------------
def show_kpis(data):
    num_cols = data.select_dtypes(include="number").columns

    if len(num_cols) >= 3:
        c1, c2, c3 = st.columns(3)
        c1.metric(num_cols[0], f"{data[num_cols[0]].sum():,.0f}")
        c2.metric(num_cols[1], f"{data[num_cols[1]].sum():,.0f}")
        c3.metric(num_cols[2], f"{data[num_cols[2]].sum():,.0f}")

# ------------------ OVERVIEW ------------------
if page == "🏠 Overview":
    show_kpis(filtered_df)

    if date_col and sales_col:
        fig = px.line(filtered_df, x=date_col, y=sales_col,
                      title="Sales Trend", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

# ------------------ SALES ------------------
elif page == "📊 Sales Dashboard":

    if category_col and sales_col:
        fig = px.bar(filtered_df, x=category_col, y=sales_col,
                     color=category_col, title="Sales by Category",
                     template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    if region_col and sales_col:
        fig = px.pie(filtered_df, names=region_col, values=sales_col,
                     title="Sales by Region",
                     template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

# ------------------ PROFIT ------------------
elif page == "📈 Profit Dashboard":

    if sales_col and profit_col:
        fig = px.scatter(filtered_df, x=sales_col, y=profit_col,
                         color=category_col,
                         title="Profit vs Sales",
                         template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    if category_col and profit_col:
        fig = px.box(filtered_df, x=category_col, y=profit_col,
                     title="Profit Distribution",
                     template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

# ------------------ CUSTOM DASHBOARD ------------------
elif page == "🎛 Custom Dashboard":

    st.subheader("Build Your Own Chart")

    cols = df.columns.tolist()

    chart_type = st.selectbox("Select Chart Type",
                             ["Bar", "Line", "Scatter", "Pie"])

    x = st.selectbox("X-axis", cols)
    y = st.selectbox("Y-axis", cols)

    if chart_type == "Bar":
        fig = px.bar(filtered_df, x=x, y=y, template="plotly_dark")
    elif chart_type == "Line":
        fig = px.line(filtered_df, x=x, y=y, template="plotly_dark")
    elif chart_type == "Scatter":
        fig = px.scatter(filtered_df, x=x, y=y, template="plotly_dark")
    elif chart_type == "Pie":
        fig = px.pie(filtered_df, names=x, values=y)

    st.plotly_chart(fig, use_container_width=True)

# ------------------ DATA ------------------
elif page == "📂 Data Explorer":

    st.write("### Columns")
    st.write(df.columns)

    st.write("### Head")
    st.dataframe(df.head())

    st.write("### Full Data")
    st.dataframe(filtered_df)

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("""
<div class="footer">
✨ Built by <b>Disha Sharma</b> | Streamlit Dashboard 🚀
</div>
""", unsafe_allow_html=True)