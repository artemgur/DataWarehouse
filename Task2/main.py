import luigi
from ProductsToPostgresTask import ProductsToPostgresTask
from EventsToPostgresTask import EventsToProductsTask

luigi.build([EventsToProductsTask()], local_scheduler=True)
luigi.build([ProductsToPostgresTask()], local_scheduler=True)
