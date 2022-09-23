import json
import random
from faker import Faker
import psycopg2


rows_to_generate = 100000
rows_to_duplicate = 1000
manufacturers = ['LG', 'HP', 'Samsung', 'Huawei', 'Canon', 'Lenovo', 'Xiaomi']
category = ['Laptop', 'PC', 'Printer', 'Monitor', 'Smartphone']
colors = ['Black', 'Grey', 'White']


def get_domain_list():
    connection = psycopg2.connect(dbname='postgres', user='postgres', password='postgrespw', host='localhost', port=49153)
    with connection.cursor() as cursor:
        cursor.execute('SELECT website FROM source_stores')
        return list(map(lambda x: x[0], cursor.fetchall()))


def generate_products(rows_to_generate=1000, infinite=False):
    duplicated_rows = []

    fake = Faker('ru_RU')

    domain_list = get_domain_list()

    for i in range(rows_to_generate):
        if infinite:
            i -= 2
        source_store_id = random.randint(0, 99)
        url = domain_list[source_store_id] + '/' + fake.md5()

        if len(duplicated_rows) > 0 and random.random() > 0.95:
            product_index = random.randint(0, len(duplicated_rows) - 1)
            product = duplicated_rows[product_index]
            #product['url'] =
            product['price'] = int(product['price'] * random.uniform(0.8, 1.2))
            if 'color' not in product['attributes']:
                product['attributes']['color'] = random.choice(colors)
            if random.random() > 0.5:
                duplicated_rows.pop(product_index)
        else:
            product = {'manufacturer': random.choice(manufacturers),
                       'model': fake.md5()[:6], 'price': random.randint(1000, 100000),
                       'length': random.randint(10, 100), 'width': random.randint(10, 100),
                       'height': random.randint(10, 100), 'weight': round(random.uniform(0.1, 4), 1),
                       'category': random.choice(category), 'attributes': {}}
            match product['category']:
                case 'Laptop':
                    product['attributes']['touchscreen'] = random.choice([True, False])
                case 'PC':
                    product['attributes']['ram'] = random.choice([2, 4, 8, 16, 32])
                    product['attributes']['ram_slots'] = random.randint(1, 4)
                case 'Printer':
                    product['attributes']['color_printer'] = random.choice([True, False])
                case 'Monitor':
                    product['attributes']['refresh_rate'] = random.choice([60, 90, 120, 144])
                case 'Smartphone':
                    product['attributes']['ram'] = random.choice([2, 4, 8, 16, 32])
                    product['attributes']['sim_count'] = random.randint(1, 2)
            if len(duplicated_rows) < rows_to_duplicate:
                duplicated_rows.append(product)

        product['source_store_id'] = source_store_id + 1
        product['url'] = url
        #product['query_time'] = str(fake.date_time_this_month())
        yield product  # json.dumps(product, ensure_ascii=False)


if __name__ == '__main__':
    for product in generate_products(10):
        print(product)
