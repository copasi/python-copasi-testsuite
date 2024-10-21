import logging
import os
from .TestCase import TestCase

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO


class TestSuite:
    def __init__(self, directory):
        self.suite_dir = directory
        self.cases = []
        self.initializeSuite(directory)

    def initializeSuite(self, directory):
        # type: (str) -> None
        self.cases = []

        if not os.path.exists(directory):
            logging.warning("Testsuite dir {0} does not exist".format(directory))
            return

        settings_file = os.path.join(directory, "settings.txt")
        if os.path.exists(settings_file):
            self.addTest(directory)
            return

        # walk through all directories in the given folder
        for (dir_path, dir_names, file_names) in os.walk(directory):
            dir_names.sort()
            for dir in dir_names:
                if os.path.exists(os.path.join(directory, dir, 'settings.txt')):
                    self.addTest(os.path.join(directory, dir))

    def addTest(self, directory):
        # type: (str) -> None
        case = TestCase(directory)
        if case.isValid():
            self.cases.append(case)

    def __repr__(self):
        builder = StringIO()
        builder.write('Test Suite dir:  {0}\n'.format(os.path.basename(self.suite_dir)))
        builder.write('Number of tests: {0}\n'.format(len(self.cases)))
        builder.seek(0)
        return builder.read()
