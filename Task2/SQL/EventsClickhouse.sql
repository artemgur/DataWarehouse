--DROP TABLE event_view_postgres;
--DROP TABLE event_store_link_click_postgres;

CREATE TABLE IF NOT EXISTS event_view_postgres(
    user_id Int32,
    product_id Int32,
    time DateTime,
    city String
) ENGINE = PostgreSQL('postgres_hub:5432', 'postgres', 'event_view', 'postgres', 'postgres');


CREATE TABLE IF NOT EXISTS event_store_link_click_postgres(
    user_id Int32,
    product_id Int32,
    source_store_id Int32,
    time DateTime,
    city String
) ENGINE = PostgreSQL('postgres_hub:5432', 'postgres', 'event_store_link_click', 'postgres', 'postgres');
