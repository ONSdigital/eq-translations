FROM python:3.11.0-slim-buster

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN pip install "poetry==1.8.3" && \
    poetry config virtualenvs.create false && \
    poetry install

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
