FROM python:3.8.13-alpine3.16

ENV PYTHONUNBUFFERED=1 POETRY_VERSION=1.5.1

RUN apk add --no-cache build-base libffi-dev musl-dev postgresql-dev
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /app

CMD gunicorn --bind :8080 simple_api.wsgi