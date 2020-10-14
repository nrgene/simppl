import os
from logging.config import fileConfig
from os import path

# Uncomment these lines in your actual module for turning simple-pipeline logs on
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging_config.ini')
if not path.exists(log_file_path):
    exit(f'''missing logging config file: {log_file_path}
            files in directory: {os.listdir(path.dirname(path.abspath(__file__)))}''')
fileConfig(log_file_path)
