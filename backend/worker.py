from celery import Celery

celery_app = Celery(__name__)

def celery_init_app(app):
    class FlaskTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.config_from_object(app.config["CELERY"])
    celery_app.Task = FlaskTask
    return celery_app