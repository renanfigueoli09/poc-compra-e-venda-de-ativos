api_flask: newrelic-admin run-program flask run --host=0.0.0.0 --port=$PORT
celery_schedule: newrelic-admin run-program celery -A app.celery beat --loglevel=DEBUG
celery_worker: newrelic-admin run-program celery -A app.celery worker --loglevel=DEBUG --concurrency=1 
flower: newrelic-admin run-program celery flower -A app.celery --purge_offline_workers=10 --port=$PORT