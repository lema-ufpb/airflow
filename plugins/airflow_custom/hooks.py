import boto3 #type: ignore
from botocore import UNSIGNED #type: ignore
from botocore.config import Config #type: ignore
from airflow.models.connection import Connection #type: ignore


class S3Hook:
    def __init__(self, aws_conn_id: str = "aws_default"):
        self.aws_conn_id = aws_conn_id
        self.conn = Connection.get_connection_from_secrets(aws_conn_id)
        self.extras = self.conn.extra_dejson
        self.s3 = self._create_client()

    def _create_client(self):
        host = self.extras.get("host")
        region = self.extras.get("region_name", "us-east-1")
        use_unsigned = self.extras.get("use_unsigned_session", False)

        session = boto3.session.Session()

        if use_unsigned:
            return session.client(
                "s3",
                endpoint_url=host,
                region_name=region,
                config=Config(signature_version=UNSIGNED),
            )
        else:
            return session.client(
                "s3",
                endpoint_url=host,
                region_name=region,
                aws_access_key_id=self.conn.login,
                aws_secret_access_key=self.conn.password,
            )

    def __getattr__(self, name):
        """
        Permite acessar métodos do client boto3 diretamente:
        s3 = S3Hook(); s3.list_buckets()
        """
        return getattr(self.s3, name)
