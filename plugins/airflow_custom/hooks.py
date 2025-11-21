from typing import Optional
import boto3
from botocore import UNSIGNED
from botocore.config import Config
from airflow.sdk import Connection


class S3Hook:
    def __init__(
        self,
        aws_conn_id: str = "aws_default",
        aws_endpoint: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        region_name: Optional[str] = None,
        use_unsigned: Optional[bool] = None,
    ):
        self.aws_conn_id = aws_conn_id
        self.aws_endpoint = aws_endpoint
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.use_unsigned = use_unsigned

        try:
            self.conn = Connection.get_connection_from_secrets(aws_conn_id)
            self.extras = self.conn.extra_dejson
        except Exception:
            self.conn = None
            self.extras = {}

        self.s3 = self._create_client()

    def _create_client(self):
        host = self.aws_endpoint or self.extras.get(
            "host") or "https://s3.lema.ufpb.br"
        region = self.region_name or self.extras.get(
            "region_name") or "us-east-1"

        if self.use_unsigned is not None:
            use_unsigned = self.use_unsigned
        else:
            use_unsigned = self.extras.get("use_unsigned_session", False)

        # Credentials
        access_key = self.aws_access_key_id or (
            self.conn.login if self.conn else None)
        secret_key = self.aws_secret_access_key or (
            self.conn.password if self.conn else None)

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
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )

    def __getattr__(self, name):
        """
        Permite acessar métodos do client boto3 diretamente:
        s3 = S3Hook(); s3.list_buckets()
        """
        return getattr(self.s3, name)
