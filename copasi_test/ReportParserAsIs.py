from ReportParser import ReportParser


class ReportParserAsIs(ReportParser):
    def __init__(self):
        ReportParser.__init__(self)

    def parseLines(self, lines):
        # type: ([str]) -> None
        self.content = self.get_next_block(lines, 0)
