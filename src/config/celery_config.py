from celery import Celery
from celery.schedules import crontab
import os
import dotenv
dotenv.load_dotenv()

url_redis = os.getenv("DBAAS_REDIS_HOST")
app = Celery("Worker-compra-venda-ativos")
app.config_from_object(
    {
        "broker_url": url_redis,  # Configuração do Redis
        "result_backend": url_redis,  # Configuração do backend de resultados, caso queira armazená-los
        "accept_content": ["json"],  # Tipo de dados aceitos para tarefas
        "task_serializer": "json",  # Serialização de tarefas
        "result_serializer": "json",  # Serialização de resultados
        "timezone": "UTC",  # Definir timezone para as tarefas
        "enable_utc": True,  # Habilitar UTC]
        "beat_schedule": {
            "Executa tarefa cada 3 minutos": {
                "task": "src.tasks.assets.start",
                "schedule": crontab(),
            }
        },
        "include": ["src.tasks.assets"],
    }
)
