from src.tasks.assets import  start

def init(flask_app):
    @flask_app.route("/start")
    def index():
        start.apply_async()
        return {"status": "iniciado"}