CREATE TABLE IF NOT EXISTS source_stores(
    id serial PRIMARY KEY,
    name varchar(50) UNIQUE,
    phone char(12) UNIQUE,
    email varchar(50) UNIQUE,
    website varchar(50) UNIQUE,
    password_hash char(64)
);

CREATE SUBSCRIPTION source_stores_subscription
    CONNECTION 'host=127.0.0.1 port=5432 user=postgres dbname=postgres'
    PUBLICATION source_stores_publication
    WITH (slot_name = 'source_stores_replication_slot', create_slot = false);
