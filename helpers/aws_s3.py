import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError


class S3Utils:
    def __init__(self, aws_access_key, aws_secret_key, region_name="us-east-1"):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )

    def list_files(self, bucket_name, prefix=""):
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            if "Contents" in response:
                return [obj["Key"] for obj in response["Contents"]]
            else:
                return []
        except ClientError as e:
            print(f"❌ Error al listar archivos: {e}")
            return []

    def upload_file(self, file_name, bucket_name, object_name=None):
        if object_name is None:
            object_name = os.path.basename(file_name)
        try:
            self.s3.upload_file(file_name, bucket_name, object_name)
            print(f"✅ Subido: {file_name} → s3://{bucket_name}/{object_name}")
        except FileNotFoundError:
            print("❌ El archivo no existe.")
        except NoCredentialsError:
            print("❌ Credenciales no encontradas.")

    def download_file(self, bucket_name, object_name, file_name=None):
        if file_name is None:
            file_name = os.path.basename(object_name)
        try:
            self.s3.download_file(bucket_name, object_name, file_name)
            print(f"✅ Descargado: s3://{bucket_name}/{object_name} → {file_name}")
        except ClientError as e:
            print(f"❌ Error al descargar archivo: {e}")

    def delete_file(self, bucket_name, object_name):
        try:
            self.s3.delete_object(Bucket=bucket_name, Key=object_name)
            print(f"🗑️ Eliminado: s3://{bucket_name}/{object_name}")
        except ClientError as e:
            print(f"❌ Error al eliminar archivo: {e}")

    def sync_folder(self, folder_path, bucket_name, prefix=""):
        for root, _, files in os.walk(folder_path):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, folder_path)
                s3_path = os.path.join(prefix, relative_path).replace("\\", "/")
                self.upload_file(local_path, bucket_name, s3_path)
