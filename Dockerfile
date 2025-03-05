# --------------------------------------------------------------------------
# Python version must be the same of bitnami/spark:version
# Pyspark version must be the same of bitnami/spark:version
# First check python and pyspark version in bitnami/spark:version images
# Spark > 3.4 should not compatible with spark mongodb connector 
# Current version supports
# python 3.11, java 17, pyspark 3.4.2 compatible with bitnami/spark:3.4
# --------------------------------------------------------------------------
FROM apache/airflow:slim-2.10.5-python3.11

USER root

# Add packages dependencies
RUN apt-get update && apt-get -y install unzip openjdk-17-jdk gcc wget p7zip-full \
    && rm -rf /var/lib/apt/lists/* && apt-get clean

# Add Spark
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64/
RUN export JAVA_HOME 

# Add Python packages
USER airflow

COPY ./requirements.txt /home/airflow/requirements.txt
RUN pip install  --no-cache-dir --trusted-host pypi.python.org  -r /home/airflow/requirements.txt
