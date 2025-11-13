# 🌊 Apache Airflow - LEMA-UFPB

This project builds a custom Apache Airflow Docker Image for various projects at LEMA-UFPB research lab. It is based on the official Airflow Docker image and includes additional features and configurations tailored for data pipeline orchestration.

## 📋 Overview

This custom Airflow implementation provides a containerized environment for orchestrating data pipelines and workflows at LEMA-UFPB research laboratory. It enables scheduling, monitoring, and managing complex data workflows with ease.

## ✨ Features

- 🐳 Built on official Apache Airflow 3.1.2 Docker image
- 🐍 Python 3.13 support
- 📦 Poetry for dependency management
- ☕ Java 17 (OpenJDK) for Spark integration
- 🔧 Custom configurations for LEMA-UFPB specific needs
- 🚀 Production-ready containerized deployment
- 📊 Web-based UI for workflow monitoring
- 🔌 Extensible with custom plugins

## 🛠️ Prerequisites

- Docker
- Docker Compose
- At least 4GB of RAM available for Docker


## 🚀 Quick Start

### Initial Setup

```bash
# Build the image
docker build -t airflow-test .

# Start all services
docker compose up -d

# Check service status
docker compose ps
```

### Accessing Airflow

Once the services are running, access the Airflow Web UI:

- **URL**: http://localhost:8080
- **Default Username**: `airflow`
- **Default Password**: `airflow`

### Managing the Environment

```bash
# View logs
docker compose logs -f

# Stop all services
docker compose down

# Stop and remove volumes (clean slate)
docker compose down -v

# Restart services
docker compose restart
```

## 📝 Managing Dependencies with Poetry

This project uses Poetry for Python dependency management. Dependencies are defined in `pyproject.toml`.

### Adding New Dependencies

```bash
# Add a new package
poetry add pandas

# Add a development dependency
poetry add --group dev pytest

# Update lock file
poetry lock

# Rebuild the Docker image
docker build -t airflow-test .
docker compose up -d --force-recreate
```


## 🏗️ Dockerfile Configuration

The Dockerfile includes:

- **Base Image**: `apache/airflow`
- **Java 17**: OpenJDK for Spark integration
- **Poetry 2.2.1**: Dependency management
- **Custom Plugins**: Mounted from `plugins/` directory
- **Environment Variables**:
  - `PYTHONPATH=/opt/airflow/dags`
  - `JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64/`
  - `POETRY_VIRTUALENVS_CREATE=false`


## 🚀 Deployment and Versioning

```bash
# Commit your changes
git add .
git commit -m "feat: description of change"

# Push to repository
git push origin main

# Create and publish version tag
git tag v3.1.2-python3.13
git push --tags
```

### 📌 Versioning Convention

We follow the pattern: `vX.Y.Z-pythonA.B`

- `X.Y.Z`: Airflow version
- `A.B`: Python version

Example: `v3.1.2-python3.13`

## 🤝 Contributing

Contributions are welcome! Follow these steps:

1. 🍴 Fork the repository
2. 🌿 Create your feature branch (`git checkout -b feature/MyFeature`)
3. 💾 Commit your changes (`git commit -m 'feat: Add MyFeature'`)
4. 📤 Push to the branch (`git push origin feature/MyFeature`)
5. 🔀 Open a Pull Request

### 📋 Commit Pattern

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `chore:` Maintenance tasks
- `refactor:` Code refactoring
- `perf:` Performance improvements

## 📚 Useful Commands

```bash
# List all DAGs
docker compose exec airflow-webserver airflow dags list

# Trigger a DAG manually
docker compose exec airflow-webserver airflow dags trigger <dag_id>

# Test a specific task
docker compose exec airflow-webserver airflow tasks test <dag_id> <task_id> <date>

# Access Airflow CLI
docker compose exec airflow-webserver airflow

# Create a new admin user
docker compose exec airflow-webserver airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Check installed Poetry packages
docker compose exec airflow-webserver poetry show

# Access container shell
docker compose exec airflow-webserver bash
```

## 🔒 Security Notes

⚠️ **Important**: 
- Change default credentials in production
- Use environment variables for sensitive data
- Enable authentication and RBAC
- Keep the image updated with security patches
- Review Poetry dependencies regularly for vulnerabilities

## 📞 Support

For support and questions, contact LEMA-UFPB laboratory:

- 🌐 Website: [LEMA-UFPB](https://lema.ufpb.br)
- 💬 Issues: Use the [Issues](../../issues) tab of this repository
- 📖 Airflow Docs: [Official Documentation](https://airflow.apache.org/docs/)
- 📦 Poetry Docs: [Poetry Documentation](https://python-poetry.org/docs/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  
[![LEMA-UFPB](https://img.shields.io/badge/LEMA-UFPB-blue)](https://lema.ufpb.br)
[![Airflow](https://img.shields.io/badge/Airflow-3.1.2-017CEE?logo=apache-airflow)](https://airflow.apache.org/)
[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)](https://www.python.org/)
[![Poetry](https://img.shields.io/badge/Poetry-2.2.1-60A5FA?logo=poetry)](https://python-poetry.org/)
[![Java](https://img.shields.io/badge/Java-17-ED8B00?logo=openjdk)](https://openjdk.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com/)

</div>