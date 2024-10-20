"""
This module provides logging functionality to create 
and manage loggers with both file and stream handlers.
Log files are stored in a specified directory, 
with a mechanism to clean up old log files.
"""

import os
import logging

from datetime import datetime


class Logging:
    """
    A class that encapsulates the creation and configuration of logging handlers, 
    including file and stream output, for logging messages to a specified directory.
    """

    def set_logger(
        self,
        name: str,
        level: int,
        path_dir: str
    ) -> logging.Logger:
        """
        Sets up and returns a logger with the specified name and level, 
        adding both file and stream handlers.

        Args:
            name (str): The name of the logger.
            level (int): The logging level (e.g., logging.DEBUG, logging.INFO).
            path_dir (str): The directory where the log file will be created.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger_ = logging.getLogger(name=name)
        logger_.setLevel(level=level)

        # check if the logger already has handlers to avoid adding handlers multiple times
        self.clean_log_dir(path_dir=path_dir)
        if not logger_.handlers:
            path_log = self.generate_path_log(path_dir=path_dir)
            formatter = logging.Formatter(
                "%(asctime)s %(levelname)s %(filename)s %(funcName)s: %(message)s"
            )

            file_handler = logging.FileHandler(path_log)
            file_handler.setFormatter(formatter)

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)

            logger_.addHandler(file_handler)
            logger_.addHandler(stream_handler)

        return logger_

    def generate_path_log(self, path_dir: str) -> str:
        """
        Generates a unique log file path in the specified directory using the current timestamp.

        Args:
            path_dir (str): The directory where the log file will be created.

        Returns:
            str: The generated log file path.
        """
        while True:
            current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            path_log = os.path.join(path_dir, f"{current_time}.log")
            if not os.path.exists(path=path_log):
                return path_log

    def clean_log_dir(self, path_dir: str) -> None:
        """
        Removes old log files from the specified directory, keeping only the most recent five logs.

        Args:
            path_dir (str): The directory from which old log files will be removed.
        """
        path_log_list = [
            path_log for path_log in os.listdir(path_dir) if os.path.splitext(path_log)[1] == ".log"
        ]
        for n, path_log in enumerate(list(reversed(path_log_list))):
            if n > 5:
                path_log = os.path.join(path_dir, path_log)
                os.remove(path=path_log)


if __name__ == "__main__":
    # Example usage of the Logging class. This sets up a logger and demonstrates logging
    # at various levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    logger = Logging().set_logger(
        name=__name__,
        level=logging.DEBUG,
        path_dir="___PATH_TO_LOG_DIR___", # Replace with the actual path to the logs directory
    )

    msg_prefix = "test" # pylint: disable=invalid-name
    logger.debug("%s - debug", msg_prefix)
    logger.info("%s - info", msg_prefix)
    logger.warning("%s - warning", msg_prefix)
    logger.error("%s - error", msg_prefix)
    logger.critical("%s - critical", msg_prefix)
