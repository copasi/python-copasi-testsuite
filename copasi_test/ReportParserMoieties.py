from ReportParser import ReportParser

class ReportParserMoieties(ReportParser):
    def __init__(self):
        ReportParser.__init__(self)


    def parseLines(self, lines):
        #type: ([str]) -> None
        raise NotImplementedError()