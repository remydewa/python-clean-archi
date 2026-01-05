FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y libpq-dev gcc

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VENV=/opt/poetry-venv \
    POETRY_CACHE_DIR=/home/pyenv/tmp/poetry_cache

RUN python3 -m venv $POETRY_VENV && \
    $POETRY_VENV/bin/pip install --upgrade pip && \
    $POETRY_VENV/bin/pip install poetry==2.2.1

ENV PATH="${PATH}:${POETRY_VENV}/bin"
RUN mkdir -p /tmp /app

COPY ./users/pyproject.toml /app
COPY ./users/poetry.lock /app
COPY ./users/README.md /app
COPY ./users/app /app/app
COPY ./users/entrypoint.sh /app

RUN cd /app && poetry install && rm -rf $POETRY_CACHE_DIR
RUN chmod +x /app/entrypoint.sh

RUN chown -R nobody:nogroup /app
WORKDIR /app
USER nobody

ENTRYPOINT [ "/app/entrypoint.sh" ]
