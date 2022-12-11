from airflow.lineage.entities import Table


def create_table(cluster, database, name):
    return Table(
        database=database,
        cluster=cluster,
        name=name,
    )


products_extract_task_xcom = create_table('default', 'products_dag', 'products_extract_task_xcom')
products_source_api = create_table('default', 'external', 'Product APIs')
postgres_source_stores = create_table('default', 'postgres_source.postgres', 'source_stores')
postgres_hub_stores = create_table('default', 'postgres_hub.postgres', 'source_stores')
postgres_hub_products = create_table('default', 'postgres_hub.postgres', 'products')
postgres_hub_event_view = create_table('default', 'postgres_hub.postgres', 'event_view')
postgres_hub_event_store_link_click = create_table('default', 'postgres_hub.postgres', 'event_store_link_click')
clickhouse_event_view = create_table('default', 'clickhouse.default', 'event_view')
clickhouse_event_store_link_click = create_table('default', 'clickhouse.default', 'event_store_link_click')
