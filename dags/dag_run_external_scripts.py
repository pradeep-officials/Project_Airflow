import airflow
from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.operators.bash import BashOperator
from test_run_python_from_airflow import test_func1

from datetime import timedelta, datetime


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 8),
    'email': ['pradeep.jha3003@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(seconds=3)
}


def testing_email_notify():
    a = 3 + 4
    return a
# with DAG('test_run_python_from_airflow',start_date=datetime(2024,1,1),schedule='@daily',catchup=False) as dag:
with DAG('email_notification_etl',
        default_args=default_args,
        schedule_interval = '@daily',
        catchup=False) as dag:
    run_esternal_task=PythonOperator(
        task_id='run_esternal_task',
        python_callable=test_func1)

    run_external_python_file = BashOperator(
    task_id='run_external_python_file',
    bash_command='python /tmp/test_run_python_from_airflow.py')
    
    # send_email=EmailOperator(
    #         task_id='send_email',
    #         to='pradeep.jha1987@gmail.com',
    #         subject='Email From Airflow Dag Run-Susccess',
    #         html_content="""<h3> This Task in airflow is sccessfully completed! </h3>""")
    tsk_email_on_retry_on_pass = PythonOperator(
            task_id= 'tsk_email_on_retry_on_pass',
            python_callable=testing_email_notify
            )
        
    run_esternal_task>>run_external_python_file>>tsk_email_on_retry_on_pass