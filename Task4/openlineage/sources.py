from openlineage.client.run import Dataset


postgres_source_stores = Dataset(namespace='default', name='postgres_source.postgres.source_stores')
postgres_hub_stores = Dataset(namespace='default', name='postgres_hub.postgres.source_stores')
postgres_hub_products = Dataset(namespace='default', name='postgres_hub.postgres.products')

postgres_hub_event_view = Dataset(namespace='default', name='postgres_hub.postgres.event_view')
postgres_hub_event_store_link_click = Dataset(namespace='default', name='postgres_hub.postgres.event_store_link_click')
