from os import environ
from colorama import Fore
from sys import exit
from azure.storage.blob import BlobServiceClient
from glogger.base.client import Client


class AzureBlob(Client):
    def __init__(self):
        self.connection_string = environ["AZURE_STORAGE_CONNECTION_STRING"]
        self.container_name = environ.get("AZURE_CONTAINER_NAME")
        self.blob_name = environ.get("AZURE_BLOB_NAME")

    def send(self, data):
        try:
            client = BlobServiceClient.from_connection_string(
                str(self.connection_string)
            )
            container_client = client.get_container_client(self.container_name)
            blob_client = container_client.get_blob_client(self.blob_name)

            current_content = (
                blob_client.download_blob().readall()
                if blob_client.exists()
                else b""
            )
            new_content = current_content + b"\n" + data.encode("utf-8")

            blob_client.upload_blob(new_content, overwrite=True)

            print(
                f"""
            {Fore.BLUE}[AZURE_BLOB] ➡️ {data}
            """
            )
        except BaseException:
            print(
                f"""
            {Fore.RED} ❌ Failed to connect to client Azure Blob Storage.
            """
            )
            exit(1)
