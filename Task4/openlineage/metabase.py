from datetime import datetime
from uuid import uuid4

from openlineage.client.run import RunEvent, RunState, Run, Job
from openlineage.client import OpenLineageClient

import openlineage.sources as os

producer = 'manual_annotation'
client = OpenLineageClient(url='http://localhost:5000')
job = Job(namespace='default', name='metabase')
run = Run(str(uuid4()))
inputs = [os.postgres_hub_stores, os.postgres_hub_products, os.postgres_hub_event_view, os.postgres_hub_event_store_link_click]
client.emit(
    RunEvent(
        RunState.START,
        datetime.now().isoformat(),
        run, job, producer,
        inputs=inputs,
    )
)
client.emit(
    RunEvent(
        RunState.COMPLETE,
        datetime.now().isoformat(),
        run, job, producer,
        inputs=inputs,
    )
)
