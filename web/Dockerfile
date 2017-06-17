FROM python:2.7

RUN apt-get update -y
RUN apt-get install nodejs-legacy npm -y

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

ADD package.json /tmp
RUN cd /tmp && npm install
RUN mkdir -p /code && cp -a /tmp/node_modules /code

COPY . /code
WORKDIR /code

RUN node_modules/gulp/bin/gulp.js build
