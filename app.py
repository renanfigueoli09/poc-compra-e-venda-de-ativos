import os
import dotenv
dotenv.load_dotenv()
from flask import Flask
from celery.schedules import crontab
from src.config.celery_config import make_celery
from flask_caching import Cache
flask_app = Flask(__name__)
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
cache.init_app(flask_app)
celery = make_celery(flask_app)
celery.conf.beat_schedule = {
    'BOOT': {
        'task': 'src.tasks.assets.boot',  # Nome correto da sua task
        'schedule': crontab(minute='*/15'),  # A cada 15 minutos
    },
}
from src.routes import *
