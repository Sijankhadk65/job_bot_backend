import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

connection_link = "redis://localhost:6379/0"

# This must match the same name you'll use in your task file
celery_app = Celery(
    "tasks",
    broker=connection_link,
    backend=connection_link,
)

# Optional: Show results in dashboard like Flower
celery_app.conf.update(result_expires=3600, task_serializer="json")
