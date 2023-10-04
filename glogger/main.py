#!/usr/bin/env python
from sys import argv, exit
from os import path, environ
from subprocess import Popen, PIPE, STDOUT
from threading import Thread, enumerate, current_thread
from glogger.base.logger import Logger
from glogger.base.client import Client
from glogger.config.environment import Environment
from glogger.providers.aws.cloudwatch import CloudWatch
from glogger.providers.aws.s3 import S3
from glogger.providers.google.logging import GCL
from glogger.providers.google.storage import GCS
from glogger.providers.azure.blob import AzureBlob
from glogger.providers.azure.insight import AzureApplicationInsights
from glogger.providers.local.file import FileLogger
from glogger.providers.socket.websocket import Websocket
from glogger.providers.socket.papertrail import Papertrail
from glogger.cli.command import Command
from colorama import just_fix_windows_console, init, Fore


class GLogger(Logger):
    def __init__(self, client: Client):
        self.client = client

    def watch(self, command):
        current_directory = path.dirname(path.abspath(__file__))
        process = Popen(
            command,
            stdout=PIPE,
            stderr=STDOUT,
            universal_newlines=True,
            shell=True,
            cwd=current_directory,
        )

        for line in process.stdout:
            self.client.send(line.strip())


def main():
    init(autoreset=True)
    just_fix_windows_console()
    
    Environment()
    Command()

    config_providers = environ.get("GLOGGER_PROVIDER", "aws_cloudwatch,local")

    log_providers = {
        "local": FileLogger(),
        "aws_cloudwatch": CloudWatch(),
        "aws_s3": S3(),
        "azure_blob": AzureBlob(),
        "azure_insight": AzureApplicationInsights(),
        "gcp_logging": GCL(),
        "gcp_storage": GCS(),
        "websocket": Websocket(),
        "papertrail": Papertrail(),
    }

    selected_providers = config_providers.split(",")
    clients = [
        log_providers[provider]
        for provider in selected_providers
        if provider in log_providers
    ]
    loggers = [GLogger(client) for client in clients]

    commands = argv[1:]

    if not commands:
        print(f"{Fore.CYAN}Usage: glogger command to watch")
        exit(1)

    for logger in loggers:
        thread = Thread(target=logger.watch, args=(commands,))
        thread.start()

    for thread in enumerate():
        if thread != current_thread():
            thread.join()


if __name__ == "__main__":
    main()
