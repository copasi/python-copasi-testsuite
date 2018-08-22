from ResultComparer import ResultComparer, CompareResult


class ResultComparerScan(ResultComparer):
    def __init__(self):
        from TaskTypes import TaskTypes
        ResultComparer.__init__(self, TaskTypes.timecourse)

    def compare(self, expected, other, **kwargs):
        result = CompareResult(self)

        if expected.status != other.status:
            result.fail_with('Status differs')
            return result

        num_dataframes = expected.num_dataframes()
        if num_dataframes != other.num_dataframes():
            result.fail_with('different number of data sets')
            return result

        for i in range(num_dataframes):
            result.explicit_fail = result.explicit_fail or \
                                   self.compare_df_unsorted(expected.data_frames[i],
                                                            other.data_frames[i],
                                                            desc=other.data_descriptions[i]['desc'],
                                                            messages=result.messages, **kwargs)
        return result
