import json
# from GenerateProducts import generate_products


# products_count = 1200


def run():
    products_count = 1200
    from GenerateProducts import generate_products
    products = list(generate_products(products_count))
    #ti = kwargs["ti"]
    #ti.xcom_push("task_products_extract_key", json.dumps(products, ensure_ascii=False))
    return products
