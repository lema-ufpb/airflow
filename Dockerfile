# --------------------------------------------------------------------------
# Python version must be the same of bitnami/spark:version
# Pyspark version must be the same of bitnami/spark:version
# First check python and pyspark version in bitnami/spark:version images
# Spark > 3.4 should not compatible with spark mongodb connector 
# Current version supports
# python 3.11, java 17, pyspark 3.5.5 compatible with bitnami/spark:3.5.5
# --------------------------------------------------------------------------
FROM apache/airflow:3.0.3-python3.11

ARG VERSION
ENV VERSION=$VERSION
ENV PYTHONPATH=/opt/airflow/dags
ENV PYTHONPATH="/opt/airflow/dags:${PYTHONPATH}"

USER root

RUN apt-get update && apt-get -y install --no-install-recommends unzip openjdk-17-jdk gcc wget p7zip-full build-essential python3-dev \
    && rm -rf /var/lib/apt/lists/* && apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64/
RUN export JAVA_HOME 

COPY plugins /opt/airflow/plugins

USER airflow

COPY ./requirements.txt /opt/airflow/requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install  --no-cache-dir -r /opt/airflow/requirements.txt
