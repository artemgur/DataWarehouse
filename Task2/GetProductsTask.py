import time
import random
from itertools import islice
import json
import luigi
#from ..Task1.GenerateProducts import generate_products

import sys
sys.path.append("../Task1")
from GenerateProducts import generate_products


products_count = 1200
min_batch_size = 20
max_batch_size = 50
time_between_batches = 0.1


class GetProductsTask(luigi.Task):
    def output(self):
        return luigi.LocalTarget('products.txt')

    def run(self):
        products = json.dumps(list(generate_products(products_count)), ensure_ascii=False)
        with self.output().open('w') as f:
            f.write(products)
