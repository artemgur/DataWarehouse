import random

from clickhouse_driver import Client
from faker import Faker


rows_to_generate = 100000
cities = ['Казань', 'Москва', 'Санкт-Петербург', 'Омск', 'Владивосток']
fake = Faker('ru_RU')


client = Client()#TODO

# noinspection SqlNoDataSourceInspection
client.execute('''
CREATE TABLE IF NOT EXISTS event_view(
    user_id Int32,
    product_id Int32,
    time DateTime,
    city String,
) ENGINE = MergeTree()
ORDER BY time''')
# noinspection SqlNoDataSourceInspection
client.execute('INSERT INTO event_view VALUES',
               [{'user_id': random.randint(1, 100000), 'product_id': random.randint(1, 100000),\
                 'time': fake.date_time_this_month(), 'city': random.choice(cities)} for i in range(rows_to_generate)])
