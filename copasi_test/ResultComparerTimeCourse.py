from ResultComparer import ResultComparer, CompareResult


class ResultComparerTimeCourse(ResultComparer):
    def __init__(self):
        from TaskTypes import TaskTypes
        ResultComparer.__init__(self, TaskTypes.timecourse)

    def compare(self, expected, other, **kwargs):
        result = CompareResult(self)
        # compare csv files, ought to be identical
        # diff = self.get_differences(expected.data_frames[0], other.data_frames[0], **kwargs)
        # result.differences.append(diff)
        result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[0],
                                                                                other.data_frames[0],
                                                                                desc="Time Series",
                                                                                messages=result.messages, **kwargs)
        return result
