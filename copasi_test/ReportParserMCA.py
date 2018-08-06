from ReportParser import ReportParser
from ReportParserSteadyState import ReportParserSteadyState

class ReportParserMCA(ReportParser):
    def __init__(self):
        ReportParser.__init__(self)


    def parseLines(self, lines):
        #type: ([str]) -> None
        current = self.skip_until(lines, 0, 'Metabolic Control Analysis Result:')
        if current == -1:
            return self
        current += 2

        # read status
        self.status = lines[current].strip()

        # read unscaled elasticities
        current = self.skip_until(lines, current, 'Unscaled elasticities')
        if current == -1:
            return self
        current = self.readAnnotatedMatrix(lines, current)

        # read scaled elasticities
        current = self.skip_until(lines, current, 'Scaled elasticities')
        if current == -1:
            return self
        current = self.readAnnotatedMatrix(lines, current)

        # read Unscaled concentration control coefficients
        current = self.skip_until(lines, current, 'Unscaled concentration control coefficients')
        if current == -1:
            return self
        current = self.readAnnotatedMatrix(lines, current)

        # read Scaled concentration control coefficients
        current = self.skip_until(lines, current, 'Scaled concentration control coefficients')
        if current == -1:
            return self
        current = self.readAnnotatedMatrix(lines, current)

        # read Unscaled flux control coefficients
        current = self.skip_until(lines, current, 'Unscaled flux control coefficients')
        if current == -1:
            return self
        current = self.readAnnotatedMatrix(lines, current)

        # read Scaled flux control coefficients
        current = self.skip_until(lines, current, 'Scaled flux control coefficients')
        if current == -1:
            return self
        current = self.readAnnotatedMatrix(lines, current)

        # read steady state result
        current = self.skip_until(lines, current,
                                  'Results of the steady state subtask (the state for which the MCA was performed):')
        if current == -1:
            return self

        steadyState = ReportParserSteadyState()
        steadyState.parseLines(lines[current + 1:])
        self.appendResults(steadyState)
