import logzero
from logzero import logger
from colorlog import ColoredFormatter

import os


def check_and_create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Directory: '{directory}' created successfully.")


def check_and_create_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass
        logger.info(f"File: '{file_path}' created successfully.")


def check_or_create_dir(log_directory, log_filename):
    # Example usage
    target_directory = log_directory
    target_file = log_directory + log_filename
    check_and_create_directory(target_directory)
    check_and_create_file(target_file)


def setup_logger(log_directory, log_filename, max_log_size, backup_count):
    check_or_create_dir(log_directory, log_filename)

    logzero.logfile(log_directory + log_filename, maxBytes=max_log_size, backupCount=backup_count)
    logzero.loglevel(logzero.DEBUG)

    fmt = (
        '%(log_color)s[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s'
    )
    
    datefmt = '%Y-%m-%d %H:%M:%S'
    
    formatter = ColoredFormatter(
        fmt,
        datefmt=datefmt,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    
    logzero.formatter(formatter)
    

def start(directory='/opt/cs/logs/', file_name='terminal.log'):
    max_log_size = 1024 * 1024
    backup_count = 5

    setup_logger(directory, file_name, max_log_size, backup_count)
