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
    if num_args < 4:
        print("usage: test_copasi <Test> <CopasiSE> <OutputDir> [Task Name]")
        sys.exit(1)

    suite = TestSuite(sys.argv[1])
    runner = TestRunner(sys.argv[2], os.path.abspath(sys.argv[3]))

    task_name = None
    if num_args == 5:
        task_name = sys.argv[4]

    cases = suite.cases
    if task_name is not None:
        cases = [c for c in cases if c.task_type == task_name]

    result = runner.runTests(cases)
    
    if result == 0: 
        print("\nall pass")
    sys.exit(result)
