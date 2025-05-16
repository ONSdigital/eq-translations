FROM python:3.12-slim

COPY . ./

RUN pip install \
    "poetry==2.1.2" && \
    poetry config virtualenvs.create false && \
    poetry install --only main

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
