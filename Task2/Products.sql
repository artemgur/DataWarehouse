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

CREATE INDEX products_manufacturer_model ON products(manufacturer, model);

CREATE TABLE product_prices(
    product_id int NOT NULL,
    source_store_id int NOT NULL,
    product_source_store_url TEXT NOT NULL,
    price int NOT NULL CHECK (price > 0),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (source_store_id) REFERENCES source_stores(id) ON DELETE CASCADE
);

CREATE TABLE product_temporary(
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

CREATE OR REPLACE PROCEDURE products_from_temporary() AS $$
DECLARE products_returning TABLE(product_id int, manufacturer varchar(20), model varchar(20));
BEGIN
    INSERT INTO products(manufacturer, model, length, width, height, weight, category, attributes)
        SELECT manufacturer, model, length, width, height, weight, category, attributes FROM product_temporary
        ON CONFLICT (manufacturer, model)
            DO UPDATE SET attributes = products.attributes || product_temporary.attributes
        RETURNING id, manufacturer, model INTO products_returning;

    INSERT INTO product_prices
    SELECT product_id, source_store_id, url, price FROM product_temporary AS pt
        JOIN products_returning AS pr ON pt.manufacturer = pr.manufacturer AND pt.model = pr.model;

    TRUNCATE TABLE product_temporary;
END;
$$ LANGUAGE plpgsql
