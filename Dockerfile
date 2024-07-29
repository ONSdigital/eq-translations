FROM python:3.11.0-slim-buster

RUN pip install "poetry==1.8.2

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry install

COPY . /usr/src/app