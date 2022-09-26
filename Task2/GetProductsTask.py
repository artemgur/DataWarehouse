import json
import luigi

import sys
sys.path.append("../Task1")
from GenerateProducts import generate_products


products_count = 1200


class GetProductsTask(luigi.Task):
    def output(self):
        return luigi.LocalTarget('products.txt')

    def run(self):
        products = json.dumps(list(generate_products(products_count)), ensure_ascii=False)
        with self.output().open('w') as f:
            f.write(products)
