import json
import luigi
import psycopg2
from psycopg2.extras import execute_values
from GetProductsTask import GetProductsTask


class ProductsToPostgresTask(luigi.Task):
    def requires(self):
        return GetProductsTask()

    def run(self):
        connection = psycopg2.connect(dbname='task2', user='postgres', password='postgrespw', host='localhost', port=49153)
        with self.input().open('r') as input_target:
            products_json = input_target.read()
        products = json.loads(products_json)
        for product in products:
            product['attributes'] = json.dumps(product['attributes'], ensure_ascii=False)
        #print(products)
        with connection.cursor() as cursor:
            cursor.executemany("""           
            INSERT INTO products_temporary
            VALUES (%(manufacturer)s, %(model)s, %(length)s, %(width)s, %(height)s, %(weight)s, %(category)s,
             %(price)s, %(source_store_id)s, %(url)s, %(attributes)s)
            """, products)
            cursor.execute("CALL products_from_temporary()")
            connection.commit()
