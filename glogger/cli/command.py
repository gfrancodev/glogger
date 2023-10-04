from colorama import just_fix_windows_console, init, Fore
from os import environ
from sys import argv, exit
from platform import system
from glogger.config.environment import Environment

class Command:
    def __init__(self):
        self.execute()
    
    def help(self):
        platform = system()
        global config_path
        
        if platform == "Linux" or platform == "Darwin":
            config_path = "/etc/glogger/glogger.config"
        if platform == "Windows":  # Verifique a plataforma Windows
            config_path = "C:\\ProgramData\\glogger\\glogger.config"
            
        help_message = f"""
        {Fore.GREEN}Usage:{Fore.RESET}
        glogger [command]
        glogger [options]

        {Fore.GREEN}Options:{Fore.RESET}
        -h, --help          Display this help message
        -p, --providers     List available log providers
        -e, --env           List available enviroments for providers in the glogger.conf
                            the configuration file is located at: ({config_path})
                            

        {Fore.MAGENTA}Explanation:{Fore.RESET}
        The {Fore.BLUE}'GLOGGER_CONFIG_PATH'{Fore.RESET} environment variable is essential because it loads the 
        necessary environment variables required for the providers to function properly.
        
        The behavior of GLogger can be customized by setting the 'GLOGGER_PROVIDER' environment variable.
        This variable determines which log providers are active and available for use. By default, 
        'GLOGGER_PROVIDER' is set to 'aws_cloudwatch,local', activating the AWS CloudWatch Logs and
        Local File Logger providers.

        You can configure this variable to include a comma-separated list of log provider names that you want to activate. 
        
        For example:
        - To activate AWS CloudWatch Logs only, set {Fore.BLUE}'GLOGGER_PROVIDER' to 'aws_cloudwatch'{Fore.RESET}.
        - To activate both AWS S3 and Azure Blob Storage, set {Fore.BLUE}'GLOGGER_PROVIDER' to 'aws_s3,azure_blob'{Fore.RESET}.

        Use 'glogger providers' to list the available log providers.

        To run GLogger in watch mode, use the following command:
        glogger <command>
        
        {Fore.MAGENTA}Explanation:{Fore.RESET}
        GLogger's watch mode allows you to monitor the execution of any system command and 
        send its logs in real-time to a configured log provider. This feature is useful for
        tracking command output and automatically collecting log records.

        {Fore.MAGENTA}Here's how it works:{Fore.RESET}
        1. Execute a system command as usual.
        2. GLogger monitors the command's standard output in real-time.
        3. Logs are sent to the configured log provider as the command runs.
        4. You can access and analyze these logs later.

        {Fore.MAGENTA}To use watch mode, run the following command:{Fore.RESET}
        glogger <command>

        {Fore.MAGENTA}Example:{Fore.RESET}
        glogger sh my_script.sh
        glogger node my_script.js

        Please note that the order of the log providers in {Fore.BLUE}'GLOGGER_PROVIDER'{Fore.RESET} 
        determines their priority. Active providers will be used in the order they appear in the list.

        Remember to configure the required environment variables for each log provider you enable 
        {Fore.BLUE}'GLOGGER_PROVIDER'{Fore.RESET} to ensure they work correctly.
        """
        print(help_message)
    
    def providers(self):
        providers = f"""
        The available log providers are:
        {Fore.MAGENTA}
        - local
        - aws_cloudwatch
        - aws_s3
        - azure_blob
        - azure_insight
        - gcp_logging
        - gcp_storage
        - websocket
        - papertrail
        {Fore.RESET}
        """
        print(providers)
    
    def environment(self):
        text = f"""
        {Fore.MAGENTA}Explanation of Environment Variables:{Fore.RESET}
        - {Fore.GREEN}AWS_ACCESS_KEY_ID:{Fore.RESET} The AWS access key ID for accessing AWS services.
        - {Fore.GREEN}AWS_SECRET_ACCESS_KEY:{Fore.RESET} The AWS secret access key associated with the access key ID.
        - {Fore.GREEN}AWS_REGION:{Fore.RESET} The AWS region where the logs will be stored.
        - {Fore.GREEN}AWS_CLOUDWATCH_LOG_GROUP_NAME:{Fore.RESET} The name of the AWS CloudWatch log group.
        - {Fore.GREEN}AWS_CLOUDWATCH_LOG_STREAM_NAME:{Fore.RESET} The name of the AWS CloudWatch log stream.
        - {Fore.GREEN}AWS_BUCKET_NAME:{Fore.RESET} The name of the AWS S3 bucket where logs will be stored.
        - {Fore.GREEN}AWS_OBJECT_KEY:{Fore.RESET} The key of the AWS S3 object where logs will be stored.
        - {Fore.GREEN}AZURE_STORAGE_CONNECTION_STRING:{Fore.RESET} The connection string for accessing Azure Blob Storage.
        - {Fore.GREEN}AZURE_CONTAINER_NAME:{Fore.RESET} The name of the Azure Blob Storage container.
        - {Fore.GREEN}AZURE_BLOB_NAME:{Fore.RESET} The name of the Azure Blob where logs will be stored.
        - {Fore.GREEN}AZURE_APP_INSIGHTS_INSTRUMENTATION_KEY:{Fore.RESET} The Application Insights instrumentation key for Azure.
        - {Fore.GREEN}GCP_LOG_NAME:{Fore.RESET} The name of the Google Cloud Logging log.
        - {Fore.GREEN}GCP_PROJECT_ID:{Fore.RESET} The ID of the Google Cloud project.
        - {Fore.GREEN}GCP_BUCKET_NAME:{Fore.RESET} The name of the Google Cloud Storage bucket.
        - {Fore.GREEN}GCP_OBJECT_KEY:{Fore.RESET} The key of the Google Cloud Storage object.
        - {Fore.GREEN}WEBSOCKET_URI:{Fore.RESET} The URI for WebSocket communication by {Fore.MAGENTA}GFRANCODEV/GLOGGER SERVER{Fore.RESET}.
        - {Fore.GREEN}LOCAL_FILE_PATH:{Fore.RESET} The local file path where logs will be stored when using the "local" log provider.
        - {Fore.GREEN}PAPERTRAIL_HOST:{Fore.RESET} The hostname or IP address of the Papertrail log destination.
        - {Fore.GREEN}PAPERTRAIL_PORT:{Fore.RESET} The port number for connecting to the Papertrail log destination.                                                               
        """
        print(text)
        
    def execute(self):
        init(autoreset=True)
        just_fix_windows_console()
        
        ascii_art = f"""
        {Fore.BLUE}
        ▄████  ██▓     ▒█████    ▄████   ▄████ ▓█████  ██▀███  
        ██▒ ▀█▒▓██▒    ▒██▒  ██▒ ██▒ ▀█▒ ██▒ ▀█▒▓█   ▀ ▓██ ▒ ██▒
        ▒██░▄▄▄░▒██░    ▒██░  ██▒▒██░▄▄▄░▒██░▄▄▄░▒███   ▓██ ░▄█ ▒
        ░▓█  ██▓▒██░    ▒██   ██░░▓█  ██▓░▓█  ██▓▒▓█  ▄ ▒██▀▀█▄  
        ░▒▓███▀▒░██████▒░ ████▓▒░░▒▓███▀▒░▒▓███▀▒░▒████▒░██▓ ▒██▒
        ░▒   ▒ ░ ▒░▓  ░░ ▒░▒░▒░  ░▒   ▒  ░▒   ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
        ░   ░ ░ ░ ▒  ░  ░ ▒ ▒░   ░   ░   ░   ░  ░ ░  ░  ░▒ ░ ▒░
        ░ ░   ░   ░ ░   ░ ░ ░ ▒  ░ ░   ░ ░ ░   ░    ░     ░░   ░ 
            ░     ░  ░    ░ ░        ░       ░    ░  ░   ░            
                                                          
        {Fore.RESET}
        {Fore.CYAN}     v0.2 GFRANCODEV | GLOGGER - Log Aggregator{Fore.RESET}
        """
        
        print(ascii_art)
        
        if len(argv) < 2:
            self.help()
            exit(1)
        
        if str(argv[1]) == "--help" or str(argv[1]) == "-h":
            self.help()
            exit(0)
            
        if str(argv[1]) == "--providers" or str(argv[1]) == "-p":
            self.providers()
            exit(0)
            
        if str(argv[1]) == "--env" or str(argv[1]) == "-e":
            self.environment()
            exit(0)