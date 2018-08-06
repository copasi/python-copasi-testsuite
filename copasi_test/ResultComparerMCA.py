from ResultComparer import CompareResult
from ResultComparerSteadyState import ResultComparerSteadyState

class ResultComparerMCA(ResultComparerSteadyState):
    def __init__(self):
        from TaskTypes import TaskTypes
        ResultComparerSteadyState.__init__(self)
        self.task_type = TaskTypes.mca

    def compare(self, expected, other, **kwargs):
        result = CompareResult()
        result.explicit_fail = result.explicit_fail or expected.status != other.status

        df1 = expected.get_data('Unscaled elasticity matrix')
        df2 = other.get_data('Unscaled elasticity matrix')
        if (not df1 is None) and (not df2 is None):
            result.explicit_fail = result.explicit_fail or \
                                   self.compare_df_unsorted(df1, df2,desc="Unscaled elasticity matrix",
                                                                     messages=result.messages)

        df1 = expected.get_data('Unscaled concentration control coefficients')
        df2 = other.get_data('Unscaled concentration control coefficients')
        if (not df1 is None) and (not df2 is None):
            result.explicit_fail = result.explicit_fail or \
                                   self.compare_df_unsorted(df1, df2,desc="Unscaled concentration control coefficients",
                                                                     messages=result.messages)

        df1 = expected.get_data('Unscaled flux control coefficients')
        df2 = other.get_data('Unscaled flux control coefficients')
        if (not df1 is None) and (not df2 is None):
            result.explicit_fail = result.explicit_fail or \
                                   self.compare_df_unsorted(df1, df2,desc="Unscaled flux control coefficients",
                                                                     messages=result.messages)


        return result

