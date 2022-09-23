import luigi
from ProductsToPostgresTask import ProductsToPostgresTask

luigi.build([ProductsToPostgresTask()], local_scheduler=True)
