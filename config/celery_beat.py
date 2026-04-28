from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # Run daily scan every day at 06:00 UTC
    "daily-osint-scan": {
        "task": "worker.tasks.scheduled_daily_scan",
        "schedule": crontab(hour=6, minute=0),
    },
}
