# Apache Airflow

This project build an Apache Airflow Docker Image for many projects of LEMA-UFPB research lab. It is based on the official Airflow Docker image and includes additional features and configurations.

## 📋 Overview

This custom Airflow implementation provides a containerized environment for orchestrating data pipelines and workflows at LEMA-UFPB research laboratory.

## Features

- Built on official Apache Airflow Docker image
- Custom configurations for LEMA-UFPB specific needs
- Containerized deployment ready
- Simplified setup process

## 🛠️ Prerequisites

- Docker

## 🚀 Usage

```bash
docker build -t airflow-test .
docker compose up -d
```

## 🚀 Deployment

```bash
git push origin main
git tag v3.0.2-python3.11-spark3.5.5
git push --tags
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## 📞 Support

For support and questions, please contact LEMA-UFPB research lab.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- [Hilton Ramalho](https://github.com/hiltonmbr) for the initial implementation.
