from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from stock_market_data_processing import (
    download_data,
    preprocess_data,
    feature_engineering,
    train_model,
)

default_args = {
    "owner": "data_engineer",
    "depends_on_past": False,
    "start_date": datetime(2023, 4, 30),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    "main_dag",
    default_args=default_args,
    description="ETL pipeline for stock market dataset",
    schedule_interval=timedelta(days=1),
)

download_data_task = PythonOperator(
    task_id="download_data",
    python_callable=download_data,
    op_kwargs={
        "user": "jacksoncrow",
        "dataset": "stock-market-dataset",
        "path": "data/raw/",
    },
    dag=dag,
)

preprocess_data_task = PythonOperator(
    task_id="preprocess_data",
    python_callable=preprocess_data,
    op_kwargs={
        "input_path": "data/raw/stocks",
        "output_path": "data/processed/stocks_{}.parquet",
    },
    dag=dag,
)

feature_engineering_task = PythonOperator(
    task_id="feature_engineering",
    python_callable=feature_engineering,
    op_kwargs={
        "input_path": "data/processed",
        "output_path": "data/processed_fe",
    },
    dag=dag,
)

# Define the train model task
train_model_task = PythonOperator(
    task_id="train_model",
    python_callable=train_model,
    op_kwargs={
        "input_path": "data/processed_fe",
        "output_path": "models/random_forest_regressor.pkl",
    },
    dag=dag,
)

(
    download_data_task
    >> preprocess_data_task
    >> feature_engineering_task
    >> train_model_task
)
