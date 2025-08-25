import os
from celery import Celery


app = Celery('dual_input')


app.conf.broker_url = os.environ.get("BROKER_URL", "amqp://admin:password@rabbitmq_messenger:5672//")

app.autodiscover_tasks(['dual_input'])