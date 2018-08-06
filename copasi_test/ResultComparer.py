from TestReport import  TestReport
from RunResult import RunResult
import numpy as np
import pandas
import logging

class CompareResult:
    def __init__(self):
        self.differences = []
        self.run_result = None
        self.explicit_fail = False
        self.messages = []
        self.changes = []

    def get_run_result(self):
        #type: () -> RunResult

        for msg in self.messages:
            print(msg)

        if self.explicit_fail:
            return RunResult.FAIL

        for df in self.differences:
            assert (isinstance(df, pandas.DataFrame))
            if df.any().any():
                print(df.describe())
                self.changes.append(df.any())
                return RunResult.FAIL


        return RunResult.PASS

class ResultComparer:
    def __init__(self, task_type = None):
        self.task_type = task_type
        self.expected = None
        self.other = None
        pass


    @staticmethod
    def get_differences(df1, df2, expected = None, **kwargs):
        # type: (pandas.DataFrame, pandas.DataFrame) -> pandas.DataFrame
        if expected is None:
            expected = df1
        return expected[np.isclose(df1, df2, equal_nan=True, **kwargs) == False]

    @staticmethod
    def get_subset(df, indices):
        # type: (pandas.DataFrame, [int]) -> pandas.DataFrame
        cols = []
        for i in indices:
            cols.append(df.columns[i])
        return df[cols]

    @staticmethod
    def compare_df_testsuite(df1, df2, expected = None, **kwargs):
        if expected is None:
            expected = df1

        atol = kwargs.get('atol', 0.0001)
        rtol = kwargs.get('rtol', 0.0001)

        diff = (np.abs(df1 - df2) <= atol + rtol * np.abs(df1))
        have_error = (diff == False)
        if have_error.any().any():
            return None
        return expected[have_error]


    @staticmethod
    def compare_df_unsorted(df1, df2, **kwargs):
        """
            compares two data frames based on their column and row indices, that way the comparison
            will work even if the indices are in a different order

        :param df1: first data frame
        :param df2: second data frame
        :param kwargs: optional parameters
        :return: boolean indicating whether the datasets match
        """
        # type: (pandas.DataFrame, pandas.DataFrame) -> pandas.DataFrame

        atol = kwargs.get('atol', 0.0001)
        rtol = kwargs.get('rtol', 0.0001)
        desc = kwargs.get('desc', '')
        messages = kwargs.get('messages', None)

        for col in df1.columns:
            col1 = df1[col]
            if not col in df2.columns:
                continue
            col2 = df2[col]

            for index in df1.index:
                val1 = col1[index]
                if not index in col2.index:
                    continue
                val2 = col2[index]

                error = abs(val1-val2)

                if error > (atol + rtol*abs(val1)):
                    msg = "mismatch comparing {4} col: {0} row: {1} here {2} != {3}".format(col, index, val1, val2, desc)
                    print(msg)
                    if not messages is None:
                        messages.append(msg)
                    logging.debug(msg)
                    return True

        return False



    def compare(self, expected, other, **kwargs):
        # type: (TestReport, TestReport) -> CompareResult
        raise NotImplementedError()

