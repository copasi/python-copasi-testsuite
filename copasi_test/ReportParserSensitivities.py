from ReportParser import ReportParser


class ReportParserSensitivities(ReportParser):
    def __init__(self):
        ReportParser.__init__(self)

    def parseLines(self, lines):
        # type: ([str]) -> None
        # Sensitivities array
        current = self.skip_until(lines, 0, 'Sensitivities array')
        current = self.readAnnotatedMatrix(lines, current)

        current = self.skip_until(lines, current, 'Scaled sensitivities array')
        self.readAnnotatedMatrix(lines, current)
