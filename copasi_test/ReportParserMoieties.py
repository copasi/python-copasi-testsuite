from ReportParser import ReportParser


class ReportParserMoieties(ReportParser):
    def __init__(self):
        ReportParser.__init__(self)

    def parseLines(self, lines):
        # type: ([str]) -> None
        current = self.skip_until(lines, 0, 'Link matrix(ann)')
        if current == -1:
            return

        current = self.readAnnotatedMatrix(lines, current)
        current = self.skip_until(lines, current, 'Stoichiometry(ann)')
        if current == -1:
            return
        current = self.readAnnotatedMatrix(lines, current)
