__author__="Xaralis"
__date__ ="$25.10.2009 14:44:38$"

import logging
from os.path import dirname, join

import metrocar
from metrocar import settings
from metrocar.utils.models import LogMessage

class DbHandler(logging.Handler):
    def emit(self, record):
        message = LogMessage()
        message.level_no = record.__dict__.get('levelno')
        message.message = record.__dict__.get('msg')
        message.save()

file_handler = logging.FileHandler(join(dirname(metrocar.__file__), settings.LOG_PATH))
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
db_handler = DbHandler()
db_handler.level = logging.DEBUG

logger = logging.getLogger('metrocar')
logger.setLevel(logging.DEBUG)
logger.addHandler(db_handler)
logger.addHandler(file_handler)

def get_logger():
    return logger