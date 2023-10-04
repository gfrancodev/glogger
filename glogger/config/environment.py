from configparser import ConfigParser
from os import environ, path
from platform import system
from subprocess import run, DEVNULL
from colorama import Fore
from sys import exit


class Environment:
    def __init__(self):
        self.platform = system()
        self.config_file_path = environ.get(
            "GLOGGER_CONFIG_PATH", "glogger.config"
        )
        self.config = self.load_config()
        self.providers_section = "providers"
        self.papertrail_keys = ["PAPERTRAIL_HOST", "PAPERTRAIL_PORT"]
        self.aws_keys = [
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "AWS_BUCKET_NAME",
            "AWS_OBJECT_KEY",
            "AWS_REGION",
            "AWS_CLOUDWATCH_LOG_GROUP_NAME",
            "AWS_CLOUDWATCH_LOG_STREAM_NAME",
        ]
        self.azure_keys = [
            "AZURE_STORAGE_CONNECTION_STRING",
            "AZURE_CONTAINER_NAME",
            "AZURE_BLOB_NAME",
            "AZURE_APP_INSIGHTS_INSTRUMENTATION_KEY",
        ]
        self.gcp_keys = [
            "GPC_APPLICATION_CREDENTIALS",
            "GCP_LOG_NAME",
            "GCP_PROJECT_ID",
            "GCP_BUCKET_NAME",
            "GCP_OBJECT_KEY",
        ]
        self.websocket_keys = ["WEBSOCKET_URI"]
        self.local_file_keys = ["LOCAL_FILE_PATH"]
        self.execute()

    def create_glogger_config(self):
        config = ConfigParser()

        config["providers"] = {
            "AWS_ACCESS_KEY_ID": "",
            "AWS_SECRET_ACCESS_KEY": "",
            "AWS_REGION": "",
            "AWS_CLOUDWATCH_LOG_GROUP_NAME": "",
            "AWS_CLOUDWATCH_LOG_STREAM_NAME": "",
            "AWS_BUCKET_NAME": "",
            "AWS_OBJECT_KEY": "",
            "AZURE_STORAGE_CONNECTION_STRING": "",
            "AZURE_CONTAINER_NAME": "",
            "AZURE_BLOB_NAME": "",
            "AZURE_APP_INSIGHTS_INSTRUMENTATION_KEY": "",
            "GPC_APPLICATION_CREDENTIALS": "",
            "GCP_LOG_NAME": "",
            "GCP_PROJECT_ID": "",
            "GCP_BUCKET_NAME": "",
            "GCP_OBJECT_KEY": "",
            "MONGO_URI": "",
            "WEBSOCKET_URI": "",
            "LOCAL_FILE_PATH": "",
            "PAPERTRAIL_HOST": "",
            "PAPERTRAIL_PORT": "",
        }

        with open("glogger.conf", "w") as config_file:
            config.write(config_file)

    def exists_config(self):
        global config_path
        if self.platform == "Linux" or self.platform == "Darwin":
            config_path = "/etc/glogger/glogger.config"
        if self.platform == "Windows":
            config_path = "C:\\ProgramData\\glogger\\glogger.config"
        if not path.exists(config_path):
            self.create_glogger_config()

    def load_config(self):
        config = ConfigParser()
        config.read(self.config_file_path)
        return config

    def set_env_variables(self, section, keys):
        for key in keys:
            env_var = key.upper()
            value = self.config.get(section, key)
            environ[env_var] = value

            if self.platform == "Linux" or self.platform == "Darwin":
                run(
                    ["export", f"{env_var}={value}"],
                    stdout=DEVNULL,
                    stderr=DEVNULL,
                    shell=True,
                )
            if self.platform == "Windows":
                run(
                    ["setx", f"{env_var}={value}"],
                    stdout=DEVNULL,
                    stderr=DEVNULL,
                    shell=True,
                )

    def execute(self):
        try:
            self.set_env_variables(self.providers_section, self.aws_keys)
            self.set_env_variables(self.providers_section, self.azure_keys)
            self.set_env_variables(self.providers_section, self.gcp_keys)
            self.set_env_variables(self.providers_section, self.websocket_keys)
            self.set_env_variables(
                self.providers_section, self.local_file_keys
            )
            self.set_env_variables(
                self.providers_section, self.papertrail_keys
            )
            print(f"""{Fore.GREEN}      ✅ Enabled environment variables.""")
        except BaseException:
            print(
                f"""
            {Fore.RED} ❌ Failed to implement glogger.config provider variables. Please check your settings.
            """
            )
            exit(1)
