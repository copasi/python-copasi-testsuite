from ResultComparer import ResultComparer, CompareResult

class ResultComparerTssa(ResultComparer):
    def __init__(self):
        from TaskTypes import TaskTypes
        ResultComparer.__init__(self, TaskTypes.tssa)

    def compare_ildm(self, expected, other, **kwargs):
        result = CompareResult()
        if len(expected.data_frames) != len(other.data_frames):
            result.explicit_fail = True
            result.messages.append('dimensions differ')
            return result

        for i in range(0, len(expected.data_frames),5):

            diff = self.get_differences(expected.data_frames[i+0], other.data_frames[i+0], **kwargs)
            result.differences.append(diff)
            diff = self.get_differences(expected.data_frames[i+1], other.data_frames[i+1], **kwargs)
            result.differences.append(diff)
            diff = self.get_differences(expected.data_frames[i+2], other.data_frames[i+2], **kwargs)
            result.differences.append(diff)
            diff = self.get_differences(expected.data_frames[i+3], other.data_frames[i+3], **kwargs)
            result.differences.append(diff)
            diff = self.get_differences(expected.data_frames[i+4], other.data_frames[i+4], **kwargs)
            result.differences.append(diff)

        return result


    def compare_modified_ildm(self, expected, other, **kwargs):
        result = CompareResult()

        if len(expected.data_frames) != len(other.data_frames):
            result.explicit_fail = True
            result.messages.append('dimensions differ')
            return result

        for i in range(0, len(expected.data_frames),4):

            diff = self.get_differences(expected.data_frames[i+0], other.data_frames[i+0], **kwargs)
            result.differences.append(diff)
            diff = self.get_differences(expected.data_frames[i+1], other.data_frames[i+1], **kwargs)
            result.differences.append(diff)
            diff = self.get_differences(expected.data_frames[i+2], other.data_frames[i+2], **kwargs)
            result.differences.append(diff)
            diff = self.get_differences(expected.data_frames[i+3], other.data_frames[i+3], **kwargs)
            result.differences.append(diff)

        return result

    def compare_csp(self, expected, other, **kwargs):
        result = CompareResult()
        if len(expected.data_frames) != len(other.data_frames):
            result.explicit_fail = True
            result.messages.append('dimensions differ')
            return result

        for i in range(0, len(expected.data_frames),3):
            if i + 3 < len(expected.data_frames):
                break
            diff = self.get_differences(expected.data_frames[i + 0], other.data_frames[i + 0], **kwargs)
            result.differences.append(diff)
            diff = self.get_differences(expected.data_frames[i + 1], other.data_frames[i + 1], **kwargs)
            result.differences.append(diff)
            diff = self.get_differences(expected.data_frames[i + 2], other.data_frames[i + 2], **kwargs)
            result.differences.append(diff)

        return result

    def compare(self, expected, other, **kwargs):

        if expected.method != other.method:
            result = CompareResult()
            result.explicit_fail = True
            result.messages.append('Different method used: {0} != {1}'.format(expected.method, other.method))
            return result

        if expected.method == 'ILDM (LSODA,Modified)':
            return self.compare_modified_ildm(expected, other, **kwargs)
        elif expected.method == 'ILDM (LSODA,Deuflhard)':
            return self.compare_ildm(expected, other, **kwargs)
        elif expected.method == 'CSP (LSODA)':
            return self.compare_csp(expected, other, **kwargs)

        return CompareResult()

