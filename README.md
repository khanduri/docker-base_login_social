
Dependencies:
 - virtualenv
 - MySql (OLD: postgres)
 - celery
 - redis
 - node

------------------------------
# Local Dev (mac OSx):

## Setup
 - `virtualenv --no-site-packages venv`
 - `source venv/bin/activate`
 - `pip install -r requirements.txt`
 - `npm install`
 - `npm install -g bower`
 - `mysql -u root -h localhost`  # to login to the mysql shell
   - `create database base_login_social`
 - `cp _env_template .env_local` .. and fill in the key values
    - Facebook: https://developers.facebook.com/apps
    - Twitter:
    - Sendgrid:
    - db info
    - redis info

## Debug
 - Setup app database:
    - `python manage.py db init`
    - `python manage.py db migrate`
    - `python manage.py db upgrade`

## Running the service:
 - [Shell 0] `mysqld`
 - [Shell 1] `redis-server`
 - [Shell 2] Start Celery up:
    - `source virenv/bin/activate`
    - `cd code`
    - `export $(cat .env_local | grep -v ^# | xargs)`
    - `celery -A app.celery worker`
 - [Shell 3] Starting up the application server:
    - `source virenv/bin/activate`
    - `bower install`
    - `gulp build`
    - `export $(cat .env_local | grep -v ^# | xargs)`
    - `python run.py`

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


## DEPRECATED
 - Setting up the database: POSTGRES
     - open up postgres cmd shell
        - Log into the shell by `psql -p5432` running in localhost
        - You will have to create a database if you're connecting/ setting up for the first time
            - `CREATE DATABASE base_login_social_db;`
        - Helpful commands
            - \l: list all databases
            - \c: connect to the data base
           - \dt: list all tables under the connected database



------------------------------
# Local Testing - Docker:

## Setup
 - Make sure to have docker installed

## Build
 - `docker-compose build`
 - `docker-compose up -d`
 - `docker-compose down`
 - `docker-compose run web /usr/local/bin/python manage.py db upgrade`
 - `docker-compose run web /usr/local/bin/python manage.py db migrate`

## Handy debugging
 - `docker stop $(docker ps -a -q)`
 - `docker rm $(docker ps -a -q)`
 - `docker-compose exec database mysql -u root -p`
 - `docker commit dockerbaseloginsocial_web_1 mysnapshot`
 - `docker run -t -i mysnapshot /bin/bash`






------------------------------
# UNTESTED : Stage Push - Docker - Heroku:

## Setup
 - `heroku login`
 - `heroku plugins:install heroku-container-registry`
 - `heroku container:login`
 - `heroku apps:create khanduri-staging --remote staging`

## Build
 - `heroku container:push web --remote staging`
 - `heroku open`


------------------------------
#  UNTESTED : PROD Push - Docker - Heroku:

## Setup
 - `heroku apps:create khanduri --remote heroku-khanduri`

## Build
 - `heroku container:push web --remote heroku-khanduri`
 - `heroku logs --remote heroku-khanduri`


------------------------------
#  UNTESTED : PROD Push - Docker - AWS:

## Setup
 - `pip install awsebcli`
 - `eb init`
 - `vim .elasticbeanstalk/config.yml`
 - `eb console`
 - `eb create`

## Build
 - `eb deploy`
 - `eb open`
 - `eb ssh`
 - `gunicorn --bind 0.0.0.0:5000 wsgi`


------------------------------------
## TODO (clean these up .. you should not need to read the following):

The following section is what I have to cleanup
export PYTHONPATH=/Users/prashantkhanduri/projects/flask/base_login_social
