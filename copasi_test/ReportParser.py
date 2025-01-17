import pandas
import numpy

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

from .TestReport import TestReport


class ReportParser:

    def __init__(self):
        self.data_frames = []
        self.data_descriptions = []
        self.status = ''
        self.description = ''
        self.stability = ''
        self.content = ''
        self.filename = ''
        self.task_type = ''
        self.method = None
        self.problem = None
        self.task = None

    def appendResults(self, parser):
        # type: (ReportParser) -> None
        self.data_descriptions += parser.data_descriptions
        self.data_frames += parser.data_frames

    def applyToReport(self, report):
        # type: (TestReport) -> None

        report.content = self.content
        report.data_frames = self.data_frames
        report.data_descriptions = self.data_descriptions
        report.description = self.description
        report.status = self.status
        report.stability = self.stability
        report.method = self.method

    def parserFile(self, file_name):
        self.filename = file_name
        with open(self.filename, 'r', encoding='utf-8') as report_file:
            lines = report_file.readlines()
        self.parseLines(lines)

    def parseLines(self, lines):
        # type: ([str]) -> None
        raise NotImplementedError()

    @staticmethod
    def find_empty(lines, current):
        # type: ([str], int) -> int
        for i in range(current, len(lines)):
            if lines[i].strip() == '':
                return i
        return -1

    @staticmethod
    def skip_until(lines, current, marker):
        # type: ([str], int, str|[str]) -> int
        for i in range(current, len(lines)):
            if type(marker) is list:
                for mark in marker:
                    if lines[i].strip().startswith(mark):
                        return i
            else:
                if lines[i].strip().startswith(marker):
                    return i
        return -1

    @staticmethod
    def get_block_as_buffer(lines, start, end, trim=False, replacements=None):
        # type: ([str], int, int) -> StringIO
        result = StringIO()
        for line in lines[start:end]:
            line = line.replace('1.#INF', 'inf')
            line = line.replace('1.#QNAN', 'nan')
            line = line.replace('1.#SNAN', 'nan')
            line = line.replace('1.#IND', 'nan')
            if replacements is not None:
                for rep in replacements:
                    line = line.replace(rep[0], rep[1])
            if trim:
                line = line.strip() + '\n'
            result.write(line)
        result.seek(0)
        return result

    @staticmethod
    def get_next_block(lines, start):
        # type: ([str], int) -> [str]
        result = []
        for i in range(start, len(lines)):
            current = lines[i].strip()
            if current == '':
                return result
            result.append(current)

        return result

    def readAnnotatedMatrix(self, lines, current, **kwargs):
        # type: ([str], int) -> int
        max_lines = len(lines)
        if current == max_lines:
            return current

        sep = kwargs.get('sep', '\t')
        header = kwargs.get('header', 'infer')
        trim = kwargs.get('trim', False)
        replacements = kwargs.get('replacements', None)
        name = lines[current].strip()
        current = current + 1
        if current >= max_lines:
            return current
        description = lines[current].strip()
        current = current + 1
        if description == '':
            description = name
        if description.startswith('Rows :') or description.startswith('Rows:'):
            current = current - 1
            description = name
        rows = lines[current]
        rows = rows[rows.find(':') + 1:].strip()
        cols = lines[current + 1]
        cols = cols[cols.find(':') + 1:].strip()
        end = self.find_empty(lines, current)
        block = self.get_block_as_buffer(lines, current + 2, end, trim=trim, replacements=replacements)
        
        if len(block.getvalue()) == 0:
            return current

        df = pandas.read_csv(block, sep=sep,  header=header)
        
        type_indices = df.dtypes.index.to_list()
        types = df.dtypes

        if types[type_indices[0]] == object:
            df = df.set_index(type_indices[0])

        for i in range(len(types)):
            current_type = types[type_indices[i]]
            if current_type == numpy.int64:
                df[type_indices[i]] = df[type_indices[i]].astype(numpy.float64)

        self.data_frames.append(df)
        self.data_descriptions.append({'desc': description, 'name': name, 'rows': rows, 'cols': cols})
        current = end + 1
        return current

    def readDataFrameWithDescription(self, lines, current, desc, **kwargs):
        # type: ([str], int, {}) -> int
        max_lines = len(lines)
        if current == max_lines:
            return current
        sep = kwargs.get('sep', '\t')
        header = kwargs.get('header', 'infer')
        trim = kwargs.get('trim', False)
        replacements = kwargs.get('replacements', None)
        cols = kwargs.get('cols', None)
        index_col = kwargs.get('index_col', -1)
        end = self.find_empty(lines, current)
        block = self.get_block_as_buffer(lines, current, end, trim=trim, replacements=replacements)

        if len(block.getvalue()) == 0:
            return current


        df = pandas.read_csv(block, sep=sep, header=header)
        if index_col != -1:
            df = df.set_index(df.columns[index_col])

        if cols is not None:
            df.columns = cols

        self.data_frames.append(df)
        self.data_descriptions.append(desc)
        current = end + 1
        return current
