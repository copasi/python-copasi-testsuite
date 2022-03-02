from .ResultComparer import ResultComparer, CompareResult

import logging

class ResultComparerSteadyState(ResultComparer):
    def __init__(self):
        from .TaskTypes import TaskTypes
        ResultComparer.__init__(self, TaskTypes.steadystate)

    def compare(self, expected, other, **kwargs):
        result = CompareResult(self)

        # compare status
        if expected.status != other.status:
            logging.debug('Status different: {0} != {1}'.format(expected.status, other.status))
            result.fail_with('  Status different: {0} != {1}'.format(expected.status, other.status))

        if 'No steady state with given resolution was found!' in expected.status:
            return result

        # species result: concentration / concentration rate / particle numbers / particle number rate
        # expected_subset = self.get_subset(expected.data_frames[0], [0, 1, 2, 3])
        # other_subset = self.get_subset(other.data_frames[0], [0, 1, 2, 3])
        # species result: concentration
        # print(self.case_id)

        if len(expected.data_frames) < 1:
            return result

        expected_subset = self.get_subset(expected.data_frames[0], [0])
        other_subset = self.get_subset(other.data_frames[0], [0])
        result.explicit_fail = result.explicit_fail or \
                               self.compare_df_unsorted(expected_subset,
                                                        other_subset,
                                                        desc=expected.data_descriptions[0]['desc'],
                                                        messages=result.messages, **kwargs)

        if len(expected.data_frames) < 2:
            return result

        # compare steady state fluxes
        result.explicit_fail = result.explicit_fail or \
                               self.compare_df_unsorted(expected.data_frames[1],
                                                        other.data_frames[1],
                                                        desc=expected.data_descriptions[1]['desc'],
                                                        messages=result.messages, **kwargs)

        if not result.explicit_fail:
            logging.debug('  results matched')


        # # compare full jacobian
        # result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[2],
        #                                                                         other.data_frames[2],
        #                                                                         desc="Full Jacobian",
        #                                                                         messages=result.messages, **kwargs)

        # # compare full eigenvalues
        # result.explicit_fail = result.explicit_fail or self.compare_df_unsorted(expected.data_frames[3],
        #                                                                         other.data_frames[3],
        #                                                                         desc="Full Eigenvalues",
        #                                                                         messages=result.messages, **kwargs)

        return result
