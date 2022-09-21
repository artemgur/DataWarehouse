import json
import luigi
import psycopg2
from GetProducts import GetProducts


class ProductsTask(luigi.Task):
    def requires(self):
        return GetProducts()

    def run(self):
        connection = psycopg2.connect(dbname='postgres', user='postgres', password='postgrespw', host='localhost', port=49153)
        with self.input().open('r') as input_target:
            products_json = input_target.read()
        products = json.loads(products_json)
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name FROM information_schema.columns
                    WHERE table_name = 'logged' AND table_schema = 'public' AND column_name != 'attributes'
                    """)
            non_attributes_columns = list(map(lambda x: x[0], cursor.fetchall()))
            products_attributes

            cursor.execute("""           
            INSERT INTO products(manufacturer, model, length, width, height, weight, category, attributes)
            VALUES (%(manufacturer)s, %(model)s, %(length)s, %(width)s, %(height)s, %(weight)s, %(category)s, %(attributes)s)
            ON CONFLICT (products_manufacturer_model)
            DO UPDATE SET attributes = attributes || %(attributes)s
            RETURNING id, manufacturer, model INTO returning_result;
            """, products)
            cursor.execute()
