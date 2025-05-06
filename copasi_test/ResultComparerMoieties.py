from .ResultComparer import ResultComparer, CompareResult


class ResultComparerMoieties(ResultComparer):
    def __init__(self):
        from .TaskTypes import TaskTypes
        ResultComparer.__init__(self, TaskTypes.timecourse)

    def compare(self, expected, other, **kwargs):
        result = CompareResult(self)


        # link matrices can be different due to different order of species
        # result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[0],
        #                                                                        other.data_frames[0],
        #                                                                        desc="Link matrix(ann)",
        #                                                                        messages=result.messages, **kwargs)
        
        import numpy as np
        
        trace_exp = np.trace(expected.data_frames[0].to_numpy())
        trace_other = np.trace(other.data_frames[0].to_numpy())
        if abs(trace_exp - trace_other) > 1e-6:
            result.explicit_fail = True
            result.messages.append(f"Trace of link matrix differs: {trace_exp} != {trace_other}")
        

        result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[1],
                                                                                other.data_frames[1],
                                                                                desc="Stoichiometry(ann)",
                                                                                messages=result.messages, **kwargs)
        return result
