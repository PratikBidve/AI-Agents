import os
import time

from celery import Celery

broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery_app = Celery(
    "worker",
    broker=broker_url,
    backend=result_backend
)

@celery_app.task(name="run_autonomous_agent")
def run_autonomous_agent(prompt: str) -> str:
    """Mock long-running autonomous agent task."""
    print(f"Starting long-running agent task with prompt: {prompt}")
    time.sleep(15)
    print("Agent task complete.")
    return f"Processing completed successfully for prompt: '{prompt}'"
