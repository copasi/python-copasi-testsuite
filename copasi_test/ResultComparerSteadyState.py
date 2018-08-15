from ResultComparer import ResultComparer, CompareResult


class ResultComparerSteadyState(ResultComparer):
    def __init__(self):
        from TaskTypes import TaskTypes
        ResultComparer.__init__(self, TaskTypes.steadystate)

    def compare(self, expected, other, **kwargs):
        result = CompareResult(self)

        # compare status
        if expected.status != other.status:
            result.fail_with('Status different: {0} != {1}'.format(expected.status, other.status))

        # species result: concentration / concentration rate / particle numbers / particle number rate
        # expected_subset = self.get_subset(expected.data_frames[0], [0, 1, 2, 3])
        # other_subset = self.get_subset(other.data_frames[0], [0, 1, 2, 3])
        # species result: concentration
        expected_subset = self.get_subset(expected.data_frames[0], [0])
        other_subset = self.get_subset(other.data_frames[0], [0])
        diff = self.get_differences(expected_subset, other_subset, **kwargs)
        result.differences.append(diff)

        # compare steady state fluxes
        diff = self.get_differences(expected.data_frames[1], other.data_frames[1], **kwargs)
        result.differences.append(diff)

        # compare full jacobian
        result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[2],
                                                                                other.data_frames[2],
                                                                                desc="Full Jacobian",
                                                                                messages=result.messages, **kwargs)

        # compare full eigenvalues
        result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[3],
                                                                                other.data_frames[3],
                                                                                desc="Full Eigenvalues",
                                                                                messages=result.messages, **kwargs)

        return result
