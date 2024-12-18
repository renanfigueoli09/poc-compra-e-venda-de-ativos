import os
import re
from dotenv import load_dotenv
load_dotenv()
from celery import Celery
from redis.sentinel import Sentinel

def make_celery():
    DBAAS_SENTINEL_HOSTS = os.getenv("DBAAS_SENTINEL_HOSTS")
    DBAAS_SENTINEL_PORT = os.getenv("DBAAS_SENTINEL_PORT")
    DBAAS_SENTINEL_ENDPOINT = os.getenv("DBAAS_SENTINEL_ENDPOINT")
    DBAAS_SENTINEL_PASSWORD = os.getenv("DBAAS_SENTINEL_PASSWORD")
    DBAAS_SENTINEL_SERVICE_NAME = os.getenv("DBAAS_SENTINEL_SERVICE_NAME")
    print(DBAAS_SENTINEL_ENDPOINT)
    sentinel_hosts_list = [
        (host, DBAAS_SENTINEL_PORT) for host in DBAAS_SENTINEL_HOSTS.split(",")
    ]
    sentinel = Sentinel(
        sentinels=sentinel_hosts_list,
        socket_timeout=2.0,
        password=DBAAS_SENTINEL_PASSWORD,
    )
    master = sentinel.discover_master(DBAAS_SENTINEL_SERVICE_NAME)
    sentinel_urls = f"redis://:{DBAAS_SENTINEL_PASSWORD}@{master[0]}:{master[1]}/0"
    print(sentinel_urls)
    celery = Celery(
        broker=sentinel_urls,
        backend=sentinel_urls,
        enable_utc=True,
        timezone="America/Sao_Paulo",
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
    return celery
