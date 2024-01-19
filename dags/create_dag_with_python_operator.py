from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

# MAX XCOM SIZE is 48KB: 49344
default_args = {
    'owner': 'jrw',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def greet(ti):
    name = ti.xcom_pull(task_ids='get_name', key='name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print(f"Hellow World! My name is {name}, "
          f"and I am {age} years old!")

# def get_name():
#     return "FOOK"

def get_name(ti):
    ti.xcom_push(key='name', value='FOOK')

def get_age(ti):
    ti.xcom_push(key='age', value='999')

with DAG(
    default_args=default_args,
    dag_id='our_dag_with_python_operator_v06',
    description='Our first dag using python operator',
    start_date=datetime(2024, 1, 19),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id="greet",
        python_callable=greet,
        # op_kwargs={"age": 20}
    )

    task2= PythonOperator(
        task_id="get_name",
        python_callable=get_name
    )

    task3 = PythonOperator(
        task_id="get_age",
        python_callable=get_age
    )

    [task2, task3] >> task1
