import pandas

from ReportParser import ReportParser


class ReportParserTimeCourse(ReportParser):
    def __init__(self):
        ReportParser.__init__(self)

    def parseLines(self, lines):
        # type: ([str]) -> None
        df = pandas.read_csv(self.filename, sep='\t')
        df = df.set_index(df.columns[0])
        self.data_frames.append(df)
        self.data_descriptions.append({'desc': 'Time Course Report'})
