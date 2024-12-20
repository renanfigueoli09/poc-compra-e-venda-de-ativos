from src.tasks.assets import boot

def init(flask_app):
    @flask_app.route("/start")
    def index():
        boot.apply_async()
        return {"status": "iniciado"}