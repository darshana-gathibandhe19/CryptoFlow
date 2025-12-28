# ❄️ CryptoFlow: Automated Cloud ELT Pipeline

## 🚀 Overview
CryptoFlow is an end-to-end **ELT (Extract, Load, Transform)** pipeline that ingests real-time cryptocurrency financial data and stores it in a Cloud Data Warehouse.

The system orchestrates data workflows using **Apache Airflow** running in **Docker**, extracts live market data via Python APIs, and loads it securely into **Snowflake** for historical analysis.

## 🏗️ Architecture
**Flow:** `CoinGecko API` → `Python Script (Docker)` → `Airflow Orchestrator` → `Snowflake DB`

* **Extraction:** Python fetches live BTC/USD price and Market Cap from the CoinGecko REST API.
* **Orchestration:** Apache Airflow schedules the job to run hourly.
* **Loading:** The `snowflake-connector` pushes data into the `BITCOIN_PRICES` table in Snowflake.
* **Environment:** Fully containerized using Docker to ensure reproducibility across Windows/Linux.

## 🛠️ Tech Stack
* **Cloud Warehouse:** Snowflake
* **Orchestration:** Apache Airflow (2.7.1)
* **Containerization:** Docker & Docker Compose
* **Language:** Python 3.10
* **Libraries:** `snowflake-connector-python`, `requests`, `pandas`

## 📂 Project Structure
```text
CryptoFlow/
├── dags/
│   └── bitcoin_dag.py      # Airflow DAG definition
├── crypto_loader.py        # Standalone Python script for local testing
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

⚙️ Setup & Installation
1. Prerequisites
Docker Desktop installed and running.

A Snowflake Account (Trial or Standard).

2. Snowflake Setup
Run the following SQL in your Snowflake worksheet to prepare the database:

SQL

CREATE DATABASE CRYPTO_DB;
CREATE TABLE BITCOIN_PRICES (
    SYMBOL VARCHAR(10),
    PRICE_USD FLOAT,
    MARKET_CAP FLOAT,
    TIMESTAMP TIMESTAMP_NTZ
);

3. Running the Pipeline (Docker)
This project uses the Airflow Standalone container.

Windows PowerShell:

PowerShell

docker run -d -p 8080:8080 -v "${PWD}/dags":/opt/airflow/dags --name airflow-crypto apache/airflow:2.7.1-python3.10 standalone
Install Dependencies inside Docker:

Bash

docker exec -u 0 -it airflow-crypto bash
python -m pip install snowflake-connector-python requests pandas
4. Access the Dashboard
Go to: http://localhost:8080

Login using the credentials found in the Docker logs.

Trigger the crypto_pipeline_v1 DAG.

📸 Screenshots
c:\Users\Dell\OneDrive\Pictures\Screenshots\airflow_success.jpg c:\Users\Dell\OneDrive\Pictures\Screenshots\snowflake_data.jpg

🚧 Challenges Overfaced
Docker Permissions: Solved root-user installation blocks by using python -m pip to bypass wrapper script restrictions.

Environment Conflicts: Managed Python versioning (3.14 vs 3.10) using Docker containers to ensure library compatibility.