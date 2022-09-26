CREATE TABLE IF NOT EXISTS event_view_postgres(
    user_id Int32,
    product_id Int32,
    time DateTime,
    city String
) ENGINE = PostgreSQL('172.20.0.2:5432', 'task2', 'event_view', 'postgres', 'postgres');


CREATE TABLE IF NOT EXISTS event_store_link_click_postgres(
    user_id Int32,
    product_id Int32,
    source_store_id Int32,
    time DateTime,
    city String
) ENGINE = PostgreSQL('172.20.0.2:5432', 'task2', 'event_view', 'postgres', 'postgres');

--DROP TABLE event_view_postgres;
--DROP TABLE event_store_link_click_postgres;

