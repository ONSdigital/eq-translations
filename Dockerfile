FROM python:3.12-slim

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN pip install \
    "poetry==1.8.3" && \
    poetry config virtualenvs.create false && \
    poetry install --only main

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
