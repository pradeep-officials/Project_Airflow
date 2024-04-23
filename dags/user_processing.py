from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime
import json
from pandas import json_normalize
def _process_user(ti):
        user=ti.xcom_pull(task_ids='extract_user')
        user=user['results'][0]
        processed_user=json_normalize({
                'firstname':user['name']['first'],
                'lastname':user['name']['last']})
        processed_user.to_csv('/tmp/processed_user.csv',index=None,header=False)
def _store_user():
        hook=PostgresHook(postgres_conn_id='postgres')
        hook.copy_expert(
                sql="COPY USERS from stdin with delimiter as ',' ",
                filename='/tmp/processed_user.csv'
        )
        
with DAG('user_processing',start_date=datetime(2024,3,20),schedule_interval='@daily',catchup=False) as dag:
        create_table=PostgresOperator(task_id='create_table',
                                  postgres_conn_id='postgres',
                                  sql='''create table if not exists users(Fname varchar(20),Lname varchar(20));'''
                                  )
        is_api_available=HttpSensor(task_id='is_api_available',
                                    http_conn_id='user_api',
                                    endpoint='api/'
                                    )
        extract_user=SimpleHttpOperator(task_id='extract_user',
                                        http_conn_id='user_api',
                                    endpoint='api/',
                                    method='GET',
                                    response_filter=lambda response:json.loads(response.text),
                                    log_response=True)
        
        process_user=PythonOperator(task_id='process_user',
                                    python_callable=_process_user)
        store_user=PythonOperator(task_id='store_user',
                                  python_callable=_store_user)
        file_sensing=FileSensor(
                task_id='file_sensing',
                filepath='user_file.txt',
                fs_conn_id='file_conn',
                poke_interval=10
        )


        extract_user>>process_user     #extract_user -api for httpsopertor is blocked so website not responsind the JSON data
       # file_sensing>>store_user ##this checks if the file is avaibale in folder it triggeres the step 'store_user' to store data in postgres table