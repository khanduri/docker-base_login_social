
------------------------------
# Local Dev (mac OSx):

## Setup
 - virtualenv
 - MySql (OLD: postgres)
 - celery
 - redis

 - `virtualenv --no-site-packages venv`
 - `source venv/bin/activate`
 - `pip install -r requirements.txt`
 - `brew install node`
 - `npm install`
 - `npm install -g bower`
 - `mysqld`
 - `mysql -u root -h localhost`
 - `create database base_login_social`
 - `cp _keys_template.sh keys.sh` .. and fill in the key values
    - Facebook: https://developers.facebook.com/apps
    - Twitter:
    - Sendgrid:

## Debug
 - Setup app database:
    - `python manage.py db init`
    - `python manage.py db migrate`
    - `python manage.py db upgrade`

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
    - `bower install`
    - `gulp build`
    - `source keys.sh`
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


------------------------------
# Local Testing - Docker:

## Setup
 - Make sure to have docker installed

## Build
 - `docker build -t docker-khanduri .`
 - `docker run -d --name khanduri-01 -p 5000:5000 docker-khanduri`



# Random notes (you should not need to read the following)
The following section is what I have to cleanup

export PYTHONPATH=/Users/prashantkhanduri/projects/flask/base_login_social




------------------------------
# Stage Push - Docker - Heroku:

## Setup
 - `heroku login`
 - `heroku plugins:install heroku-container-registry`
 - `heroku container:login`
 - `heroku apps:create khanduri-staging --remote staging`

## Build
 - `heroku container:push web --remote staging`
 - `heroku open`


------------------------------
# PROD Push - Docker - Heroku:

## Setup
 - `heroku apps:create khanduri --remote heroku-khanduri`

## Build
 - `heroku container:push web --remote heroku-khanduri`
 - `heroku logs --remote heroku-khanduri`


------------------------------
# PROD Push - Docker - AWS:

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


------------------------------
# DEBUGGING tips:

## TODO (clean these up):
 - `docker images`
 - `docker rmi $(docker images | grep "<none>" | awk '{print $3}')`
 - `docker exec -ti khanduri-01 bash`
 - `lsof -i tcp:8000`
 - `rm -rf /Users/prashantkhanduri/Library/Containers/com.docker.docker/Data/*`
 - `docker logs khanduri-01`
 - `docker exec -ti khanduri-01 bash`

 - `git clone https://github.com/khanduri/base_login_social.git docker-base_login_social`
 - `virtualenv --no-site-packages venv`
 - `source venv/bin/activate`
 - `pip install -r requirements.txt`
 - `npm install`
 - `docker-compose build`
 - `docker-compose up -d`
 - `docker commit dockerbaseloginsocial_web_1 mysnapshot`
 - `docker run -t -i mysnapshot /bin/bash`

 - `docker stop $(docker ps -a -q)`
 - `docker rm $(docker ps -a -q)`
 - `docker-compose up -d`
 - `docker-compose build`
 - `docker-compose exec database mysql -u root -p`
 - `docker-compose run web /usr/local/bin/python manage.py db upgrade`
 - `docker-compose run web /usr/local/bin/python manage.py db migrate`
 - `cp .env_template .env`
