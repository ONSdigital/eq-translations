FROM python:3.10.0-slim-buster

RUN pip install pipenv==2022.9.24

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install

COPY . /usr/src/app