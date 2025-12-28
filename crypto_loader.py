import requests
import snowflake.connector
from datetime import datetime

# --- CONFIGURATION (EDIT THIS!) ---
SNOWFLAKE_CONFIG = {
    "user": "DARSHANA",        # e.g. "DARSHANA"
    "password": "REPLACE_WITH_YOUR_PASSWORD",    # Your login password
    "account": "REPLACE_WITH_YOUR_ACCOUNT",   # e.g. "xy12345.us-east-1"
    "warehouse": "COMPUTE_WH",
    "database": "CRYPTO_DB",
    "schema": "PUBLIC"
}

# --- 1. FETCH DATA (Extract) ---
def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_market_cap=true"
    try:
        print("🌍 Fetching Bitcoin price from API...")
        response = requests.get(url)
        data = response.json()
        price = data['bitcoin']['usd']
        cap = data['bitcoin']['usd_market_cap']
        return price, cap
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None, None

# --- 2. LOAD DATA (Load) ---
def upload_to_snowflake(price, cap):
    print("❄️ Connecting to Snowflake...")
    try:
        conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
        cur = conn.cursor()
        
        # SQL Injection safe query
        sql = """
        INSERT INTO BITCOIN_PRICES (SYMBOL, PRICE_USD, MARKET_CAP, TIMESTAMP)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP())
        """
        
        cur.execute(sql, ('BTC', price, cap))
        print(f"✅ Success! Inserted BTC Price: ${price}")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Snowflake Error: {e}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    btc_price, btc_cap = get_crypto_data()
    if btc_price:
        upload_to_snowflake(btc_price, btc_cap)