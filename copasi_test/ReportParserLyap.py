import pandas
from .ReportParser import ReportParser


class ReportParserLyap(ReportParser):
    def __init__(self):
        ReportParser.__init__(self)

    def parseLines(self, lines):
        # type: ([str]) -> None
        current = self.skip_until(lines, 0, 'Lyapunov Exponents:')
        if current == -1:
            return
        exponents_string = lines[current + 1].strip().split(' ')
        exponents = [float(x) for x in exponents_string]
        df = pandas.DataFrame(exponents, columns=['Exponents'])
        self.data_frames.append(df)
        self.data_descriptions.append({'desc': 'Lyapunov Exponents'})

        current = self.skip_until(lines, current + 1, 'Average divergence:')
        if current == -1:
            return
        divergence = float(lines[current].split(':')[1].strip())
        df = pandas.DataFrame([divergence], columns=['Average divergence'])
        self.data_frames.append(df)
        self.data_descriptions.append({'desc': 'Average divergence'})
