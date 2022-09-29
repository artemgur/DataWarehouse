CREATE TYPE category_type as ENUM ('Laptop', 'PC', 'Printer', 'Monitor', 'Smartphone');

CREATE TABLE products(
    id serial PRIMARY KEY,
    manufacturer varchar(20) NOT NULL,
    model varchar(20) NOT NULL,
    length int NOT NULL CHECK (length > 0),
    width int NOT NULL CHECK (length > 0),
    height int NOT NULL CHECK (length > 0),
    weight int NOT NULL CHECK (length > 0),
    category category_type NOT NULL,
    attributes jsonb NOT NULL
);

CREATE UNIQUE INDEX products_manufacturer_model ON products(manufacturer, model);

CREATE TABLE product_prices(
    product_id int NOT NULL,
    source_store_id int NOT NULL,
    product_source_store_url TEXT NOT NULL,
    price int NOT NULL CHECK (price > 0),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (source_store_id) REFERENCES source_stores(id) ON DELETE CASCADE,
    UNIQUE (product_id, source_store_id)
);

CREATE TABLE products_temporary(
    manufacturer varchar(20),
    model varchar(20),
    length int,
    width int,
    height int,
    weight int,
    category category_type,
    price int,
    source_store_id int,
    url text,
    attributes jsonb
);

CREATE OR REPLACE FUNCTION json_aggregate_step(aggregated jsonb, new jsonb) RETURNS jsonb AS $$
    BEGIN
        RETURN aggregated || new;
    END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE AGGREGATE json_aggregate(jsonb)(
    SFUNC = json_aggregate_step,
    STYPE = jsonb,
    INITCOND = '{}'
);

CREATE OR REPLACE FUNCTION last_aggregate_step(aggregated anyelement, new anyelement) RETURNS anyelement AS $$
    BEGIN
        RETURN new;
    END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE AGGREGATE last_aggregate(anyelement)(
    SFUNC = last_aggregate_step,
    STYPE = anyelement
);

CREATE OR REPLACE PROCEDURE products_from_temporary() AS $$
    WITH products_temporary_aggregated AS (
        SELECT manufacturer, model, last_aggregate(length) AS length, last_aggregate(width) AS width,
               last_aggregate(height) AS height, last_aggregate(weight) AS weight, last_aggregate(category) AS category,
               json_aggregate(attributes) AS attributes FROM products_temporary
        GROUP BY (manufacturer, model)
    ),
        products_returning AS (
        INSERT INTO products (manufacturer, model, length, width, height, weight, category, attributes)
            SELECT manufacturer, model, length, width, height, weight, category, attributes
            FROM products_temporary_aggregated
            ON CONFLICT (manufacturer, model)
                DO UPDATE SET length = excluded.length, width = excluded.width, height = excluded.height,
                    weight = excluded.weight, category = excluded.category,
                    attributes = products.attributes || excluded.attributes
            RETURNING id AS product_id, manufacturer, model
    ),
    products_temporary_aggregated_prices AS (
        SELECT manufacturer, model, source_store_id,
               last_aggregate(url) AS product_source_store_url, last_aggregate(price) AS price
        FROM products_temporary
        GROUP BY (manufacturer, model, source_store_id)
    )
    INSERT INTO product_prices
    SELECT product_id, source_store_id, product_source_store_url, price FROM products_temporary_aggregated_prices AS pt
        JOIN products_returning AS pr ON pt.manufacturer = pr.manufacturer AND pt.model = pr.model
        ON CONFLICT (product_id, source_store_id)
            DO UPDATE SET price = excluded.price, product_source_store_url = excluded.product_source_store_url;

    TRUNCATE TABLE products_temporary;
$$ LANGUAGE sql
