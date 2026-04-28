import asyncio
from celery import Celery
from core.config import settings
from core.pipeline import OSINTPipeline
from utils.logger import setup_logger

logger = setup_logger("celery_worker")

celery_app = Celery(
    "oan_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def run_pipeline_task(self, target: str):
    """
    Celery task wrapper for the OSINT pipeline.
    Runs the async pipeline inside a new event loop.
    """
    logger.info(f"[Task {self.request.id}] Starting pipeline for: {target}")
    try:
        pipeline = OSINTPipeline()
        result = asyncio.run(pipeline.run(target))
        logger.info(f"[Task {self.request.id}] Completed: {result}")
        return result
    except Exception as exc:
        logger.error(f"[Task {self.request.id}] Failed: {exc}")
        raise self.retry(exc=exc)


@celery_app.task
def scheduled_daily_scan():
    """
    Scheduled task: runs a daily scan against a predefined watchlist of APT groups.
    Configure with Celery Beat in config/celery_beat.py
    """
    watchlist = settings.TARGET_KEYWORDS
    if not watchlist:
        logger.warning("No targets in watchlist. Set TARGET_KEYWORDS in .env")
        return

    for target in watchlist:
        run_pipeline_task.delay(target)
        logger.info(f"Queued daily scan for: {target}")
