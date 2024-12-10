api_flask: newrelic-admin run-program flask run --host=0.0.0.0 --port=$PORT
celery_schedule: celery -A app.celery beat --loglevel=info
celery_worker: celery -A app.celery worker --loglevel=info
flower: newrelic-admin run-program celery -A app.celery flower --purge_offline_workers=10 --port=$PORT --broker=$DBAAS_REDIS_HOST
