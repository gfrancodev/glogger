import asyncio
from websockets.sync.client import connect
from os import environ
from colorama import Fore
from sys import exit
from glogger.base.client import Client

class Websocket(Client):
    def __init__(self):
        self.socket_uri = environ.get("WEBSOCKET_URI")

    def connect(self, data):
        try:
            with connect(self.socket_uri) as ws:
                ws.send(data)
                ws.recv()
            print(
                f"""
            {Fore.BLUE}[WEBSOCKET] ➡️ {data}
            """
            )
        except Exception as e:
            print(
                f"""
            {Fore.RED} ❌ Failed to connect to client{Fore.RESET} {Fore.MAGENTA}GLOGGER SERVER / WEBSOCKET{Fore.RESET}.
            Error: {str(e)}
            """
            )
            exit(1)
