from pathlib import Path
import os
import logging.handlers
from datetime import date
import time


class Logging:
    def __init__(self, project_name):
        self._log_dir = str(Path(__file__).parent / 'logs')
        self._logger = self._create_logger(project_name)

    def _create_logger(self, _project_name):
        logging_level = logging.DEBUG
        _logfile = '{}/{}.log'.format(self._log_dir, _project_name)
        if not os.path.exists(self._log_dir):
            os.makedirs(self._log_dir)

        logger = logging.getLogger(_project_name)
        logger.setLevel(logging_level)

        fh = logging.FileHandler(_logfile)
        fh.setLevel(logging_level)

        ch = logging.StreamHandler()
        ch.setLevel(logging_level)

        formatter = logging.Formatter("%(asctime)s - [%(filename)s - %(funcName)10s():%(lineno)s ] - "
                                      "%(levelname)s - %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)
        return logger

    @property
    def logger(self):
        return self._logger


class Configuration:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent

    @property
    def today(self):
        return str(date.today())

    @property
    def unix_time(self):
        return int(time.time())
