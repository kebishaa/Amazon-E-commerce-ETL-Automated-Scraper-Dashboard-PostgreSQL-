import os
import pandas as pd

# Use a folder inside your project instead of /opt/airflow
os.makedirs("./data/raw", exist_ok=True)

# Path to save CSV
csv_file = "./data/raw/scraped.csv"

# Example scraped data
df = pd.DataFrame({
    "product": ["Item1", "Item2"],
    "price": [10, 20]
})

df.to_csv(csv_file, index=False)
print(f"CSV saved at {csv_file}")
