#!/bin/env python
#
# Test tasks using CopasiSE
#
from __future__ import print_function
import sys
import os

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from copasi_test import *

if __name__ == "__main__":
    setup_logging()

    num_args = len(sys.argv)
    if num_args != 4:
        print("usage: compare_only <Test> <CopasiSE> <OutputDir>")
        sys.exit(1)

    suite = TestSuite(sys.argv[1])
    runner = TestRunner(sys.argv[2], os.path.abspath(sys.argv[3]))

    print("Comparing tests of {0} with results of {1}".format(suite, runner))
    result = 0
    for case in suite.cases:
        result += runner.compareTest(case)

    if result == 0:
        print("\nall pass")

    sys.exit(result)
