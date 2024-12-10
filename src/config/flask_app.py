import os
import dotenv
dotenv.load_dotenv()
from flask import Flask
from src.config.celery_config import make_celery
from flask_caching import Cache
url_redis= os.getenv("DBAAS_REDIS_HOST")
app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = url_redis
app.config['CELERY_RESULT_BACKEND'] = url_redis

cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
cache.init_app(app)
celery = make_celery(app)
from src.routes import *
