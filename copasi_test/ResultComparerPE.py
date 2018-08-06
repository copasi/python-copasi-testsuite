from ResultComparer import ResultComparer, CompareResult


class ResultComparerPE(ResultComparer):
    def __init__(self):
        from TaskTypes import TaskTypes
        ResultComparer.__init__(self, TaskTypes.parameterEstimation)

    def compare(self, expected, other, **kwargs):
        result = CompareResult()
        # compare csv files, ought to be identical
        diff = self.get_differences(expected.data_frames[0], other.data_frames[0], **kwargs)
        result.differences.append(diff)
        return result
