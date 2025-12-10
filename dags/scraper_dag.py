# dags/scraper_dag.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import sys
sys.path.append("/opt/airflow/scraper")  # Add scraper folder to path
from scraper import scrape
import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection string
POSTGRES_CONN = "postgresql+psycopg2://postgres:postgres@postgres:5432/amazon_db"

def load_to_postgres():
    # Read CSV
    df = pd.read_csv("./data/raw/scraped.csv")
    
    # Connect to Postgres
    engine = create_engine(POSTGRES_CONN)
    
    # Load into table 'products' (create if not exists)
    df.to_sql("products", engine, if_exists="replace", index=False)
    print("Data loaded into PostgreSQL")

# DAG definition
default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 12, 4),
}

with DAG(
    dag_id="scraper_to_postgres",
    default_args=default_args,
    schedule_interval="@daily",  # run once a day
    catchup=False,
) as dag:

    task_scrape = PythonOperator(
        task_id="scrape_data",
        python_callable=scrape
    )

    task_load = PythonOperator(
        task_id="load_data",
        python_callable=load_to_postgres
    )

    task_scrape >> task_load  # scrape first, then load
