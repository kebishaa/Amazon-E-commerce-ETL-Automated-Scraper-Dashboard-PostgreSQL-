from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Import your scraper and loader
from scraper.scraper import scrape_amazon_data
from database.db_loader import load_to_postgres

# Python functions that Airflow will run
def run_scraper():
    scrape_amazon_data()

def run_loader():
    load_to_postgres()

default_args = {
    "owner": "kibatu",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
}

with DAG(
    dag_id="amazon_scraper_etl",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",          # ← AUTOMATED SCHEDULING HERE
    catchup=False,
    max_active_runs=1,
) as dag:

    scrape_task = PythonOperator(
        task_id="scrape_amazon",
        python_callable=run_scraper
    )

    load_task = PythonOperator(
        task_id="load_to_postgres",
        python_callable=run_loader
    )

    scrape_task >> load_task
