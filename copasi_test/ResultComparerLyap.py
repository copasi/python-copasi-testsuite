from .ResultComparer import ResultComparer, CompareResult


class ResultComparerLyap(ResultComparer):
    def __init__(self):
        from .TaskTypes import TaskTypes
        ResultComparer.__init__(self, TaskTypes.lyap)

    def compare(self, expected, other, **kwargs):
        result = CompareResult(self)

        if len(other.data_frames) != len(expected.data_frames):
            result.fail_with('Different number of results returned')
            return

        result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[0],
                                                                                other.data_frames[0],
                                                                                desc="Lyapunov Exponent",
                                                                                messages=result.messages, **kwargs)

        result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[1],
                                                                                other.data_frames[1],
                                                                                desc="Average divergence",
                                                                                messages=result.messages, **kwargs)

        return result
