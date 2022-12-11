import json
from datetime import datetime

from airflow.models import DAG
from airflow.operators.python import PythonVirtualenvOperator, PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

import source_annotations as sa, task_products_extract, task_products_load


default_args = {
    'depends_on_past': False
}


with DAG(dag_id='products_dag',
         schedule='@daily',
         catchup=False,
         start_date=datetime(2022, 12, 5, 14),
         default_args=default_args):
    extract_products = PythonVirtualenvOperator(task_id='products_extract_task',
                                      inlets=[sa.products_source_api],
                                      outlets=[sa.products_extract_task_xcom],
                                      do_xcom_push=True,
                                      requirements=["psycopg2", "faker"],
                                      system_site_packages=True,
                                      #provide_context=False,
                                      python_callable=task_products_extract.run)


    load_products = PythonOperator(task_id='products_load_task',
                                   inlets=[sa.products_extract_task_xcom],
                                   outlets=[sa.postgres_hub_products],
                                   #requirements=["psycopg2", "faker"],
                                   #system_site_packages=True,
                                   #provide_context=False,
                                   python_callable=task_products_load.run)

    extract_products >> load_products

    #transform_products = PostgresOperator(task_id='products_load_task', sql="CALL products_from_temporary()")