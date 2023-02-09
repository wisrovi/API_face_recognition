import os

from celery import Celery

broker_url = os.environ.get("BROKER_RABBITMQ")
redis_url = os.environ.get("BROKER_REDIS")

if not broker_url:
    print("BROKER_RABBITMQ not found in env")
if not redis_url:
    print("BROKER_REDIS not found in env")

broker_url = "amqp://localhost" if not broker_url else broker_url
redis_url = "redis://localhost" if not redis_url else redis_url

app = Celery('tasks', broker=broker_url, backend=redis_url)
app.conf.update(
    result_expires=3600,
)
