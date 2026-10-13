FROM python:3.13-slim

LABEL org.opencontainers.image.source=https://github.com/WinterFramework/winter-getting-started

ENV PYTHONUNBUFFERED=1 POETRY_VERSION=2.5.1
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install --only main --no-interaction --no-ansi

COPY . /app

CMD ["gunicorn", "--bind", ":8080", "simple_api.wsgi"]
