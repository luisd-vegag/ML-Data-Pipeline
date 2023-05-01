from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

dag = DAG(
    "dummy_dag",
    description="A dummy DAG to test Airflow",
    start_date=datetime(2023, 4, 30),
    schedule_interval="@once",
)

t1 = BashOperator(
    task_id="print_hello",
    bash_command='echo "Hello, World!"',
    dag=dag,
)

t2 = BashOperator(
    task_id="print_goodbye",
    bash_command='echo "Goodbye, World!"',
    dag=dag,
)

t1 >> t2
