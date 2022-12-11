import json

import psycopg2


def run(ti):
    #ti = kwargs["ti"]
    products_list = ti.xcom_pull(task_ids='products_extract_task')
    if not products_list:
        raise ValueError('No value currently stored in XComs.')
    #products_list = json.loads(products_list)

    connection = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='postgres_hub', port=5432)

    for product in products_list:
        product['attributes'] = json.dumps(product['attributes'], ensure_ascii=False)
    with connection.cursor() as cursor:
        cursor.executemany("""           
        INSERT INTO products_temporary
        VALUES (%(manufacturer)s, %(model)s, %(length)s, %(width)s, %(height)s, %(weight)s, %(category)s,
         %(price)s, %(source_store_id)s, %(url)s, %(attributes)s)
        """, products_list)
        cursor.execute("CALL products_from_temporary()")
        connection.commit()