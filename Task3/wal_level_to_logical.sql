ALTER SYSTEM SET WAL_LEVEL TO logical;

CREATE PUBLICATION postgres_debezium_source_publication FOR TABLE source_stores;

SELECT pg_create_logical_replication_slot('postgres_debezium_source_slot', 'pgoutput');
--SELECT pg_drop_replication_slot('postgres_debezium_source_slot');