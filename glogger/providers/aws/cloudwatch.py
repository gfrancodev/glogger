from os import environ
from boto3 import client
from time import time
from colorama import Fore
from sys import exit
from glogger.base.client import Client


class CloudWatch(Client):
    def __init__(self):
        self.region = environ.get("AWS_DEFAULT_REGION")
        self.aws_access_key_id = environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = environ.get("AWS_SECRET_ACCESS_KEY")
        self.log_group_name = environ.get("AWS_CLOUDWATCH_LOG_GROUP_NAME")
        self.log_stream_name = environ.get("AWS_CLOUDWATCH_LOG_STREAM_NAME")

    def send(self, data):
        try:
            cw_client = client(
                "logs",
                region_name=self.region,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            )

            cw_client.put_log_events(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name,
                logEvents=[{"timestamp": int(time() * 1000), "message": data}],
            )

            print(
                f"""
            {Fore.BLUE}[AWS_CLOUDWATCH] ➡️ {data}
            """
            )
        except BaseException:
            print(
                f"""
            {Fore.RED} ❌ Failed to connect to client Cloudwach.
            """
            )
            exit(1)
