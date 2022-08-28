FROM python:3.8.13-alpine3.16

ENV PYTHONUNBUFFERED=1 POETRY_VERSION=1.1.15

RUN apk add --no-cache build-base libffi-dev musl-dev postgresql-dev
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /app

CMD gunicorn --bind :$PORT simple_api.wsgi