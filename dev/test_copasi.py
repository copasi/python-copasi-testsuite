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

#basico.settings['quiet'] = True


class CompareResult:
    def __init__(self):
        pass


def are_close(df1, df2, **kwargs):
    # type: (pandas.DataFrame, pandas.DataFrame) -> bool

    if df1 is None or df2 is None:
        return False

    have_mismatch = (numpy.isclose(df1, df2, equal_nan=True, **kwargs) == False).any()

    return not have_mismatch


def match(result1, result2, **kwargs):
    # type: (test_copasi.TestReport, test_copasi.TestReport) -> bool
    result = True
    n_max = min(len(result1.data_frames), len(result2.data_frames))
    for i in range(n_max):
        if result1.data_descriptions[i] != result2.data_descriptions[i]:
            continue
        df1 = result1.data_frames[i]
        df2 = result2.data_frames[i]

        if not are_close(df1, df2, **kwargs):
            print ('Mismatch in {0}\n\n'.format(result1.data_descriptions[i]['desc']))
            #print(df1[numpy.isclose(df1, df2, equal_nan=True, **kwargs) == False])
            #print('\n\nvs\n\n')
            #print(df2[numpy.isclose(df1, df2, equal_nan=True, **kwargs) == False])
            result = False

    if result:
        print ('all match')
    return result


def compare_data_frames(df1, df2):
    # type: (pandas.DataFrame, pandas.DataFrame) -> CompareResult
    result = CompareResult()

    if df1 is None or df2 is None:
        return  result



    return  result


class TestClass:

    def __init__(self):
        self.runners = []
        self.suite = None
        self.versions = None

    def setup(self):
        all_versions = ['4.24.193', '4.23.184', '4.22.170',
                        '4.21.166', '4.20.158', '4.19.140',
                        '4.18.136', '4.17.135', '4.16.104',
                        '4.15.95', '4.11.65', '4.8.35']
        # all_versions = ['4.18.136', '4.17.135', '4.16.104', '4.15.95', '4.11.65', '4.8.35']

        # for version in ['4.24.193', '4.23.184', '4.22.170', '4.21.166', '4.20.158', '4.19.140', '4.18.136', '4.17.135', '4.16.104', '4.15.95', '4.11.65', '4.8.35']:

        # initialize all test suite runners
        runners = []
        for version in all_versions:
            r1 = TestRunner(r"C:\Program Files\copasi.org\COPASI {0}\bin\CopasiSE.exe".format(version),
                            r"c:\Temp\{0}".format(version))
            if not r1.is_valid():
                continue

            assert os.path.isfile(r1.executable)
            assert os.path.isdir(r1.output_dir)

            runners.append(r1)

        s1 = TestSuite('test-suite')
        assert len(s1.cases) > 0


