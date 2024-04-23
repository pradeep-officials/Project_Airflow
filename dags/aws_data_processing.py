from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
import os
import boto3
from botocore.exceptions import ClientError
import logging
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime


# [START weblog_function]
def f_generate_log(*op_args, **kwargs):
    ti = kwargs['ti']
    lines = op_args[0]
    logFile ='/tmp/weblog_20240327-160743.log' #generate_log(lines)
    ti.xcom_push(key='logFileName', value=logFile)# [END weblog_function]# [Start weblog task]
# [End weblog task]


# [START s3_upload_file function]
def s3_upload_file(**kwargs):
        ti = kwargs['ti']
        bucketName = kwargs['bucketName']    
        fileName = ti.xcom_pull(task_ids='weblog', key='logFileName')
        objectName = os.path.basename(fileName)    
        s3_client = boto3.client('s3')    
        try:
            response = s3_client.upload_file(fileName, bucketName, objectName)
        except ClientError as e:
            return False
        return True# [END s3_upload_file function]
with DAG('aws_data_processing',start_date=datetime(2024,3,20),schedule_interval='@daily',catchup=False) as dag:
            file_sensing=FileSensor(
                task_id='file_sensing',
                filepath='user_file.txt',
                fs_conn_id='file_conn',
                poke_interval=10
                )
            create_weblog_task = PythonOperator(
            task_id='weblog',
            python_callable=f_generate_log,
            op_args = [30],
            )
            s3_upload_log_file_task = PythonOperator(
            task_id = 's3_upload_log_file',
            python_callable=s3_upload_file,
            # bucketname='airflowbucket-01'
            op_kwargs = {'bucketName':'airflowbucket-01'},
            )# [End s3 upload task]
            
create_weblog_task>>s3_upload_log_file_task