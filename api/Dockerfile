FROM python:3.12-slim

RUN apt-get update 
RUN apt-get install -y unzip gcc python3-dev software-properties-common python3-launchpadlib g++
RUN add-apt-repository ppa:ubuntugis/ppa
RUN apt-get update
RUN apt-get install -y gdal-bin libgdal-dev

ARG ENVIRONMENT

ENV ENVIRONMENT=${ENVIRONMENT} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.7.1 \
  GDAL_CONFIG=/usr/bin/gdal-config


RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

COPY ./pyproject.toml /code/pyproject.toml
COPY ./poetry.lock /code/poetry.lock

WORKDIR /code

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$ENVIRONMENT" == "production" && echo "--no-dev") --no-interaction --no-ansi --

# Conditionally copy the tests folder only if ENVIRONMENT is "test"
COPY ./app /code/app
COPY ./tests /code/tests
RUN touch /code/.env

COPY entrypoint.sh /code/entrypoint.sh

ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]
