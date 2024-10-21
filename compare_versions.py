#!/bin/env python
#
# Test tasks using CopasiSE
#
from __future__ import print_function
import sys
import os

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

from copasi_test import *

if __name__ == "__main__":
    setup_logging()

    num_args = len(sys.argv)
    if num_args != 6:
        print("usage: compare_versions <Test> <CopasiSE1> <OutputDir1>  <CopasiSE2> <OutputDir2>")
        sys.exit(1)

    suite = TestSuite(sys.argv[1])
    runner1 = TestRunner(sys.argv[2], os.path.abspath(sys.argv[3]))
    runner2 = TestRunner(sys.argv[4], os.path.abspath(sys.argv[5]))

    result = 0
    print("Comparing tests of {0} with results of {1} against {2}".format(suite, runner1, runner2))
    for case in suite.cases:
        result += runner1.compareTestAgainstOther(case, runner2)

    if result == 0:
        print("\nall pass")

    sys.exit(result)
