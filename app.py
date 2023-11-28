import os

from flask import Flask
from flask_apscheduler import APScheduler
from flask_login import LoginManager

from tts_app import frontend, voice_api, auth, admin
from utils.phrases_dict import phrases_dict_init
from utils.data_utils import clean_folder

from utils.config_manager import global_config

app_path = os.path.dirname(__file__)

app = Flask(
    __name__,
    template_folder=os.path.join(app_path, 'tts_app', 'templates'),
    static_folder=os.path.join(app_path, 'tts_app', 'static')
)

app.config.update(global_config)
phrases_dict_init(app.config['ABS_PATH'])

app.register_blueprint(frontend, url_prefix='/')
app.register_blueprint(voice_api, url_prefix='/voice')

if app.config.get("IS_ADMIN_ENABLED", False):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        users = app.config["users"]["admin"]
        for user in users.values():
            if user.get_id() == user_id:
                return user
        return None

    app.register_blueprint(auth, url_prefix=app.config.get("ADMIN_ROUTE", "/admin"))
    app.register_blueprint(admin, url_prefix=app.config.get("ADMIN_ROUTE", "/admin"))

if app.config.get("CLEAN_INTERVAL_SECONDS", 6000) > 0:
    scheduler = APScheduler()
    scheduler.init_app(app)

    scheduler.start()

@scheduler.task('interval', id='clean_task', seconds=app.config.get("CLEAN_INTERVAL_SECONDS", 6000), misfire_grace_time=1000)

def clean_task():
    clean_folder(app.config["UPLOAD_FOLDER"])
    clean_folder(app.config["CACHE_PATH"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config.get("PORT", 8888), debug=app.config.get("DEBUG", False))
