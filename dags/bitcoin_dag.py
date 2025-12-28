from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import snowflake.connector

# --- CONFIG (Paste your details here again) ---
SNOWFLAKE_CONFIG = {
    "user": "DARSHANA",
    "password": "REPLACE_WITH_YOUR_PASSWORD",
    "account": "REPLACE_WITH_YOUR_ACCOUNT",
    "warehouse": "COMPUTE_WH",
    "database": "CRYPTO_DB",
    "schema": "PUBLIC"
}

# --- TASK 1: Extract & Load (Combined for simplicity) ---
def extract_and_load_bitcoin():
    # 1. Extract
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_market_cap=true"
    print("🌍 Fetching data from API...")
    data = requests.get(url).json()
    price = data['bitcoin']['usd']
    cap = data['bitcoin']['usd_market_cap']
    
    # 2. Load
    print(f"❄️ Connecting to Snowflake to load Price: {price}")
    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    cur = conn.cursor()
    sql = """
    INSERT INTO BITCOIN_PRICES (SYMBOL, PRICE_USD, MARKET_CAP, TIMESTAMP)
    VALUES (%s, %s, %s, CURRENT_TIMESTAMP())
    """
    cur.execute(sql, ('BTC', price, cap))
    cur.close()
    conn.close()
    print("✅ Load Complete.")

# --- DAG DEFINITION ---
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='crypto_pipeline_v1',
    default_args=default_args,
    description='Fetch Bitcoin price every hour',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@hourly', # Run once an hour
    catchup=False,
) as dag:

    # The Task
    run_etl = PythonOperator(
        task_id='fetch_bitcoin_price',
        python_callable=extract_and_load_bitcoin
    )

    run_etl