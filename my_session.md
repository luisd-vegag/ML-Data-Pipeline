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

```
mkdir -p dags

touch dags/stock_market_data_processing.py

nano dags/stock_market_data_processing.py
```
```
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from src.etl.download_data import download_data
from src.etl.preprocess_data import preprocess_data
from src.etl.feature_engineering import feature_engineering
from src.etl.train_model import train_model

default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 30),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'stock_market_data_processing',
    default_args=default_args,
    description='DAG for processing stock market data',
    schedule_interval=timedelta(days=1)
)

download_data_task = PythonOperator(
    task_id='download_data',
    python_callable=download_data,
    dag=dag
)

preprocess_data_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag
)

feature_engineering_task = PythonOperator(
    task_id='feature_engineering',
    python_callable=feature_engineering,
    dag=dag
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)

download_data_task >> preprocess_data_task >> feature_engineering_task >> train_model_task
```

# Implement unit tests for relevant logic under src/tests, covering data preprocessing and feature engineering functions.
```
mkdir -p src/tests

touch src/tests/test_preprocess_data.py

nano src/tests/test_preprocess_data.py
```
```
import unittest
from preprocess_data import preprocess_data

class TestPreprocessData(unittest.TestCase):
    def test_preprocess_data(self):
        input_path = 'data/raw/Data/Stocks'
        output_path = 'data/processed/stocks.parquet'
        preprocess_data(input_path, output_path)

        # TODO: Add assertions to verify the correctness of the processed data
```
### Save the file ('Ctrl+X', then 'Y', then press Enter)

```
touch src/tests/test_feature_engineering.py

nano src/tests/test_feature_engineering.py
```
```
import unittest
from feature_engineering import feature_engineering

class TestFeatureEngineering(unittest.TestCase):
    def test_feature_engineering(self):
        input_path = 'data/processed/stocks.parquet'
        output_path = 'data/processed/stocks_fe.parquet'
        feature_engineering(input_path, output_path)

        # TODO: Add assertions to verify the correctness of the feature engineered data

```
### Save the file ('Ctrl+X', then 'Y', then press Enter)

# Create a FastAPI server under src/api that will load the trained model and serve predictions through the /predict endpoint.
```
mkdir -p src/api

touch src/api/app.py

nano src/api/app.py
```
```
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

class StockMarketData(BaseModel):
    vol_moving_avg: float
    adj_close_rolling_med: float

@app.post('/predict')
def predict(data: StockMarketData):
    # Load the trained model
    model = joblib.load('path/to/trained/model.pkl')

    # Create a Pandas DataFrame from the input data
    input_data = pd.DataFrame([{
        'vol_moving_avg': data.vol_moving_avg,
        'adj_close_rolling_med': data.adj_close_rolling_med
    }])

    # Make predictions using the trained model
    predictions = model.predict(input_data)

    # Return the predicted value
    return int(predictions[0])
```

# Write a Dockerfile under the docker directory to containerize the ETL pipeline with necessary dependencies and build/execution configurations.
```
mkdir -p docker

touch docker/Dockerfile

nano docker/Dockerfile
```
```
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for Airflow home
ENV AIRFLOW_HOME /app

# Expose the Airflow webserver and scheduler ports
EXPOSE 8080 5555

# Start the Airflow webserver and scheduler
CMD ["airflow", "webserver", "--port", "8080"] 
CMD ["airflow", "scheduler"]
```

# Test the ETL pipeline locally, ensure it works as expected, and store a log file from the pipeline execution.
```
pip freeze >> requirements.txt

pip install -r requirements.txt
```
```
export AIRFLOW_HOME=$(pwd)

cp dags/stock_market_data_processing.py $AIRFLOW_HOME/dags/
```
```
airflow db init

airflow users create --username admin --firstname luis --lastname vega --role Admin --email luisd.vegag@gmail.com
```

## To store a log file from the pipeline execution, you can redirect the Airflow logs to a file by adding the following configuration to the airflow.cfg file:
```
[core]
...
dag_default_view = tree
logging_level = INFO
logging_config_class = log_config.LOGGING_CONFIG
```
## Then, create a log_config.py file under the src/etl directory with the following content:
``` 
touch src/etl/log_config.py

nano src/etl/log_config.py
``` 
```
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
```
```
airflow webserver -D
airflow scheduler -D
```
## Use next t stop servers
```
airflow webserver -D stop
airflow scheduler -D stop
```
## Open http://localhost:8080
