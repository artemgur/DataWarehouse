import requests


def delete_connector(connector_name):
    response = requests.delete('http://localhost:8083/connectors/' + connector_name)
    print(response.text)


#delete_connector('postgres_debezium_source_connector')
delete_connector('postgres_sink_connector')