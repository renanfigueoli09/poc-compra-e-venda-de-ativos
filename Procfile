api_flask: newrelic-admin run-program flask run --host=0.0.0.0 --port=$PORT
celery_schedule: newrelic-admin run-program celery -A app.celery beat --loglevel=info
# celery_worker: newrelic-admin run-program celery -A app.celery worker --loglevel=DEBUG --concurrency=1 
celery_worker_boot: newrelic-admin run-program celery -A app.celery worker -Q boot --concurrency=4  --loglevel=info -E -n BOOT@%h 
flower: newrelic-admin run-program celery flower -A app.celery --purge_offline_workers=10 --port=$PORT