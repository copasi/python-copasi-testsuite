from .ResultComparer import ResultComparer, CompareResult


class ResultComparerLNA(ResultComparer):
    def __init__(self):
        from .TaskTypes import TaskTypes
        ResultComparer.__init__(self, TaskTypes.timecourse)

    def compare(self, expected, other, **kwargs):
        result = CompareResult(self)
        result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[0],
                                                                                other.data_frames[0],
                                                                                desc="Covariance matrix",
                                                                                messages=result.messages, **kwargs)
        return result
