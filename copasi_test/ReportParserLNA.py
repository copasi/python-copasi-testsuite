from .ReportParser import ReportParser
from .ReportParserSteadyState import ReportParserSteadyState


class ReportParserLNA(ReportParser):
    def __init__(self):
        ReportParser.__init__(self)

    def parseLines(self, lines):
        # type: ([str]) -> None
        current = self.skip_until(lines, 0, 'Covariance matrix')
        if current == -1:
            return

        self.readAnnotatedMatrix(lines, current)

        current = self.skip_until(lines, current, 'Results of the steady state subtask')
        if current == -1:
            return
        try: 
            # as it turns out, the results from the steady state subtask 
            # were broken in some releases
            steadyState = ReportParserSteadyState()
            steadyState.parseLines(lines[current + 1:])
            self.appendResults(steadyState)
        except IndexError:
            return
