from celery import Celery


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
        enable_utc=True,
        timezone="America/Sao_Paulo",
        result_expires=0,
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        worker_pool_restarts=True,
        log_format=(
            "%(asctime)s [%(levelname)s]: task_name=%(name)s task_id=%(task_id)s "
            "request_id=%(request_id)s message=%(message)s"
        ),
        date_time_format="%Y-%m-%dT%H:%M:%S%z",
    )
    celery.conf.update(app.config)
    return celery
