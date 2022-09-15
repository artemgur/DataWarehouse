import psycopg2
from faker import Faker


rows_to_generate = 100
fake = Faker('ru_RU')

connection = psycopg2.connect(dbname='postgres', user='postgres', password='postgrespw', host='abul.db.elephantsql.com', port=49153)
with connection.cursor() as cursor:
    # noinspection SqlNoDataSourceInspection
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS source_stores(
        id serial PRIMARY KEY,
        name varchar(50),
        phone char(12),
        email varchar(50),
        website varchar(50),
    )
    ''')
    for i in range(rows_to_generate):
        # noinspection SqlNoDataSourceInspection
        cursor.execute(f'''INSERT INTO source_stores (name, phone, email, website) VALUES 
        ({fake.company()}, {fake.phone_number().replace(" ", "")}, {fake.company_email()}, {fake.domain_name()})''')
    connection.commit()