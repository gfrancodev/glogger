from socket import socket, AF_INET, SOCK_DGRAM
from os import environ
from colorama import Fore
from sys import exit
from glogger.base.client import Client


class Papertrail(Client):
    def __init__(self):
        self.hostname = environ.get("HOSTNAME")
        self.papertrail_host = environ.get("PAPERTRAIL_HOST")
        self.papertrail_port = environ.get("PAPERTRAIL_PORT")

    def send(self, data):
        try:
            client = socket(AF_INET, SOCK_DGRAM)
            client.sendto(
                str(f"[{self.hostname}] {data}").encode(),
                (self.papertrail_host, self.papertrail_port),
            )
            client.close()
            print(
                f"""
            {Fore.BLUE}[PAPERTRAIL] ➡️ {data}
            """
            )
        except BaseException:
            print(
                f"""
            {Fore.RED} ❌ Failed to connect to client Papertrail.
            """
            )
            exit(1)
