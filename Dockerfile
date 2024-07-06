FROM python:3.10-alpine3.20

RUN apk add --no-cache build-base libffi-dev musl-dev postgresql-dev

ENV PYTHONUNBUFFERED=1 POETRY_VERSION=1.8.3
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /app

CMD gunicorn --bind :8080 simple_api.wsgi