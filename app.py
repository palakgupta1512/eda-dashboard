import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="CSV EDA Dashboard", layout="wide")

st.title("📊 CSV Auto EDA Dashboard")
st.write("Koi bhi CSV upload karo — main automatically analyse kar dunga!")

# ---- FILE UPLOAD ----
uploaded_file = st.file_uploader("📁 CSV file upload karo", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.success("✅ File successfully load ho gayi!")
    
    # ---- BASIC INFO ----
    st.subheader("📌 Dataset Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())
    
    st.dataframe(df.head(10))  # pehli 10 rows dikhao
    
    # ---- DATATYPES ----
    st.subheader("🔢 Column Datatypes")
    st.dataframe(df.dtypes.rename("DataType").reset_index().rename(columns={"index": "Column"}))
    
    # ---- MISSING VALUES ----
    st.subheader("❓ Missing Values per Column")
    missing = df.isnull().sum().reset_index()
    missing.columns = ["Column", "Missing Count"]
    missing["Missing %"] = (missing["Missing Count"] / len(df) * 100).round(2)
    st.dataframe(missing)
    
    # ---- STATISTICS ----
    st.subheader("📈 Descriptive Statistics")
    st.dataframe(df.describe())
    
    # ---- CHARTS ----
    st.subheader("📊 Column-wise Analysis")
    
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()
    
    # Categorical column ka bar chart
    if categorical_cols:
        selected_cat = st.selectbox("Categorical column choose karo (Bar Chart):", categorical_cols)
        fig1, ax1 = plt.subplots()
        df[selected_cat].value_counts().plot(kind='bar', ax=ax1, color='steelblue', edgecolor='black')
        ax1.set_title(f'{selected_cat} Distribution')
        ax1.set_xlabel(selected_cat)
        ax1.set_ylabel('Count')
        st.pyplot(fig1)
    
    # Numeric column ka histogram
    if numeric_cols:
        selected_num = st.selectbox("Numeric column choose karo (Histogram):", numeric_cols)
        fig2, ax2 = plt.subplots()
        df[selected_num].dropna().hist(ax=ax2, bins=15, color='coral', edgecolor='black')
        ax2.set_title(f'{selected_num} Distribution')
        st.pyplot(fig2)
    
    # Correlation Heatmap
    if len(numeric_cols) >= 2:
        st.subheader("🔥 Correlation Heatmap")
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax3)
        st.pyplot(fig3)

else:
    st.info("👆 Upar CSV upload karo, analysis shuru ho jaayega!")
    
