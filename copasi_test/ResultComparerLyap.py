from ResultComparer import ResultComparer, CompareResult


class ResultComparerLyap(ResultComparer):
    def __init__(self):
        from TaskTypes import TaskTypes
        ResultComparer.__init__(self, TaskTypes.lyap)

    def compare(self, expected, other, **kwargs):
        result = CompareResult(self)

        if len(other.data_frames) != len(expected.data_frames):
            result.fail_with('Different number of results returned')
            return

        # compare csv files, ought to be identical
        diff = self.get_differences(expected.data_frames[0], other.data_frames[0], **kwargs)
        result.differences.append(diff)
        diff = self.get_differences(expected.data_frames[1], other.data_frames[1], **kwargs)
        result.differences.append(diff)
        return result
