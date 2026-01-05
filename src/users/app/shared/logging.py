from datetime import datetime
import logging
import os
import socket
import sys

from pythonjsonlogger import jsonlogger


# TODO: if another micro service is created in this application please move this file in a shared directory
#  in the 'src' folder
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    This class is a custom json logger to send code in something like elasticsearch to simplify parsing
    and help MCO
    """

    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if not log_record.get("application"):
            log_record["application"] = os.environ.get(
                "APPLICATION_NAME", "not defined"
            )
        if not log_record.get("environment"):
            log_record["environment"] = os.environ.get(
                "APPLICATION_ENVIRONMENT", "not defined"
            )
        if log_record.get("severity"):
            log_record["severity"] = log_record["severity"].upper()
        else:
            log_record["severity"] = record.levelname
        if not log_record.get("host"):
            log_record["host"] = socket.gethostname()


def get_json_logger(name, log_lvl=logging.INFO, log_ext_lvl=logging.WARN):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler(sys.stdout)
    formatter = CustomJsonFormatter(
        "%(timestamp)s %(severity)s %(name)s %(funcName)s %(message)s %(application)s %(environment)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_lvl)
    # configure external loggers (third party libs, etc...)
    external_loggers = ("requests", "urllib3", "aiohttp", "chardet")

    for logger_name in external_loggers:
        external_logger = logging.getLogger(logger_name)
        external_logger.setLevel(log_ext_lvl)
    return logger
