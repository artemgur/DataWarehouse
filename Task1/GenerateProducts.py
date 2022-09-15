import random


rows_to_generate = 100000
manufacturers = ['LG', 'HP', 'Samsung', 'Huawei', 'Canon', 'Lenovo', 'Xiaomi']
category = ['Laptop', 'PC', 'Printer', 'Monitor', 'Smartphone']

for i in range(rows_to_generate):
    product = {}
    product['manufacturer'] = random.choice(manufacturers)
    product['price'] = random.randint(1000, 1000000)
    product['length'] = random.randint(10, 100)
    product['width'] = random.randint(10, 100)
    product['height'] = random.randint(10, 100)
    product['weight'] = random.uniform(0.1, 4)
    product['category'] = random.choice(category)
    match product['category']:
        case 'Laptop':
            product['touchscreen'] = random.choice([True, False])
        case 'PC':
            product['ram'] = random.choice([2, 4, 8, 16, 32])
            product['ram_slots'] = random.randint(1, 4)
        case 'Printer':
            product['color'] = random.choice([True, False])
        case 'Monitor':
            product['refresh_rate'] = random.choice([60, 90, 120, 144])
        case 'Smartphone':
            product['ram'] = random.choice([2, 4, 8, 16, 32])
            product['sim_count'] = random.randint(1, 2)
    product.json

