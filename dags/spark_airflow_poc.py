import airflow
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

with DAG('pyspark_ariflow_processing',start_date=datetime(2024,1,1),schedule='@daily',catchup=False) as dag:
    pyspark_processing_task=SparkSubmitOperator(
        task_id='pyspark_processing_task',
        application='/opt/airflow/dags/pyspark_test.py',#the full path of dags folder in airflow worker container
        conn_id='spark_conn_id',
    )