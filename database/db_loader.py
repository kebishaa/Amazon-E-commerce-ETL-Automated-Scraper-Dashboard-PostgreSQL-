import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(dotenv_path="/opt/airflow/database/.env")

# Get database credentials
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

# Connect to PostgreSQL
engine = create_engine(
    f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
)

# -------------------- INSERT INTO DATABASE --------------------

def load_to_postgres():
    """Load the scraped CSV file into PostgreSQL."""

    csv_path = "/opt/airflow/scraper/output/amazon_products.csv"

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found at {csv_path}")

    # Load CSV into DataFrame
    df = pd.read_csv(csv_path)

    # Add timestamp if not in CSV
    if "scraped_at" not in df.columns:
        df["scraped_at"] = pd.Timestamp.utcnow()

    # Write to PostgreSQL
    df.to_sql(
        "amazon_products",        # <-- TABLE NAME
        engine,
        if_exists="append",       # append new daily data
        index=False
    )

    print("Data loaded successfully into PostgreSQL.")
