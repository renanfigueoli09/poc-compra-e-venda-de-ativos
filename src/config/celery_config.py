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
    DBAAS_SENTINEL_HOSTS = os.getenv("DBAAS_SENTINEL_HOSTS")
    DBAAS_SENTINEL_PORT = os.getenv("DBAAS_SENTINEL_PORT")
    DBAAS_SENTINEL_ENDPOINT = os.getenv("DBAAS_SENTINEL_ENDPOINT")
    DBAAS_SENTINEL_PASSWORD = os.getenv("DBAAS_SENTINEL_PASSWORD")
    print("tr6srcghcct")
    print(DBAAS_SENTINEL_ENDPOINT)
    sentinel_hosts_list = [
        (host, DBAAS_SENTINEL_PORT) for host in DBAAS_SENTINEL_HOSTS.split(",")
    ]
    sentinel = Sentinel(
        sentinels=sentinel_hosts_list,
        socket_timeout=0.1,
        password=DBAAS_SENTINEL_PASSWORD,
    )
    master = sentinel.discover_master("mymaster")
    sentinel_urls = f"redis://{master[0]}:{master[1]}/0"
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

    # celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
