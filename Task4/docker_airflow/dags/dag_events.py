from datetime import datetime

from airflow.models import DAG
from airflow.operators.python import PythonVirtualenvOperator

import source_annotations as sa, task_events


default_args = {
    'depends_on_past': False
}


with DAG(dag_id='events_dag',
         schedule='@daily',
         catchup=False,
         start_date=datetime(2022, 12, 5, 14),
         default_args=default_args):
    PythonVirtualenvOperator(task_id='events_task',
                                      inlets=[sa.clickhouse_event_view, sa.clickhouse_event_store_link_click],
                                      outlets=[sa.postgres_hub_event_view, sa.postgres_hub_event_store_link_click],
                                      requirements=["clickhouse_driver"],
                                      system_site_packages=True,
                                      #provide_context=False,
                                      python_callable=task_events.run)

