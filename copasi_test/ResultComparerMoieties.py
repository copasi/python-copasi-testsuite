from ResultComparer import ResultComparer, CompareResult


class ResultComparerMoieties(ResultComparer):
    def __init__(self):
        from TaskTypes import TaskTypes
        ResultComparer.__init__(self, TaskTypes.timecourse)

    def compare(self, expected, other, **kwargs):
        result = CompareResult(self)

        result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[0],
                                                                                other.data_frames[0],
                                                                                desc="Link matrix(ann)",
                                                                                messages=result.messages, **kwargs)

        result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[1],
                                                                                other.data_frames[1],
                                                                                desc="Stoichiometry(ann)",
                                                                                messages=result.messages, **kwargs)
        return result
