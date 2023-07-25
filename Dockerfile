FROM python:3.11.0-slim-buster

RUN pip install pipenv==2023.7.23

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install

COPY . /usr/src/app