import os
from celery import Celery


app = Celery('dual_input')


app.conf.broker_url = os.environ.get("BROKER_URL", "amqp://admin:password@rabbitmq_messenger:5672//")
# TODO: backend for chords
# app.conf.result_backend = os.environ.get(
#     "CELERY_RESULT_BACKEND",
#     "redis://redis:6379/0"
# )
app.autodiscover_tasks(['dual_input'])