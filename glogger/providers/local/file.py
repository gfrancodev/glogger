from os import environ
from colorama import Fore
from sys import exit
import logging
from glogger.base.client import Client


class FileLogger(Client):
    def __init__(self):
        log_file_path = environ.get("LOG_FILE_PATH", "glogger.log")
        logging.basicConfig(filename=log_file_path, level=logging.INFO)

    def send(self, data):
        try:
            logging.info(str(data).encode("utf-8"))
            print(
                f"""
            {Fore.BLUE}[LOCAL] ➡️ {data}
            """
            )
        except BaseException:
            print(
                f"""
            {Fore.RED} ❌ Failure to record information in the log file.
            """
            )
            exit(1)
