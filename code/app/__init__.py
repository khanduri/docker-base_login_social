from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from celery import Celery
from sendgrid import SendGridClient
from flask_admin import Admin
from hashids import Hashids
import logging


app = Flask(__name__, static_folder='../static')
app.config.from_object('config')


@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)


def make_celery(flask_app):
    celery = Celery(flask_app.import_name,
                    backend=flask_app.config['CELERY_RESULT_BACKEND'],
                    broker=flask_app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            # with app.app_context():
            with app.test_request_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index_page'

sg = SendGridClient(app.config['SENDGRID_USER'], app.config['SENDGRID_API_KEY'])

hashids = Hashids(salt=app.config.get('HASHIDS_SALT'), min_length=8)


from app import views, tables, admins, apis  # noqa: E402,F401


class LockedModelView(admins.AdminAccessModelView):
    can_delete = False


class EditableModelView(admins.AdminAccessModelView):
    page_size = 50


admin = Admin(app, name='Admin Home', template_mode='bootstrap3', index_view=admins.AdminAccessIndexView())
admin.add_view(LockedModelView(tables.User, db.session))
admin.add_view(LockedModelView(tables.UserSocial, db.session))
admin.add_view(EditableModelView(tables.Contact, db.session))
