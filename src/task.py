from src.config.celery_config import app


@app.task
def add():
    print("TEWSDASDSAD")
    return 'teste'