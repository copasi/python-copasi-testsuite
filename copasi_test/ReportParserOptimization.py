import pandas
from ReportParser import ReportParser


class ReportParserOptimization(ReportParser):
    def __init__(self):
        ReportParser.__init__(self)

    def parseLines(self, lines):
        # type: ([str]) -> None
        current = self.skip_until(lines, 0, 'Objective Function Value')
        if current != -1:
            self.status = lines[current].strip()
        else:
            current = 0
        current = self.skip_until(lines, current, 'Evaluations/Second')
        if current == -1:
            return

        block_lines = ['OptItem: Value'] + self.get_next_block(lines, current+2)
        for i in range(len(block_lines)):
            block_lines[i] = block_lines[i] + '\n'
        block = self.get_block_as_buffer(block_lines, 0, len(block_lines))
        df = pandas.read_csv(block, sep=':')
        df = df.set_index(df.columns[0])
        self.data_frames.append(df)
        self.data_descriptions.append({'desc': 'Optimization Result'})
