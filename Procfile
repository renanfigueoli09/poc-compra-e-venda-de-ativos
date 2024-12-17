api_flask: flask run --host=0.0.0.0 --port=$PORT

celery_worker: celery -A app.celery worker --loglevel=info
schedule: celery -A app.celery beat --loglevel=DEBUG 
flower: celery flower -A app.celery --port=$PORT