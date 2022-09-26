import random

from clickhouse_driver import Client
from faker import Faker


def generate_event_view(fake):
    return {'user_id': random.randint(1, 1000), 'product_id': random.randint(1, 1000),
                 'time': fake.date_time_this_month(), 'city': random.choice(cities)}


def generate_event_store_link_click(fake):
    x = generate_event_view(fake)
    x['source_store_id'] = random.randint(1, 100)
    return x


rows_to_generate = 10000
cities = ['Казань', 'Москва', 'Санкт-Петербург', 'Омск', 'Владивосток']
fake = Faker('ru_RU')


client = Client(port=9000, user='default', password='', host='localhost')
#print(client.execute('SHOW databases'))

client.execute('''
CREATE TABLE IF NOT EXISTS event_view(
    user_id Int32,
    product_id Int32,
    time DateTime,
    city String
) ENGINE = MergeTree()
ORDER BY time''')
client.execute('INSERT INTO event_view VALUES', [generate_event_view(fake) for i in range(rows_to_generate)])

client.execute('''
CREATE TABLE IF NOT EXISTS event_store_link_click(
    user_id Int32,
    product_id Int32,
    source_store_id Int32,
    time DateTime,
    city String
) ENGINE = MergeTree()
ORDER BY time''')
client.execute('INSERT INTO event_store_link_click VALUES',
               [generate_event_store_link_click(fake) for i in range(rows_to_generate)])
