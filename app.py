import os
import dotenv
dotenv.load_dotenv()
from flask import Flask
from src.config.celery_config import make_celery
from flask_caching import Cache
flask_app = Flask(__name__)
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
cache.init_app(flask_app)
celery = make_celery(app=flask_app)
from src.routes import *
