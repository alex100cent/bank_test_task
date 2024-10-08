import asyncio
from celery import Celery

from app.config import redis
from app.services.outbox_service import outbox_send_service

celery = Celery(__name__)
redis_url = f"redis://:{redis.password}@{redis.host}:{redis.port}/0"
celery.conf.broker_url = redis_url
celery.conf.result_backend = redis_url

celery.conf.beat_schedule = {
    "run_every_3_second": {
        "task": "outbox_send",
        "schedule": 3,
    }
}


@celery.task(name="outbox_send")
def outbox_send_task():
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(outbox_send_service())
    else:
        loop.run_until_complete(outbox_send_service())
