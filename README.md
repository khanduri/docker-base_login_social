
# How to clone this repo for a new project:

## Prerequisites:
 - virtualenv
 - postgres
 - celery
 - redis

## Setting up the environment:
 - virtualenv virenv --no-site-packages
     - source virenv/bin/activate
     - pip install -R requirements.txt
 - create the keys.sh file

## Setting up the database:
 - open up postgres cmd shell
    - I used postgres and installed the postgres client
    - I can log into the shell by `psql -p5432` running in localhost
    - You will have to create a database if you're connecting/ setting up for the first time
        - `CREATE DATABASE base_login_social_db;`
    - Helpful commands
        - \l: list all databases
        - \c: connect to the data base
        - \dt: list all tables under the connected database
 - Setup postgres:
    - python manage.py db init
    - python manage.py db migrate
    - python manage.py db upgrade

## Running the service:
 - [Shell 1] Start redis server up:
    - redis-server
 - [Shell 2] Start Celery up:
    - cd into the repo location
    - source virenv/bin/activate
    - source keys.sh
    - celery -A app.celery worker
 - [Shell 3] Starting up the application server:
    - cd into the repo location
    - source virenv/bin/activate
    - source keys.sh
    - `./run.py`
    - STOP after visiting the index page .. we needs to setup a few service dependencies

## Services to register for:
 - Facebook
 - Twitter
 - Sendgrid


## Page references:
    - index:
        - http://localhost:5454/
    - admin:
        - http://localhost:5454/admin/
        - User with id == 1 will be an admin. You should change that logic soon :)
    - trigger an email:
        - http://localhost:5454/send_email
    - template email:
        - http://localhost:5454/email/template/email_verify


## Cleanup to add in your custom logic
    - Places to add in your company log
    - Code to delete



# Random notes (you should not need to read the following)
The following section is what I have to cleanup
 - source keys.sh
```
export SECRET_KEY='secretykey'


export OAUTH_CREDENTIALS_FB_ID=''
export OAUTH_CREDENTIALS_FB_SECRET=''

export OAUTH_CREDENTIALS_TW_ID=''
export OAUTH_CREDENTIALS_TW_SECRET=''


export SENDGRID_USER=''
export SENDGRID_API_KEY=''


export HASHIDS_SALT='hasheykey'


export SERVER_NAME='localhost:5454'
```

npm init
npm install
export PYTHONPATH=/Users/prashantkhanduri/projects/flask/base_login_social