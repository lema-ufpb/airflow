FROM apache/airflow:3.1.3-python3.13

ARG VERSION
ENV PYTHONPATH="/opt/airflow/dags"
ENV VERSION=$VERSION \
    PYTHONPATH="${PYTHONPATH}" \
    JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64/ \
    POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=2.2.1 \
    PATH="/opt/poetry/bin:$PATH" \
    POETRY_VIRTUALENVS_CREATE=false

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    unzip \
    openjdk-17-jdk \
    gcc \
    wget \
    build-essential \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY plugins /opt/airflow/plugins

COPY --chown=airflow:root pyproject.toml poetry.lock ./

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN poetry install --no-root --only main

USER airflow
