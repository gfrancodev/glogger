from os import environ
from colorama import Fore
from sys import exit
from google.cloud import storage
from glogger.base.client import Client


class GCS(Client):
    def __init__(self):
        self.project_id = environ.get("GCP_PROJECT_ID")
        self.bucket_name = environ.get("GCP_BUCKET_NAME")
        self.blob_name = environ.get("GCP_OBJECT_KEY")

    def send(self, data):
        try:
            client = storage.Client(project=self.project_id)
            bucket = client.get_bucket(self.bucket_name)
            blob = bucket.blob(self.blob_name)

            current_content = blob.download_as_text() if blob.exists() else ""
            new_content = current_content + "\n" + data

            blob.upload_from_string(new_content)

            print(
                f"""
            {Fore.BLUE}[GCP_STORAGE] ➡️ {data}
            """
            )
        except BaseException:
            print(
                f"""
            {Fore.RED} ❌ Failed to connect to client Google Cloud Storage.
            """
            )
            exit(1)
