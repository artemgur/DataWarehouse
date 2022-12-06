from marquez_client import MarquezClient

client = MarquezClient(url='http://localhost:5000')

# list namespaces
client.create_source
print(client.list_namespaces())