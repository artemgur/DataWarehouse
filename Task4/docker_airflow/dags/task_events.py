from datetime import datetime


def run():
    from clickhouse_driver import Client

    client = Client(port=9000, user='default', password='', host='clickhouse')
    event_view_max_time_query = client.execute('SELECT MAX(time) FROM event_view_postgres')
    event_view_max_time = event_view_max_time_query[0][0] if len(event_view_max_time_query) > 0 else datetime.min
    client.execute('INSERT INTO event_view_postgres SELECT * FROM event_view WHERE time > %(max_time)s',
                   {'max_time': event_view_max_time})

    event_click_max_time_query = client.execute('SELECT MAX(time) FROM event_store_link_click_postgres')
    event_click_max_time = event_click_max_time_query[0][0] if len(event_click_max_time_query) > 0 else datetime.min
    client.execute('INSERT INTO event_store_link_click_postgres SELECT * FROM event_store_link_click WHERE time > %(max_time)s',
                   {'max_time': event_click_max_time})