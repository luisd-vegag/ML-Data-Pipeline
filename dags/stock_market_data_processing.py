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
