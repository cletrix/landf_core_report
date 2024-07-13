import os
import sys
import datetime
import pytz
from version import __version__

TZ_CS = pytz.timezone('America/Sao_Paulo')

VERSION = __version__
PORT = 33444
HOST = "0.0.0.0"
LOG_DIR = "/opt/report/logs/"
LOG_FILE_NAME = 'terminal_report.log'
HOST_DB = 'keno.cletrix.net'
PORT_DB = 53306
START_TIME = '{:%Y-%m-%d %H:%M:%S:%f %Z}'.format(datetime.datetime.now(TZ_CS))

MODE_ENV = os.environ.get('MODE_ENV')


if MODE_ENV == 'LOCAL':
    HOST_DB = 'titan.cletrix.net'

db_config = {
    'host': HOST_DB,
    'port': PORT_DB,
    'user': 'cleyton',
    'password': 'Jane4k_SGiuwyetgjdgkgjBVHJASCX567923',
    'autocommit': True,
    'charset': 'utf8mb4',
    'minsize': 1,
    'maxsize': 20,
}

db_name = 'CS1'


def to_str():
    config_dict = {'PYTHON_VERSION': sys.version,
                   'VERSION': VERSION,
                   'HOST': HOST,
                   'PORT': PORT,
                   'MODE_ENV': MODE_ENV,
                   'DB HOST': db_config['host'],
                   'DB PORT': db_config['port'],
                   'LOG_FILE_NAME': LOG_DIR + LOG_FILE_NAME,
                   'START_TIME': START_TIME}

    config_string = ""

    for key, value in config_dict.items():
        config_string += f'\n\t{key}: {value}'

    return config_string
