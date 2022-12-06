import psycopg2
from faker import Faker


def fake_phone_number(fake: Faker) -> str:
    return f'+7{fake.msisdn()[3:]}'


rows_to_generate = 100
fake = Faker('ru_RU')

connection = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost', port=5433)
with connection.cursor() as cursor:
    cursor.execute('DROP TABLE IF EXISTS source_stores')
    cursor.execute('''
    CREATE TABLE source_stores(
        id serial PRIMARY KEY,
        name varchar(50) UNIQUE,
        phone char(12) UNIQUE,
        email varchar(50) UNIQUE,
        website varchar(50) UNIQUE,
        password_hash char(64)
    )
    ''')
    for i in range(rows_to_generate):
        cursor.execute(f"""INSERT INTO source_stores (name, phone, email, website, password_hash) VALUES 
        ('{fake.unique.company()}', '{fake_phone_number(fake)}', '{fake.unique.company_email()}', '{fake.unique.domain_name()}',
        '{fake.md5() * 2}')""")
    connection.commit()