def test():
    logger = logging.getLogger("test")
    logger.setLevel(logging.DEBUG)

    report = TestReport('c:/Temp/report-00001-BIOMD0000000001.txt', TaskTypes.timecourse)
    assert report.filename == 'c:/Temp/report-00001-BIOMD0000000001.txt'
    assert report.task == TaskTypes.timecourse
    assert len(report.data_frames) > 0

    report = TestReport('c:/Temp/report-00002-BIOMD0000000001.txt', TaskTypes.steadystate)
    assert report.filename == 'c:/Temp/report-00002-BIOMD0000000001.txt'
    assert report.task == TaskTypes.steadystate
    assert len(report.data_frames) > 0

    report = TestReport('c:/Temp/report-00003-BIOMD0000000003.txt', TaskTypes.mca)
    assert report.filename == 'c:/Temp/report-00003-BIOMD0000000003.txt'
    assert report.task == TaskTypes.mca
    assert len(report.data_frames) > 0

    report = TestReport('c:/Temp/report-00004-BIOMD0000000001.txt', TaskTypes.efm)
    assert report.filename == 'c:/Temp/report-00004-BIOMD0000000001.txt'
    assert report.task == TaskTypes.efm
    assert len(report.data_frames) > 0

    report = TestReport('c:/Temp/4.24.193/report-00013-RastriginFunction.txt', TaskTypes.optimization)
    assert report.filename == 'c:/Temp/4.24.193/report-00013-RastriginFunction.txt'
    assert report.task == TaskTypes.optimization
    assert len(report.data_frames) > 0

    report = TestReport('c:/Temp/report-00006-BIOMD0000000004.txt', TaskTypes.lyap)
    assert report.filename == 'c:/Temp/report-00006-BIOMD0000000004.txt'
    assert report.task == TaskTypes.lyap
    assert len(report.data_frames) > 0

    report = TestReport('c:/Temp/4.20.158/report-00007-BIOMD0000000002.txt', TaskTypes.tssa)
    assert report.task == TaskTypes.tssa
    assert len(report.data_frames) > 0

    report = TestReport('c:/Temp/4.23.184/report-00007-BIOMD0000000002.txt', TaskTypes.tssa)
    assert report.filename == 'c:/Temp/4.23.184/report-00007-BIOMD0000000002.txt'
    assert report.task == TaskTypes.tssa
    assert len(report.data_frames) > 0

    report = TestReport('c:/Temp/report-00007-BIOMD0000000002.txt', TaskTypes.tssa)
    assert report.filename == 'c:/Temp/report-00007-BIOMD0000000002.txt'
    assert report.task == TaskTypes.tssa
    assert len(report.data_frames) > 0

    report = TestReport('c:/Temp/report-00008-BIOMD0000000003.txt', TaskTypes.sensitivities)
    assert report.filename == 'c:/Temp/report-00008-BIOMD0000000003.txt'
    assert report.task == TaskTypes.sensitivities
    assert len(report.data_frames) > 0

    report = TestReport('c:/Temp/4.24.193/report-00014-LM-test1.txt', TaskTypes.parameterEstimation)
    assert report.filename == 'c:/Temp/4.24.193/report-00014-LM-test1.txt'
    assert report.task == TaskTypes.parameterEstimation
    assert len(report.data_frames) > 0

    report = TestReport('c:/Temp/4.24.193/report-00011-BIOMD0000000011.txt', TaskTypes.lna)
    assert report.filename == 'c:/Temp/4.24.193/report-00011-BIOMD0000000011.txt'
    assert report.task == TaskTypes.lna
    assert len(report.data_frames) > 0

    all_versions = ['4.24.197']
          # , '4.23.184', '4.22.170',
          #           '4.21.166', '4.20.158', '4.19.140',
          #           '4.18.136', '4.17.135', '4.16.104',
          #           '4.15.95', '4.11.65', '4.8.35']
    # all_versions = ['4.18.136', '4.17.135', '4.16.104', '4.15.95', '4.11.65', '4.8.35']

    #for version in ['4.24.193', '4.23.184', '4.22.170', '4.21.166', '4.20.158', '4.19.140', '4.18.136', '4.17.135', '4.16.104', '4.15.95', '4.11.65', '4.8.35']:

    # initialize all test suite runners
    runners = []
    for version in all_versions:
        r1 = TestRunner(r"C:\Program Files\copasi.org\COPASI {0}\bin\CopasiSE.exe".format(version),
                        r"c:\Temp\{0}".format(version))
        if not r1.is_valid():
            continue

        assert os.path.isfile(r1.executable)
        assert os.path.isdir(r1.output_dir)

        runners.append(r1)


    s1 = TestSuite('test-suite')
    assert len(s1.cases) > 0

    cases = s1.cases

    # filter as needed
    #cases = [ c for c in cases if c.task_type == TaskTypes.mca or c.task_type == TaskTypes.efm]
    #cases = [c for c in cases if c.task_type == TaskTypes.optimization and c.id == '00013']
    #cases = [c for c in cases if c.task_type == TaskTypes.lyap]
    cases = [c for c in cases if c.task_type == TaskTypes.tssa]
    #cases = [c for c in cases if c.task_type == TaskTypes.efm]
    #cases = [c for c in cases if c.id == '00014']
    #cases = [c for c in cases if c.id == '00013']

    #cases[0].open_dir()
    #cases[0].open_settings()

    for c1 in cases:
        assert c1.isValid()

        for r1 in runners:
            r1.runTest(c1, use_existing=False, write_result=False)
            #assert r1.runTest(c1, use_existing=True) == 0
            #r1.remove_results(c1, remove_model=False, remove_report=False, remove_result=True)


    #sys.exit(0)


if __name__ == "__main__":
    num_args = len(sys.argv)
    if num_args != 4:
        print("usage: test_copasi <Test> <CopasiSE> <OutputDir>")
        sys.exit(1)

    suite = TestSuite(sys.argv[1])
    runner = TestRunner(sys.argv[2], os.path.abspath(sys.argv[3]))

    sys.exit(runner.runTests(suite.cases))


