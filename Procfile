api_flask: flask run --host=0.0.0.0 --port=$PORT
celery_worker: celery -A app.celery worker --loglevel=info
schedule: celery -A app.celery beat --loglevel=INFO
monitor: celery -A  app.celery --broker=$DBAAS_REDIS_ENDPOINT flower --purge_offline_workers=10 --port=$PORT