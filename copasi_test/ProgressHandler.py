from __future__ import print_function

import logging
import os

class ProgressHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self, logging.INFO)
        self.infos = []
        self.warnings = []
        self.errors = []
        self.debug = []
        self.messages = []

    def emit(self, record):
        # type: (logging.LogRecord) -> None
        pos = len(self.messages)
        self.messages.append(record)
        if record.levelno == logging.INFO:
            print('.', end="")
            self.infos.append(pos)
        if record.levelno == logging.WARNING:
            print('W', end="")
            self.warnings.append(pos)
        if record.levelno == logging.ERROR:
            print('E', end="")
            self.errors.append(pos)
        if record.levelno == logging.DEBUG:
            print('D', end="")
            self.debug.append(pos)
        pass

    def handleError(self, record):
        print('X', end="")

    def close(self):
        num_errors = len(self.errors)
        if num_errors == 0:
            return
        print()
        if num_errors == 1:
            print ("There was 1 error.")
        else:
            print("There were {0} errors\n".format(num_errors))

        for err in self.errors:
            print (self.messages[err].getMessage())


def setup_logging(progress_only=True, level=logging.INFO):
    logging.basicConfig(format='%(relativeCreated)-8d %(levelname)-7s - %(message)s', level=level, datefmt='%X')

    if progress_only and os.getenv('COPASI_TEST_PRINT') is not None:
        progress_only = False

    if progress_only:
        logging.getLogger('').handlers[0] = ProgressHandler()
