from ResultComparer import ResultComparer, CompareResult


class ResultComparerPE(ResultComparer):
    def __init__(self):
        from TaskTypes import TaskTypes
        ResultComparer.__init__(self, TaskTypes.parameterEstimation)

    def compare(self, expected, other, **kwargs):
        result = CompareResult(self)

        try:
            expected_obj = expected.status[expected.status.find(':') + 1:].strip()
            expected_obj = float(expected_obj)
            other_obj = other.status[other.status.find(':') + 1:].strip()
            other_obj = float(other_obj)

            result.explicit_fail = result.explicit_fail or self.compare_numbers(expected_obj,
                                                                                other_obj,
                                                                                desc="Objective Function Value",
                                                                                messages=result.messages, **kwargs)
        except:
            result.fail_with('No objective Value')

        result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[0],
                                                                                other.data_frames[0],
                                                                                desc="Parameter Estimation Result",
                                                                                messages=result.messages, **kwargs)

        return result
