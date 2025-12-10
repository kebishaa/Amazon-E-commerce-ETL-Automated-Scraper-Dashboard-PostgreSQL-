# Amazon E-commerce ETL
End-to-end scraper + ETL + dashboard. Scrapes Amazon search results
(educational/demo use), stores records in PostgreSQL, and exposes a Streamlit
dashboard.

## Steps to run locally
1. Copy `.env.example` to `.env` and fill values.
2. Create Postgres DB and run `database/create_tables.sql` (or run `python
database/db_loader.py`).
3. Install requirements: `pip install -r requirements.txt`.
4. Run scraper manually: `python scraper/scraper.py` (this writes to `data/raw/
scraped.csv`).
5. Load into Postgres: `python database/db_loader.py`.
6. Run dashboard: `streamlit run dashboard/app.py`.
