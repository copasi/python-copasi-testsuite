from ReportParser import ReportParser


class ReportParserParameterEstimation(ReportParser):
    def __init__(self):
        ReportParser.__init__(self)

    def parseLines(self, lines):
        # type: ([str]) -> None
        current = self.skip_until(lines, 0, 'Objective Function Value')
        self.status = lines[current].strip()
        current = self.skip_until(lines, current, 'Parameter\tValue\tGradient\tStandard Deviation')
        if current == -1:
            return

        self.readDataFrameWithDescription(lines, current, {'desc': 'Parameter Estimation Result'},
                                          trim=True, index_col=0)
