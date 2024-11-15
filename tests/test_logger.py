"""
Module for testing logging functionality.

Execute: python -m tests.test_logger
"""

# pylint: disable=unnecessary-comprehension
# pylint: disable=too-many-locals
# pylint: disable=line-too-long
# pylint: disable=fixme

# TODO: check stdout
# TODO: check external function

import os
import shutil
import logging
import unittest

from src.logger.logger_config import Logging


class TestLogging(unittest.TestCase):
    """Unit test class for logging setup and configuration."""

    def __init__(self, methodName: str = "runTest") -> None:
        """Initialize the test instance with a logger and directory path."""
        super().__init__(methodName)

        self.logger = None
        self.path_dir = None

    def setUp(self) -> None:
        """Set up the test environment by creating a logging directory and logger instance."""
        # generate dir
        self.path_dir = self.generate_dir()

        # set up logger
        name = self.path_dir.rsplit("_")[-1]
        self.logger = self.set_logger(name=name)

    def tearDown(self) -> None:
        """
        Tear down the test environment by closing handlers, shutting down logging, 
        and removing the logging directory.
        """
        # close handlers
        if self.logger is not None:
            for handler in self.logger.handlers[:]:
                handler.close()
                self.logger.removeHandler(handler)

        # shut down logging
        logging.shutdown()

        # remove directory
        if os.path.exists(self.path_dir):
            shutil.rmtree(self.path_dir)

    def generate_dir(
        self,
        name: str = "test_log"
    ) -> str:
        """Generate a unique logging directory for the test."""
        n = 0
        while True:
            n += 1
            name = f"{name}_{n}"
            path_dir = os.path.join(os.path.dirname(__file__), name)
            if not os.path.exists(path=path_dir):
                os.mkdir(path_dir)
                return path_dir

    def set_logger(
        self,
        name: str
    ) -> logging.Logger:
        """Set up a logger with the specified name, logging level, and directory."""
        logger = Logging().set_logger(
            name=name,
            level=logging.DEBUG,
            path_dir=self.path_dir,
        )
        return logger

    def test_logger_000(self) -> None:
        """Test the existence and basic setup of the logger."""
        # existence of logger
        self.assertIsNotNone(self.logger, "logger instance does not exist")

        # type of logger
        self.assertIsInstance(self.logger, logging.Logger, "logger is not an instance of logging.Logger")

        # existence of logger directory
        self.assertTrue(os.path.isdir(self.path_dir), f"{self.path_dir} does not exist")

        # existence of logger file
        path_log_list = os.listdir(self.path_dir)
        self.assertEqual(len(path_log_list), 1, f"{self.path_dir} has not exactly one file")

        # type of logger file
        path_log = path_log_list[0]
        self.assertTrue(path_log.endswith(".log"), f"{path_log} is not an instance of .log")

    def test_logger_001(self) -> None:
        """Test logging functionality for the DEBUG level."""
        print() # only for stdout
        level = "DEBUG"
        message = f"test - {level.lower()}"
        path_log_list = os.listdir(self.path_dir)
        path_log = os.path.join(self.path_dir, path_log_list[0])

        with open(path_log, "r", encoding="utf-8") as f:
            log_lines = [line for line in f]
        self.assertEqual(len(log_lines), 0, f"{path_log} is not empty")

        self.logger.debug("%s", message)

        with open(path_log, "r", encoding="utf-8") as f:
            log_lines = [line for line in f]
        self.assertEqual(len(log_lines), 1, f"{path_log} has not exactly one line")

        log_lines = [line for line in log_lines if level in line and message in line]
        self.assertEqual(len(log_lines), 1, f"{path_log} has not exactly one {level} line with '{message}'")

    def test_logger_002(self) -> None:
        """Test logging functionality for the INFO level."""
        print() # only for stdout
        level = "INFO"
        message = f"test - {level.lower()}"
        path_log_list = os.listdir(self.path_dir)
        path_log = os.path.join(self.path_dir, path_log_list[0])

        with open(path_log, "r", encoding="utf-8") as f:
            log_lines = [line for line in f]
        self.assertEqual(len(log_lines), 0, f"{path_log} is not empty")

        self.logger.info("%s", message)

        with open(path_log, "r", encoding="utf-8") as f:
            log_lines = [line for line in f]
        self.assertEqual(len(log_lines), 1, f"{path_log} has not exactly one line")

        log_lines = [line for line in log_lines if level in line and message in line]
        self.assertEqual(len(log_lines), 1, f"{path_log} has not exactly one {level} line with '{message}'")

    def test_logger_003(self) -> None:
        """Test logging functionality for the WARNING level."""
        print() # only for stdout
        level = "WARNING"
        message = f"test - {level.lower()}"
        path_log_list = os.listdir(self.path_dir)
        path_log = os.path.join(self.path_dir, path_log_list[0])

        with open(path_log, "r", encoding="utf-8") as f:
            log_lines = [line for line in f]
        self.assertEqual(len(log_lines), 0, f"{path_log} is not empty")

        self.logger.warning("%s", message)

        with open(path_log, "r", encoding="utf-8") as f:
            log_lines = [line for line in f]
        self.assertEqual(len(log_lines), 1, f"{path_log} has not exactly one line")

        log_lines = [line for line in log_lines if level in line and message in line]
        self.assertEqual(len(log_lines), 1, f"{path_log} has not exactly one {level} line with '{message}'")

    def test_logger_004(self) -> None:
        """Test logging functionality for the ERROR level."""
        print() # only for stdout
        level = "ERROR"
        message = f"test - {level.lower()}"
        path_log_list = os.listdir(self.path_dir)
        path_log = os.path.join(self.path_dir, path_log_list[0])

        with open(path_log, "r", encoding="utf-8") as f:
            log_lines = [line for line in f]
        self.assertEqual(len(log_lines), 0, f"{path_log} is not empty")

        self.logger.error("%s", message)

        with open(path_log, "r", encoding="utf-8") as f:
            log_lines = [line for line in f]
        self.assertEqual(len(log_lines), 1, f"{path_log} has not exactly one line")

        log_lines = [line for line in log_lines if level in line and message in line]
        self.assertEqual(len(log_lines), 1, f"{path_log} has not exactly one {level} line with '{message}'")

    def test_logger_005(self) -> None:
        """Test logging functionality for the CRITICAL level."""
        print() # only for stdout
        level = "CRITICAL"
        message = f"test - {level.lower()}"
        path_log_list = os.listdir(self.path_dir)
        path_log = os.path.join(self.path_dir, path_log_list[0])

        with open(path_log, "r", encoding="utf-8") as f:
            log_lines = [line for line in f]
        self.assertEqual(len(log_lines), 0, f"{path_log} is not empty")

        self.logger.critical("%s", message)

        with open(path_log, "r", encoding="utf-8") as f:
            log_lines = [line for line in f]
        self.assertEqual(len(log_lines), 1, f"{path_log} has not exactly one line")

        log_lines = [line for line in log_lines if level in line and message in line]
        self.assertEqual(len(log_lines), 1, f"{path_log} has not exactly one {level} line with '{message}'")

    def test_logger_006(self) -> None:
        """Test logging functionality for all level."""
        print() # only for stdout
        path_log_list = os.listdir(self.path_dir)
        path_log = os.path.join(self.path_dir, path_log_list[0])

        with open(path_log, "r", encoding="utf-8") as f:
            log_lines = [line for line in f]
        self.assertEqual(len(log_lines), 0, f"{path_log} is not empty")

        level_d = "DEBUG"
        message_d = f"test - {level_d.lower()}"
        self.logger.debug("%s", message_d)

        level_i = "INFO"
        message_i = f"test - {level_i.lower()}"
        self.logger.info("%s", message_i)

        level_e = "ERROR"
        message_e = f"test - {level_e.lower()}"
        self.logger.error("%s", message_e)

        level_w = "WARNING"
        message_w = f"test - {level_w.lower()}"
        self.logger.warning("%s", message_w)

        level_c = "CRITICAL"
        message_c = f"test - {level_c.lower()}"
        self.logger.critical("%s", message_c)

        with open(path_log, "r", encoding="utf-8") as f:
            log_lines = [line for line in f]
        self.assertEqual(len(log_lines), 5, f"{path_log} has not exactly five lines")

        log_lines_d = [line for line in log_lines if level_d in line and message_d in line]
        self.assertEqual(len(log_lines_d), 1, f"{path_log} has not exactly one {level_d} line with '{message_d}'")

        log_lines_i = [line for line in log_lines if level_i in line and message_i in line]
        self.assertEqual(len(log_lines_i), 1, f"{path_log} has not exactly one {level_i} line with '{message_i}'")

        log_lines_e = [line for line in log_lines if level_e in line and message_e in line]
        self.assertEqual(len(log_lines_e), 1, f"{path_log} has not exactly one {level_e} line with '{message_e}'")

        log_lines_w = [line for line in log_lines if level_w in line and message_w in line]
        self.assertEqual(len(log_lines_w), 1, f"{path_log} has not exactly one {level_w} line with '{message_w}'")

        log_lines_c = [line for line in log_lines if level_c in line and message_c in line]
        self.assertEqual(len(log_lines_c), 1, f"{path_log} has not exactly one {level_c} line with '{message_c}'")

    def test_logger_007(self) -> None:
        """
        Test logging behavior when generating multiple log files.
        This test verifies that the logger correctly limits the number of log files in the directory.
        """
        print() # only for stdout
        path_log_list = os.listdir(self.path_dir)
        path_log = os.path.join(self.path_dir, path_log_list[0])
        # path_log = os.path.join(self.path_dir, "asd")

        for n in range(10):
            # set logger
            name = f"test_log_{n}"
            level = logging.DEBUG
            if n % 2:
                level = logging.INFO
            logger = Logging().set_logger(
                name=name,
                level=level,
                path_dir=self.path_dir,
            )
            # message_added = False     # only for print(...)
            if n % 3:
                # message_added = True  # only for print(...)
                logger.info("%i: test - %s", n, "info")
                logger.debug("%i: test - %s", n, "debug")

            # close handlers
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)
            # shut down logging
            logging.shutdown()

            n_file = min(n + 2, 7) # +2 becasue of setUp and n = 0, 1, 2, ...
            path_log_list = os.listdir(self.path_dir)
            # print(f"\
            #     loop:    {n}\n\
            #     level:   {level}\n\
            #     files:   {len(path_log_list)}\n\
            #     message: {message_added} ↑\
            # ")
            self.assertEqual(len(path_log_list), n_file, f"{path_log} has not exactly {n_file} files")

        path_log_list = os.listdir(self.path_dir)
        self.assertEqual(len(path_log_list), 7, f"{path_log} has not exactly seven files")

    def test_logger_008(self) -> None:
        """Test the content of log files when using the logging methods."""
        print() # only for stdout
        path_log_list = os.listdir(self.path_dir)
        path_log = os.path.join(self.path_dir, path_log_list[0])


        level_i = "INFO"
        message_i = f"test - {level_i.lower()}"
        self.logger.info(message_i)
        level_i_m = "INFO"
        message_i_m = self.add_log_info()
        level_d_m = "DEBUG"
        message_d_m = self.add_log_debug()
        self.add_log_info()
        self.add_log_debug()
        self.add_log_debug()

        with open(path_log, "r", encoding="utf-8") as f:
            log_lines = [line for line in f]
        self.assertEqual(len(log_lines), 6, f"{path_log} has not exactly five lines")

        log_lines_i = [line for line in log_lines if level_i in line and message_i in line]
        self.assertEqual(len(log_lines_i), 1, f"{path_log} has not exactly two {level_i} line with '{message_i}'")

        log_lines_i_m = [line for line in log_lines if level_i_m in line and message_i_m in line]
        self.assertEqual(len(log_lines_i_m), 2, f"{path_log} has not exactly two {level_i_m} line with '{message_i_m}'")

        log_lines_d_m = [line for line in log_lines if level_d_m in line and message_d_m in line]
        self.assertEqual(len(log_lines_d_m), 3, f"{path_log} has not exactly three {level_d_m} line with '{message_d_m}'")

    def add_log_info(self) -> None:
        """
        Log an INFO level message using the logger.

        This method logs an INFO message, 'test method - info', and returns the message
        for further verification in tests.

        Returns:
            str: The logged INFO message.
        """
        message = "test method - info"
        self.logger.info(message)
        return message

    def add_log_debug(self) -> None:
        """
        Log a DEBUG level message using the logger.

        This method logs a DEBUG message, 'test method - debug', and returns the message
        for further verification in tests.

        Returns:
            str: The logged DEBUG message.
        """
        message = "test method - debug"
        self.logger.debug(message)
        return message


if __name__ == "__main__":
    unittest.main()
