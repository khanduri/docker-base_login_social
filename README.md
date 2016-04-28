
 - virtualenv virenv --no-site-packages
     - source virenv/bin/activate
 - open up postgres cmd shell
   - create db
   - \l: list all databases
   - \c: connect to the data base
   - \dt: list all tables under the connected database
 - Setup postgres:
    - python manage.py db init
    - python manage.py db upgrade
    - python manage.py db migrate
 - Start Celery up:
    - celery -A app.celery worker
 - Start redis server up:
    - redis-server


 - Starting up the application server: `./run.py`
 - Have redis running: `redis-server` # make sure to have redis installed
 - Have celery running: `celery -A app.celery worker`



Dev Setup:
----

TODO: Initial install and setup for pip

 - source keys.sh
```
export SECRET_KEY='secret key'


export OAUTH_CREDENTIALS_FB_ID=''
export OAUTH_CREDENTIALS_FB_SECRET=''

export OAUTH_CREDENTIALS_TW_ID=''
export OAUTH_CREDENTIALS_TW_SECRET=''


export SENDGRID_USER=''
export SENDGRID_API_KEY=''


export HASHIDS_SALT=''
export SERVER_NAME=''
```

npm init
npm install
