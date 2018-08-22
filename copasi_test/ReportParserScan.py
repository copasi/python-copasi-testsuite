from ReportParser import ReportParser
import pandas


class ReportParserScan(ReportParser):
    def __init__(self):
        ReportParser.__init__(self)

    def parseLines(self, lines):
        # type: ([str]) -> None

        num_lines = len(lines)
        current = self.readDataFrameWithDescription(lines, 0, {"desc": "Scan Log"})

        first = self.data_frames[-1]
        assert (isinstance(first, pandas.DataFrame))

        if current == 0:
            # reached the end
            return

        count = 1

        while current + 1 < num_lines:

            # skip empty lines
            while lines[current].strip() == '':
                current += 1

            try:
                current = self.readDataFrameWithDescription(lines, current, {"desc": "Scan Log {0}".format(count)},
                                                        cols=first.columns)
                count += 1
            except:
                raise
