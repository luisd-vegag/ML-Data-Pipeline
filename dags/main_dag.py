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
