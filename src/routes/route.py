from src.tasks.assets import  start

def init(app):
    @app.route("/start")
    def index():
        start.apply_async()
        return {"status": "iniciado"}