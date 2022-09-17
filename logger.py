import logging
import time
import os

from logging import handlers
from __init__ import __appname__

class Logger():
    def __init__(self):
        self.logger = logging.getLogger(__appname__)
        # output level
        LEVELS = {
            'NOSET': logging.NOTSET,
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }

        # logfile path for storage
        timestr = time.strftime('%Y_%m_%d', time.localtime(time.time()))
        log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './logs'))
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        self.logname = log_path + '/' + timestr + '.log'

        # set log level
        self.logger.setLevel(logging.INFO)

        # log format
        self.formatter = logging.Formatter('[%(levelname)s] %(module)s:%(funcName)s:%(lineno)s - %(message)s')

        # fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')
        fh = handlers.RotatingFileHandler(filename=self.logname, maxBytes=1024*1024*50,backupCount=5)

        fh.setLevel(logging.INFO)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        fh.close()

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)






