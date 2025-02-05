import logging
import os


def enable_log(path: str = "./agent.log", log_level: str= "info", mode: str = "w" ):
    """
        Enables logging for the application.

        :param path: The file path to log to. Defaults to "./agent.log".
        :type path: str, optional
        :param log_level: The log level to use. Defaults to "info".
        :type log_level: str, optional
    """
    if path is None:
        path = "./agent.log"
    os.environ["LOG_LEVEL"] = log_level
    os.environ["LOG_PATH"] = path
    assert log_level.upper() in {
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    }, "Invalid log level."
    assert mode in {"w", "a"}, "Invalid mode."
    logging.basicConfig(level=log_level.upper(), filename=path, filemode=mode)



def check_log():
    """
        Checks if logging has been enabled.
        :return: True if logging has been enabled, False otherwise.
        :rtype: bool
    """
    return os.environ.get("LOG_PATH", None) is not None
