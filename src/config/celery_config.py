import os
from dotenv import load_dotenv

load_dotenv()
from celery import Celery
from redis.sentinel import Sentinel


def make_celery(app):
    DBAAS_SENTINEL_SERVICE_NAME = os.getenv("DBAAS_SENTINEL_SERVICE_NAME")
    DBAAS_SENTINEL_HOSTS: str | None = os.getenv("DBAAS_SENTINEL_HOSTS")
    host = DBAAS_SENTINEL_HOSTS.split(",")
    print(host)
    DBAAS_SENTINEL_PORT = os.getenv("DBAAS_SENTINEL_PORT")
    DBAAS_SENTINEL_PASSWORD = os.getenv("DBAAS_SENTINEL_PASSWORD")
    DBAAS_MONGODB_ENDPOINT = os.getenv("DBAAS_MONGODB_ENDPOINT")
    CELERY_BROKER_ENDPOINT = os.getenv("CELERY_BROKER_ENDPOINT")
    # url = f"sentinel://{DBAAS_SENTINEL_PASSWORD}@{host[0]}:{DBAAS_SENTINEL_PORT}/0;sentinel://{DBAAS_SENTINEL_PASSWORD}@{host[1]}:{DBAAS_SENTINEL_PORT}/0;sentinel://{DBAAS_SENTINEL_PASSWORD}@{host[2]}:{DBAAS_SENTINEL_PORT}/0"
    # url = f"sentinel://{host[0]}:{DBAAS_SENTINEL_PORT}/0;sentinel://{host[1]}:{DBAAS_SENTINEL_PORT}/0;sentinel://{host[2]}:{DBAAS_SENTINEL_PORT}/0"
    print("TASDASFADSFGADSF")
    print(CELERY_BROKER_ENDPOINT)

    # sentinel = Sentinel([('sentinel1', 26379), ('sentinel2', 26379), ('sentinel3', 26379)], socket_timeout=0.1)
    # master = sentinel.master_for(DBAAS_SENTINEL_SERVICE_NAME, socket_timeout=0.1)
    # print(master.connection_pool.get_connection())
    url = "redis://172.21.0.5:26379,172.21.0.6:26380?sentinel=redis_master&password=mypassword"
    celery = Celery(
        app.import_name,
        # broker_url = f'redis://{redis_master.connection_pool.get_connection().host}:{redis_master.connection_pool.get_connection().port}/0',
        # result_backend = f'redis://{redis_master.connection_pool.get_connection().host}:{redis_master.connection_pool.get_connection().port}/0',
        # redis_sentinel_service = 'redis_master',
        broker_transport_options={
            # "sentinels": [
            #     ("sentinel1", 26379),
            #     ("sentinel2", 26380),
            #     ("sentinel3", 26381),
            # ],
            "master_name": "redis_master",  # Configuração do nome do mestre no Redis Sentinel
            "socket_timeout": 0.1,
            "sentinel_kwargs": {"password": ""},
        },
        # broker="sentinel://172.21.0.5:26379/0",
        # broker=url,
        backend=url,
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
        alternative_result_backend=DBAAS_MONGODB_ENDPOINT,
        celery_max_retries=7,
        result_expires=0,
        result_persistent=True,
        MONGO_PORT="27017",
    )
    celery.conf.update(app.config)
    return celery
