# Set up a Python virtual environment and install necessary libraries, such as Airflow, pandas, scikit-learn, FastAPI, and others.
```
python3 -m venv env

source env/bin/activate

pip install pandas scikit-learn fastapi uvicorn apache-airflow

pip freeze
----------------------------
# Download the stock market dataset and store it under the data/raw directory.
mkdir -p data/raw

kaggle datasets download jacksoncrow/stock-market-dataset -p data/raw
```
## Go to Kaggle.com, login, settings, API, Create New Token 
```
mkdir ~/.kaggle/

mv kaggle.json ~/.kaggle/

sudo chmod 600 ~/.kaggle/kaggle.json

sudo pip install kaggle

kaggle datasets list

unzip data/raw/stock-market-dataset.zip -d data/raw
```
----------------------------------------
# Implement ETL scripts under src/etl to perform data processing, feature engineering, and ML training tasks.
```
mkdir -p src/etl

touch src/etl/download_data.py

nano src/etl/download_data.py 
```
## Create Python file named 'download_data.py' under 'src/etl' directory to download the stock market dataset from the Kaggle website
```
import os
import urllib.request

def download_data(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    urllib.request.urlretrieve(url, path)

if __name__ == '__main__':
    url = 'https://www.kaggle.com/jacksoncrow/stock-market-dataset/download'
    path = 'data/raw/stock-market-dataset.zip'
    download_data(url, path)
```
### Save the file ('Ctrl+X', then 'Y', then press Enter)

## Create Python file named preprocess_data.py under src/etl directory to preprocess the raw data and store it in a structured format.
```
mkdir -p src/etl

touch src/etl/preprocess_data.py

nano src/etl/preprocess_data.py 
```
```
import os
import pandas as pd

def preprocess_data(input_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.read_csv(input_path)
    # Rename columns
    df = df.rename(columns={'tic': 'Symbol', 'datadate': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'adjcp': 'Adj Close', 'volume': 'Volume', 'name': 'Security Name'})
    # Convert date column to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    # Save the preprocessed data to a structured format
    df.to_parquet(output_path)

if __name__ == '__main__':
    input_path = 'data/raw/Data/Stocks'
    output_path = 'data/processed/stocks.parquet'
    preprocess_data(input_path, output_path)
```
### Save the file ('Ctrl+X', then 'Y', then press Enter)

## Create Python file named feature_engineering.py under src/etl directory to perform feature engineering on the preprocessed data. 
```
mkdir -p src/etl

touch src/etl/feature_engineering.py

nano src/etl/feature_engineering.py 
```
```
import os
import pandas as pd

def feature_engineering(input_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.read_parquet(input_path)
    # Calculate the rolling average of the trading volume for each stock and ETF
    df['vol_moving_avg'] = df.groupby('Symbol')['Volume'].rolling(window=30, min_periods=1).mean().reset_index(0, drop=True)
    # Calculate the rolling median of the adjusted closing price for each stock and ETF
    df['adj_close_rolling_med'] = df.groupby('Symbol')['Adj Close'].rolling(window=30, min_periods=1).median().reset_index(0, drop=True)
    # Save the feature engineered data to the same structured format
    df.to_parquet(output_path)

if __name__ == '__main__':
    input_path = 'data/processed/
```
### Save the file ('Ctrl+X', then 'Y', then press Enter)

# Create Airflow DAG (main_dag.py) in the dags directory that will orchestrate the ETL process by calling the respective Python scripts from src/etl.

```
mkdir -p dags

touch dags/main_dag.py

nano dags/main_dag.py
```
```
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 30),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'main_dag',
    default_args=default_args,
    description='ETL pipeline for stock market dataset',
    schedule_interval=timedelta(days=1),
)

download_data_task = PythonOperator(
    task_id='download_data',
    python_callable=download_data,
    op_kwargs={
        'url': 'https://www.kaggle.com/jacksoncrow/stock-market-dataset/download',
        'path': 'data/raw/stock-market-dataset.zip'
    },
    dag=dag
)

preprocess_data_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    op_kwargs={
        'input_path': 'data/raw/Data/Stocks',
        'output_path': 'data/processed/stocks.parquet'
    },
    dag=dag
)

feature_engineering_task = PythonOperator(
    task_id='feature_engineering',
    python_callable=feature_engineering,
    op_kwargs={
        'input_path': 'data/processed/stocks.parquet',
        'output_path': 'data/processed/stocks_fe.parquet'
    },
    dag=dag
)

download_data_task >> preprocess_data_task >> feature_engineering_task
```
### Save the file ('Ctrl+X', then 'Y', then press Enter)