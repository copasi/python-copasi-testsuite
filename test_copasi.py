#!/bin/env python
#
# Test tasks using CopasiSE
#
from __future__ import print_function
import sys
import os
import logging
import pandas
import numpy

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from copasi_test import *

if __name__ == "__main__":
    num_args = len(sys.argv)
    if num_args != 4:
        print("usage: test_copasi <Test> <CopasiSE> <OutputDir>")
        sys.exit(1)

    suite = TestSuite(sys.argv[1])
    runner = TestRunner(sys.argv[2], os.path.abspath(sys.argv[3]))
    
    result = runner.runTests(suite.cases)
    
    if result == 0: 
        print("all pass")
    sys.exit(result)


