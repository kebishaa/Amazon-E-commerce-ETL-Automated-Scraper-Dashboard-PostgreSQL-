import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

# ---------------------------
# Database connection
# ---------------------------
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

engine = create_engine(
    f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
)

st.set_page_config(page_title="Amazon ETL Dashboard", layout="wide")

st.title("📊 Amazon Product Dashboard")
st.write("This dashboard displays the latest Amazon scraped data (product + price).")

# ---------------------------
# Load data
# ---------------------------
def load_data():
    try:
        df = pd.read_sql("SELECT * FROM products;", engine)
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None

df = load_data()

if df is None or df.empty:
    st.warning("No data found in the database. Run the scraper DAG first.")
else:
    # Show table
    st.subheader("📦 Product List")
    st.dataframe(df, use_container_width=True)

    # Convert price string to numeric if needed
    if df["price"].dtype == object:
        df["price"] = df["price"].replace('[\$,]', '', regex=True).astype(float)

    # Summary
    st.subheader("📈 Summary Statistics")
    st.write(df["price"].describe())

    # Price chart
    st.subheader("💰 Price Distribution")
    st.bar_chart(df["price"])

    # Top 10 expensive items
    st.subheader("🏆 Top 10 Most Expensive Products")
    st.write(df.sort_values("price", ascending=False).head(10))
