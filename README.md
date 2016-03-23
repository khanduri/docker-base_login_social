

 - virtualenv virenv --no-site-packages
 - source virenv/bin/activate


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
```

 - Starting up the application server: `./run.py`
 - Have redis running: `redis-server` # make sure to have redis installed
 - Have celery running: `celery -A app.celery worker`


