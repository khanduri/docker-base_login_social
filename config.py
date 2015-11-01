import os
basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'app.db'))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'seekrey -- keaze')


BOOTSWATCH_TEMPLATE_LIST = ["paper", "sandstone", "cosmo", "darkly", "yeti", "slate", "superhero"]
BOOTSWATCH_TEMPLATE = BOOTSWATCH_TEMPLATE_LIST[6]


OAUTH_CREDENTIALS = {
    'facebook': {
        'id': os.environ.get('OAUTH_CREDENTIALS_FB_ID'),
        'secret': os.environ.get('OAUTH_CREDENTIALS_FB_SECRET'),
    },
    'twitter': {
        'id': os.environ.get('OAUTH_CREDENTIALS_TW_ID'),
        'secret': os.environ.get('OAUTH_CREDENTIALS_TW_SECRET'),
    },
}


CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')


SENDGRID_USER = os.environ['SENDGRID_USER']
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']

HASHIDS_SALT = os.environ['HASHIDS_SALT']