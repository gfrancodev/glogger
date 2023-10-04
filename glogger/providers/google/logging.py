from os import environ
from colorama import Fore
from sys import exit
from google.cloud import logging
from glogger.base.client import Client


class GCL(Client):
    def __init__(self):
        self.project_id = environ.get("GCP_PROJECT_ID")
        self.log_name = environ.get("GCP_LOG_NAME")

    def send(self, data):
        try:
            client = logging.Client(project=self.project_id)
            logger = client.logger(self.log_name)
            logger.log_text(data)

            print(
                f"""
            {Fore.BLUE}[GCP_LOGGING] ➡️ {data}
            """
            )
        except BaseException:
            print(
                f"""
            {Fore.RED} ❌ Failed to connect to client Google Cloud Logging.
            """
            )
            exit(1)
