import os
basedir = os.path.abspath(os.path.dirname(__file__))
dirname = os.path.split(os.path.dirname(__file__))[-1]
local_db = 'postgresql://localhost/{0}_db'.format(dirname)


SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', local_db)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'seekrey -- keaze')


BOOTSWATCH_TEMPLATE_LIST = [
    "paper", "sandstone", "cosmo",
    "darkly", "yeti", "slate",
    "superhero", "cerulean", "united",
    "spacelab", "simplex", "lumen",
    "flatly", "journal", "cyborg",
]
# import random
# BOOTSWATCH_TEMPLATE = BOOTSWATCH_TEMPLATE_LIST[random.randint(0, len(BOOTSWATCH_TEMPLATE_LIST) - 1)]
BOOTSWATCH_TEMPLATE = BOOTSWATCH_TEMPLATE_LIST[8]


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

SERVER_NAME = os.environ['SERVER_NAME']


# Print the setup
output_strings = [
    'LOCAL DB setup in: {0}'.format(local_db),
    BOOTSWATCH_TEMPLATE,
    SERVER_NAME,
]

for output_string in output_strings:
    print output_string
