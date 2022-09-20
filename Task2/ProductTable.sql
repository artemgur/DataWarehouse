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
)