CREATE TYPE city_type as ENUM ('Казань', 'Москва', 'Санкт-Петербург', 'Омск', 'Владивосток');

CREATE TABLE IF NOT EXISTS event_view(
    user_id int,
    product_id int,
    source_store_id int,
    time timestamp,
    city city_type,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (source_store_id) REFERENCES source_stores(id) ON DELETE CASCADE
);

CREATE INDEX event_view_time ON event_view(time);

CREATE TABLE IF NOT EXISTS event_store_link_click(
    user_id int,
    product_id int,
    source_store_id int,
    time timestamp,
    city city_type,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (source_store_id) REFERENCES source_stores(id) ON DELETE CASCADE
);

CREATE INDEX event_store_link_click_time ON event_store_link_click(time);

