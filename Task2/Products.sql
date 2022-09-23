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
    FOREIGN KEY (source_store_id) REFERENCES source_stores(id) ON DELETE CASCADE
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



-- CREATE OR REPLACE FUNCTION json_aggregate_final(aggregated jsonb) RETURNS jsonb AS $$
--     BEGIN
--         RETURN aggregated;
--     END;
-- $$ LANGUAGE plpgsql;

CREATE AGGREGATE json_aggregate(jsonb)(
    SFUNC = json_aggregate_step,
    STYPE = jsonb,
    INITCOND = '{}'
    );

CREATE OR REPLACE FUNCTION last_aggregate_step(aggregated anyelement, new anyelement) RETURNS anyelement AS $$
    BEGIN
        RETURN new;
    END;
$$ LANGUAGE plpgsql;

CREATE AGGREGATE last_aggregate(anyelement)(
    SFUNC = last_aggregate_step,
    STYPE = anyelement
    --INITCOND = '{}'
    );

CREATE OR REPLACE PROCEDURE products_from_temporary() AS $$
DECLARE products_returning record;--TABLE(product_id int, manufacturer varchar(20), model varchar(20));
BEGIN
    WITH products_temporary_aggregated AS (
        SELECT manufacturer, model, last_aggregate(length) AS length, last_aggregate(width) AS width, last_aggregate(height) AS height,
               last_aggregate(weight) AS weight, last_aggregate(category) AS category, json_aggregate(attributes) AS attributes FROM products_temporary
        GROUP BY (manufacturer, model)
    ),
        products_returning AS (
        INSERT INTO products (manufacturer, model, length, width, height, weight, category, attributes)
            SELECT manufacturer, model, length, width, height, weight, category, attributes
            FROM products_temporary_aggregated
            ON CONFLICT (manufacturer, model)
                DO UPDATE SET attributes = products.attributes || excluded.attributes
            RETURNING id AS product_id, manufacturer, model)
    INSERT INTO product_prices
    SELECT product_id, source_store_id, url, price FROM products_temporary AS pt
        JOIN products_returning AS pr ON pt.manufacturer = pr.manufacturer AND pt.model = pr.model;

    TRUNCATE TABLE products_temporary;
END;
$$ LANGUAGE plpgsql
