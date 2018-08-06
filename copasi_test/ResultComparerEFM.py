from ResultComparer import ResultComparer, CompareResult

class ResultComparerEFM(ResultComparer):
    def __init__(self):
        from TaskTypes import TaskTypes
        ResultComparer.__init__(self, TaskTypes.efm)

    @staticmethod
    def compare_rows(row1, row2):
        for i in range(len(row1)):
            if row1[i] != row2[i]:
                #print('{0} != {1}'.format(self.row_to_str(row1), self.row_to_str(row2)))
                return False

        #print('{0} == {1}'.format(self.row_to_str(row1),self.row_to_str(row2)))
        return True

    def find_row_in_df(self, row1, df, columns):
        # type: ([], pandas.DataFrame, []) -> bool

        for row in range(len(df)):
            # get row data
            row_data = []
            for col in range(1, len(columns)):
                row_data.append(df[columns[col]][row])
            # compare against the given one
            if self.compare_rows(row1, row_data):
                return True

        return False

    @staticmethod
    def row_to_str(row):
        data_string = ''
        for i in row:
            data_string += str(i) + ' '
        return data_string

    def compare(self, expected, other, **kwargs):
        result = CompareResult()

        df_exp = expected.data_frames[2]
        df_other = other.data_frames[2]

        if len(df_exp) != len(df_other):
            result.explicit_fail = True
            return result

        for row in range(len(df_exp)):
            row_data = []
            for col in range(1, len(df_exp.columns)):
                row_data.append(df_exp[df_exp.columns[col]][row])

            row_in_other = self.find_row_in_df(row_data, df_other, df_exp.columns)
            result.explicit_fail = result.explicit_fail or not row_in_other

            if not row_in_other:
                result.messages.append('Missing row: {0}'.format(self.row_to_str(row_data)))


        return result

