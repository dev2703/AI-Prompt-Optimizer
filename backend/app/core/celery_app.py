from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "ai_prompt_optimizer",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.optimization_tasks",
        "app.tasks.analytics_tasks",
        "app.tasks.email_tasks",
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    broker_connection_retry_on_startup=True,
    result_expires=3600,  # 1 hour
    task_routes={
        "app.tasks.optimization_tasks.*": {"queue": "optimization"},
        "app.tasks.analytics_tasks.*": {"queue": "analytics"},
        "app.tasks.email_tasks.*": {"queue": "email"},
    },
    task_default_queue="default",
    task_default_exchange="default",
    task_default_routing_key="default",
)

# Optional: Configure result backend for better performance
if settings.ENVIRONMENT == "production":
    celery_app.conf.update(
        result_backend_transport_options={
            "master_name": "mymaster",
            "visibility_timeout": 3600,
        }
    ) 