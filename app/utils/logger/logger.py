import logging
import sys
import os
import time

from logging.handlers import TimedRotatingFileHandler
from inspect import getframeinfo, stack
from dataclasses import dataclass


class BaseSingleton(type):
    _inst = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._inst:
            cls._inst[cls] = super(BaseSingleton, cls).__call__(*args, **kwargs)
            print("[BaseSingleton][Created] New instance")
        return cls._inst[cls]


# Interface for DI
class Logger:
    def __init__(self):
        pass

    def debug(self, msg: str):
        pass

    def info(self, msg: str):
        pass

    def warning(self, msg: str):
        pass

    def error(self, msg: str):
        pass


@dataclass
class LoggerInitParam:
    logger_name: str = "potato"
    # ERROR = 40, WARNING = 30, INFO = 20, DEBUG = 10
    logging_level: int = 20
    is_use_file_logging: bool = False


class PotatoLogger(metaclass=BaseSingleton):
    """
    Usage)
    import logger
    logger.info("Test Info Msg")
    """

    def __init__(self, init_param: LoggerInitParam = None):
        if not init_param:
            init_param = LoggerInitParam()
            print("[PotatoLogger][Created] Default LoggerInitParam")
        logging.basicConfig(stream=sys.stdout)
        logging.StreamHandler(stream=None)
        logging.Formatter.converter = time.gmtime

        self._logger = logging.getLogger(init_param.logger_name)
        self._logger.setLevel(init_param.logging_level)
        self._logger.propagate = False

        stream_handler = logging.StreamHandler()
        # AWS의 timestamp가 존재하기때문에 자체적인 %(asctime)s 는 현시점에서는 사용하지 않음
        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        stream_handler.setFormatter(formatter)
        self._logger.addHandler(stream_handler)
        print("[PotatoLogger][Created] Output stream handler")

        if init_param.is_use_file_logging:
            dirname = "potato_logs"
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
                print("Created ", dirname, " dir path")

            file_handler = TimedRotatingFileHandler(
                filename=dirname + "/potato.log",
                when="midnight",
                encoding=None,
                delay=False,
                backupCount=7,
            )
            file_handler.suffix = "%Y-%m-%d"
            file_formatter = logging.Formatter(
                "[%(asctime)s-%(levelname)s] %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            self._logger.addHandler(file_handler)
            print("[PotatoLogger][Created] File stream handler")
        print("[PotatoLogger][Created] New instance")

    def debug(self, msg: str):
        caller = getframeinfo(stack()[1][0])
        self._logger.debug(
            "[{0}:{1}] {2}".format(
                os.path.basename(caller.filename), caller.lineno, msg
            )
        )

    def info(self, msg: str):
        caller = getframeinfo(stack()[1][0])
        self._logger.info(
            "[{0}:{1}] {2}".format(
                os.path.basename(caller.filename), caller.lineno, msg
            )
        )

    def warning(self, msg: str):
        caller = getframeinfo(stack()[1][0])
        self._logger.warning(
            "[{0}:{1}] {2}".format(
                os.path.basename(caller.filename), caller.lineno, msg
            )
        )

    def error(self, msg: str):
        caller = getframeinfo(stack()[1][0])
        self._logger.error(
            "[{0}:{1}] {2}".format(
                os.path.basename(caller.filename), caller.lineno, msg
            )
        )

    def exception(self, msg: str):
        caller = getframeinfo(stack()[1][0])
        self._logger.error(
            "[{0}:{1}] {2}".format(
                os.path.basename(caller.filename), caller.lineno, msg
            ),
            exc_info=1,
        )
