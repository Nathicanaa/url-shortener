FROM python:3.11.2-slim-buster as builder

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get -y install curl
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local python3 - && \
    poetry config virtualenvs.in-project true

COPY poetry.lock pyproject.toml ./
RUN poetry install --only main --no-interaction  --no-ansi --no-root


FROM python:3.11.2-slim-buster

ENV PYTHONPATH=/opt/url-shortener PATH="/opt/url-shortener/.venv/bin:$PATH"
WORKDIR $PYTHONPATH

COPY --from=builder .venv/ .venv/
COPY alembic.ini ./
COPY alembic alembic
COPY src src
ARG PORT
EXPOSE $PORT
CMD python -m alembic upgrade head && python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT
