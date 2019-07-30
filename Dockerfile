FROM python:3.7-alpine

RUN pip install pipenv==2018.11.26

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install

COPY . /usr/src/app