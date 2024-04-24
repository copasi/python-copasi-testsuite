from .TestReport import TestReport
from .RunResult import RunResult
import numpy as np
import pandas
import logging


class CompareResult:
    def __init__(self, comparer=None):
        self.differences = []
        self.run_result = None
        self.explicit_fail = False
        self.messages = []
        self.changes = []
        self.comparer = comparer
        self.case_id = "" if comparer is None else comparer.case_id

    def fail_with(self, msg):
        self.explicit_fail = True
        if self.case_id and self.case_id not in msg:
            self.messages.append(self.case_id + " - " + msg)
        else:
            self.messages.append(msg)

    def get_run_result(self):
        # type: () -> RunResult

        for msg in self.messages:
            logging.error(msg)

        if self.explicit_fail:
            return RunResult.FAIL

        for df in self.differences:
            assert (isinstance(df, pandas.DataFrame))
            try:
                if df.any().any():
                    logging.error(df.describe())
                    self.changes.append(df.any())
                    return RunResult.FAIL
            except:
                print(df)
                if df.any():
                    logging.error(df.describe())
                    self.changes.append(df.any())
                    return RunResult.FAIL

        return RunResult.PASS


class ResultComparer:
    def __init__(self, task_type=None):
        self.task_type = task_type
        self.expected = None
        self.other = None
        self.case_id = ""

    @staticmethod
    def get_differences(df1, df2, expected=None, **kwargs):
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

    def compare_numbers(self, val1, val2, **kwargs):
        atol = kwargs.get('atol', 0.0001)
        rtol = kwargs.get('rtol', 0.0001)
        desc = kwargs.get('desc', '')
        messages = kwargs.get('messages', None)

        error = abs(val1 - val2)

        if error > (atol + rtol * abs(val1)):
            msg = "mismatch comparing {0} numbers: {1} != {2}" \
                .format(desc, val1, val2)
            if messages is not None:
                if self.case_id:
                    messages.append(self.case_id + " - " + msg)
                else:
                    messages.append(msg)

            return True

        return False

    @staticmethod
    def compare_df_testsuite(df1, df2, expected=None, **kwargs):
        if expected is None:
            expected = df1

        atol = kwargs.get('atol', 0.0001)
        rtol = kwargs.get('rtol', 0.0001)

        diff = (np.abs(df1 - df2) <= atol + rtol * np.abs(df1))
        have_error = (diff == False)
        if have_error.any().any():
            return None
        return expected[have_error]

    def compare_df_unsorted(self, df1, df2, **kwargs):
        # type: (pandas.DataFrame, pandas.DataFrame)->pandas.DataFrame
        """
            compares two data frames based on their column and row indices, that way the comparison
            will work even if the indices are in a different order

        :param df1: first data frame
        :param df2: second data frame
        :param kwargs: optional parameters
        :return: boolean indicating whether the datasets match
        """

        atol = kwargs.get('atol', 0.0001)
        rtol = kwargs.get('rtol', 0.0001)
        desc = kwargs.get('desc', '')
        messages = kwargs.get('messages', None)

        for col in df1.columns:
            col1 = df1[col]
            if col not in df2.columns:
                continue
            col2 = df2[col]

            for index in df1.index:
                if pandas.isna(index):
                    continue
                val1 = col1[index]
                if type(val1) is str and 'nan' in val1: 
                    val1 = np.nan
                if isinstance(val1, pandas.Series):
                    if val1.dtype != np.float64:
                        val1 = val1.astype(np.float64)
                else: 
                    val1 = float(val1)
                if index not in col2.index:
                    continue
                val2 = col2[index]
                if type(val2) is str and 'nan' in val2: 
                    val2 = np.nan

                if isinstance(val2, pandas.Series):
                    if val2.dtype != np.float64:
                        val2 = val2.astype(np.float64)
                else: 
                    val2 = float(val2)

                error = abs(val1-val2)

                if isinstance(error, pandas.Series):
                    if (error > (atol + rtol*abs(val1))).any():
                        msg = "mismatch comparing {0} col: {1} row: {2}" \
                            .format(desc, col, index)
                        if messages is not None:
                            if self.case_id:
                                messages.append(self.case_id + " - " + msg)
                            else:
                                messages.append(msg)
                        return True
                    return False

                if error > (atol + rtol*abs(val1)):
                    msg = "mismatch comparing {4} col: {0} row: {1} here {2} != {3}"\
                        .format(col, index, val1, val2, desc)

                    if messages is not None:
                        if self.case_id:
                            messages.append(self.case_id + " - " + msg)
                        else:
                            messages.append(msg)
                    return True

        return False

    def compare(self, expected, other, **kwargs):
        # type: (TestReport, TestReport) -> CompareResult
        raise NotImplementedError()
