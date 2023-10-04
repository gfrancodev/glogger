from os import environ
from colorama import Fore
from sys import exit
from applicationinsights import TelemetryClient
from glogger.base.client import Client


class AzureApplicationInsights(Client):
    def __init__(self):
        self.instrumentation_key = environ.get(
            "AZURE_APP_INSIGHTS_INSTRUMENTATION_KEY"
        )

    def send(self, data):
        try:
            client = TelemetryClient(self.instrumentation_key)
            client.track_event(data)
            client.flush()

            print(
                f"""
            {Fore.BLUE}[AZURE_INSIGHTS] ➡️ {data}
            """
            )
        except Exception:
            print(
                f"""
            {Fore.RED} ❌ Failed to connect to client Azure Insights.
            """
            )
            exit(1)
