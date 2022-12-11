from datetime import datetime
from uuid import uuid4

from openlineage.client.run import RunEvent, RunState, Run, Job
from openlineage.client import OpenLineageClient

from openlineage.sources import postgres_source_stores, postgres_hub_stores

producer = 'manual_annotation'
client = OpenLineageClient(url='http://localhost:5000')
job = Job(namespace='default', name='postgres_stores_cdc')
run = Run(str(uuid4()))
client.emit(
    RunEvent(
        RunState.START,
        datetime.now().isoformat(),
        run, job, producer,
        inputs=[postgres_source_stores],
        outputs=[postgres_hub_stores]
    )
)
client.emit(
    RunEvent(
        RunState.COMPLETE,
        datetime.now().isoformat(),
        run, job, producer,
        inputs=[postgres_source_stores],
        outputs=[postgres_hub_stores]
    )
)
