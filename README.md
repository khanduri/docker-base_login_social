
# How to clone this repo for a new project:


## Prerequisites to install:
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
    - Log into the shell by `psql -p5432` running in localhost
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


## Services to register for:
 - `cp _keys_template.sh keys.sh`
 - Fill in the keys/tokens by signing up for the correct services
    - Facebook: https://developers.facebook.com/apps
    - Twitter:
    - Sendgrid:


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


## Page references:
    - index:
        - http://localhost:5454/
    - admin:
        - http://localhost:5454/admin/
        - User with id == 1 will be an admin. You should change that logic soon :)
    - trigger an email:
        - http://localhost:5454/send_email
    - template email:
        - http://localhost:5454/email/templates/email_verify


## Cleanup to add in your custom logic
    - Places to add in your company log
    - Code to delete



# Random notes (you should not need to read the following)
The following section is what I have to cleanup

npm init
npm install
export PYTHONPATH=/Users/prashantkhanduri/projects/flask/base_login_social