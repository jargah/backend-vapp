import os
from typing import Optional, Union, Dict, Any
import boto3
from botocore.exceptions import BotoCoreError, ClientError


class AwsStorage:
    def __init__(
        self,
        region: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
    ) -> None:
        region = region or os.getenv("AWS_REGION")
        access_key = access_key or os.getenv("AWS_ACCESS_KEY")
        secret_key = secret_key or os.getenv("AWS_SECRET_KEY")

        self._region = region
        self._s3 = boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )


    def create_bucket(self, bucket: str) -> bool:

        try:
            if self._region and self._region != "us-east-1":
                self._s3.create_bucket(
                    Bucket=bucket,
                    CreateBucketConfiguration={"LocationConstraint": self._region},
                )
            else:
                self._s3.create_bucket(Bucket=bucket)
            return True
        except (BotoCoreError, ClientError) as e:
            print(e)
            return False

    def list_bucket(self, bucket: str, prefix: Optional[str] = None) -> Optional[Dict[str, Any]]:

        try:
            params = {"Bucket": bucket}
            if prefix:
                params["Prefix"] = prefix
            resp = self._s3.list_objects_v2(**params)
            return resp
        except (BotoCoreError, ClientError) as e:
            print(e)
            return None

    # ---------- Objetos ----------

    def upload_file(self, bucket: str, key: str, body: Union[bytes, str, 'IO[bytes]']) -> bool:

        try:
            data = body.encode("utf-8") if isinstance(body, str) else body
            self._s3.put_object(Bucket=bucket, Key=key, Body=data)
            return True
        except (BotoCoreError, ClientError) as e:
            print(e)
            return False

    def download_file(self, bucket: str, key: str, as_text: bool = True, encoding: str = "utf-8"):

        try:
            obj = self._s3.get_object(Bucket=bucket, Key=key)
            raw = obj["Body"].read()
            return raw.decode(encoding) if as_text else raw
        except (BotoCoreError, ClientError) as e:
            print(e)
            return None

    def generate_url(self, bucket: str, key: str, expires_in: int = 1800) -> Optional[str]:

        try:
            url = self._s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=expires_in,
            )
            return url
        except (BotoCoreError, ClientError) as e:
            print(e)
            return None
