import os
import dotenv
dotenv.load_dotenv()
from flask import Flask
from src.config.celery_config import make_celery
from flask_caching import Cache
url_redis= os.getenv("DBAAS_REDIS_HOST")
flask_app = Flask(__name__)

flask_app.config['CELERY_BROKER_URL'] = url_redis
flask_app.config['CELERY_RESULT_BACKEND'] = url_redis

cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
cache.init_app(flask_app)
celery = make_celery(app=flask_app)
from src.routes import *
