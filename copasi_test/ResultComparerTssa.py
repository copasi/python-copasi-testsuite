from .ResultComparer import ResultComparer, CompareResult


class ResultComparerTssa(ResultComparer):
    def __init__(self):
        from .TaskTypes import TaskTypes
        ResultComparer.__init__(self, TaskTypes.tssa)

    def compare_ildm(self, expected, other, **kwargs):
        result = CompareResult(self)
        if len(expected.data_frames) != len(other.data_frames):
            result.fail_with('dimensions differ')
            return result

        for i in range(0, len(expected.data_frames), 5):
            result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[i+0],
                                                                                    other.data_frames[i+0],
                                                                                    desc="Contribution of species to modes",
                                                                                    messages=result.messages, **kwargs)

            result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[i+1],
                                                                                    other.data_frames[i+1],
                                                                                    desc="Modes distribution for species",
                                                                                    messages=result.messages, **kwargs)

            result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[i+2],
                                                                                    other.data_frames[i+2],
                                                                                    desc="Slow space",
                                                                                    messages=result.messages, **kwargs)

            result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[i+3],
                                                                                    other.data_frames[i+3],
                                                                                    desc="Fast space",
                                                                                    messages=result.messages, **kwargs)

            result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[i+4],
                                                                                    other.data_frames[i+4],
                                                                                    desc="Reactions slow space",
                                                                                    messages=result.messages, **kwargs)

        return result

    def compare_modified_ildm(self, expected, other, **kwargs):
        result = CompareResult(self)

        if len(expected.data_frames) != len(other.data_frames):
            result.fail_with('dimensions differ')
            return result

        for i in range(0, len(expected.data_frames), 4):
            result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[i + 0],
                                                                                    other.data_frames[i + 0],
                                                                                    desc="Contribution of species to modes",
                                                                                    messages=result.messages, **kwargs)

            result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[i + 1],
                                                                                    other.data_frames[i + 1],
                                                                                    desc="Modes distribution for species",
                                                                                    messages=result.messages, **kwargs)

            result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[i + 2],
                                                                                    other.data_frames[i + 2],
                                                                                    desc="Slow space",
                                                                                    messages=result.messages, **kwargs)

            result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[i + 3],
                                                                                    other.data_frames[i + 3],
                                                                                    desc="Fast space",
                                                                                    messages=result.messages, **kwargs)

        return result

    def compare_csp(self, expected, other, **kwargs):
        result = CompareResult(self)
        if len(expected.data_frames) != len(other.data_frames):
            result.fail_with('dimensions differ')
            return result

        for i in range(0, len(expected.data_frames), 3):
            if i + 3 < len(expected.data_frames):
                break
            result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[i + 0],
                                                                                    other.data_frames[i + 0],
                                                                                    desc="Time scales",
                                                                                    messages=result.messages, **kwargs)

            result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[i + 1],
                                                                                    other.data_frames[i + 1],
                                                                                    desc="Radical Pointer",
                                                                                    messages=result.messages, **kwargs)

            result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[i + 2],
                                                                                    other.data_frames[i + 2],
                                                                                    desc="Participation Index",
                                                                                    messages=result.messages, **kwargs)

        return result

    def compare(self, expected, other, **kwargs):

        if expected.method != other.method:
            result = CompareResult(self)
            result.fail_with('Different method used: {0} != {1}'.format(expected.method, other.method))
            return result

        if expected.method == 'ILDM (LSODA,Modified)':
            return self.compare_modified_ildm(expected, other, **kwargs)
        elif expected.method == 'ILDM (LSODA,Deuflhard)':
            return self.compare_ildm(expected, other, **kwargs)
        elif expected.method == 'CSP (LSODA)':
            return self.compare_csp(expected, other, **kwargs)

        return CompareResult()
