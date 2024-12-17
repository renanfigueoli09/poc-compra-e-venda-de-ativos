import os
import re
from dotenv import load_dotenv

load_dotenv()
from celery import Celery
from redis.sentinel import Sentinel


def parse_sentinel_endpoint(endpoint):
    match = re.search(
        r"^(?P<prefix>sentinel\:\/\/(.+@)?).*(?P<suffix>\/service_name\:.+)$", endpoint
    )
    if match and match.group("prefix") and match.group("suffix"):
        servers = endpoint.split(",")
        for i in range(0, len(servers)):
            # Add prefix when not founded
            if not servers[i].startswith(match.group("prefix")):
                servers[i] = match.group("prefix") + servers[i]
            # Remove suffix when founded
            if servers[i].endswith(match.group("suffix")):
                servers[i] = servers[i].replace(match.group("suffix"), "")
        broker_url = ";".join(servers)
        return broker_url


def make_celery(app):
    DBAAS_SENTINEL_SERVICE_NAME = os.getenv("DBAAS_SENTINEL_SERVICE_NAME")
    # DBAAS_MONGODB_ENDPOINT = os.getenv("DBAAS_MONGODB_ENDPOINT")
    DBAAS_SENTINEL_ENDPOINT = os.getenv("DBAAS_SENTINEL_ENDPOINT")
    # url = f"sentinel://{DBAAS_SENTINEL_PASSWsimORD}@{host[0]}:{DBAAS_SENTINEL_PORT}/0;sentinel://{DBAAS_SENTINEL_PASSWORD}@{host[1]}:{DBAAS_SENTINEL_PORT}/0;sentinel://{DBAAS_SENTINEL_PASSWORD}@{host[2]}:{DBAAS_SENTINEL_PORT}/0"
    # url = f"sentinel://{host[0]}:{DBAAS_SENTINEL_PORT}/0;sentinel://{host[1]}:{DBAAS_SENTINEL_PORT}/0;sentinel://{host[2]}:{DBAAS_SENTINEL_PORT}/0"
    # sentinel = Sentinel([('sentinel1', 26379), ('sentinel2', 26379), ('sentinel3', 26379)], socket_timeout=0.1)
    # master = sentinel.master_for(DBAAS_SENTINEL_SERVICE_NAME, socket_timeout=0.1)
    # print(master.connection_pool.get_connection())
    print("tr6srcghcct")
    print(DBAAS_SENTINEL_ENDPOINT)
    print(DBAAS_SENTINEL_SERVICE_NAME)
    sentinel_urls = parse_sentinel_endpoint(DBAAS_SENTINEL_ENDPOINT)
    # sentinel_urls = "sentinel://sentinel1:26379/0"
    print(sentinel_urls)
    celery = Celery(
        app.import_name,
        broker_transport_options={
            "master_name": DBAAS_SENTINEL_SERVICE_NAME,
        },
        broker=sentinel_urls,
        # backend=sentinel_urls,
        # result_backend=sentinel_urls,
        # result_backend_transport_options={
        #     "master_name": DBAAS_SENTINEL_SERVICE_NAME,
        # },
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
        # alternative_result_backend=DBAAS_MONGODB_ENDPOINT,
        # celery_max_retries=7,
        # result_expires=0,
        # result_persistent=True,
        # MONGO_PORT="27017",
    )
    celery.conf.update(app.config)
    return celery
