CREATE PUBLICATION source_stores_publication FOR TABLE source_stores;

SELECT pg_create_logical_replication_slot('source_stores_replication_slot', 'pgoutput')