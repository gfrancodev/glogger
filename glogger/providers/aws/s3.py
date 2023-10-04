from os import environ
from boto3 import client
from glogger.base.client import Client
from colorama import Fore
from sys import exit


class S3(Client):
    def __init__(self):
        self.region = environ.get("AWS_DEFAULT_REGION")
        self.aws_access_key_id = environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = environ.get("AWS_SECRET_ACCESS_KEY")
        self.aws_bucket_name = environ.get("AWS_BUCKET_NAME")
        self.aws_object_key = environ.get("AWS_OBJECT_KEY")
        self.client = self._initialize_client()

    def _initialize_client(self):
        return client(
            "s3",
            region_name=self.region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    def _object_exists(self):
        try:
            self.client.head_object(
                Bucket=self.aws_bucket_name, Key=self.aws_object_key
            )
            return True
        except self.client.exceptions.ClientError:
            return False

    def send(self, data):
        try:
            if not self._object_exists():
                self.client.put_object(
                    Bucket=self.aws_bucket_name,
                    Key=self.aws_object_key,
                    Body="glogger initialize",
                )

            response = self.client.get_object(
                Bucket=self.aws_bucket_name, Key=self.aws_object_key
            )
            current_content = response["Body"].read().decode("utf-8")
            new_content = current_content + "\n" + data

            self.client.put_object(
                Bucket=self.aws_bucket_name,
                Key=self.aws_object_key,
                Body=new_content,
            )
            print(
                f"""
            {Fore.BLUE}[AWS_S3] ➡️ {data}
            """
            )
        except BaseException:
            print(
                f"""
            {Fore.RED} ❌ Failed to connect to client S3.
            """
            )
            exit(1)
