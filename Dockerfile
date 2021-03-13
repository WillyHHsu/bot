ARG PYTHON_VERSION=3.8.5

FROM python:${PYTHON_VERSION}-alpine

ENV POETRY_HOME="/etc/poetry" \
    POETRY_VIRTUALENVS_CREATE="false"

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN apk update && \
    apk add --virtual .build-deps curl && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

COPY .env poetry.lock pyproject.toml main.py ./

RUN poetry install --no-dev

RUN apk del .build-deps

CMD python main.py
