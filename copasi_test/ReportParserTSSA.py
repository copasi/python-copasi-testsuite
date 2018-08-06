from ReportParser import ReportParser
import pandas


class ReportParserTSSA(ReportParser):
    def __init__(self):
        ReportParser.__init__(self)

    def parseLines(self, lines):
        # type: ([str]) -> None

        current = self.skip_until(lines, 0, 'OutputStartTime:')
        if current == -1:
            return

        method = lines[current + 2].strip()
        method = method[method.find(':') + 1:].strip()
        self.method = method

        if method == 'ILDM (LSODA,Modified)':
            self.parseILDMModified(lines, current + 2)
        elif method == 'ILDM (LSODA,Deuflhard)':
            self.parseILDM(lines, current + 2)
        elif method == 'CSP (LSODA)':
            self.parseCSP(lines, current + 2)

    def parseCSP(self, lines, start):

        species = []

        current = self.skip_until(lines, start, 'Species:')
        while lines[current + 1].strip() != '':
            species.append(lines[current + 1].strip())
            current += 1

        reactions = []
        current = self.skip_until(lines, current, 'Reactions:')
        while lines[current + 1].strip() != '':
            reactions.append(lines[current + 1].strip())
            current += 1

        ts = '**************** Time step'
        ts1 = '****************  Time step'
        current = self.skip_until(lines, current, [ts, ts1])

        while current != -1:

            current = self.skip_until(lines, current, 'Number of fast modes:')
            num_fast = lines[current]
            num_fast = int(num_fast[num_fast.find(':') + 1:].strip())

            current = self.skip_until(lines, current, 'Time scales')
            if current == -1:
                continue
            current = self.readDataFrameWithDescription(lines, current+1, {'desc': 'Time scales'},
                                                        header=None, trim=True,
                                                        replacements=[['   ', '\t']])
            df = self.data_frames[len(self.data_frames) - 1]
            df.index = [num_fast]

            current = self.skip_until(lines, current, 'Radical Pointer')
            if current == -1:
                continue

            if not lines[current + 1].strip() == '':
                current = self.readDataFrameWithDescription(lines, current+1, {'desc': 'Radical Pointer'},
                                                            header=None, trim=True,
                                                            replacements=[['   ', '\t']])
                df = self.data_frames[len(self.data_frames) - 1]
                df.index = species
            else:
                self.data_frames.append(pandas.DataFrame())
                self.data_descriptions.append({'desc': 'Radical Pointer'})

            current = self.skip_until(lines, current, 'Participation Index')
            if current == -1:
                continue
            current = self.readDataFrameWithDescription(lines, current+1, {'desc': 'Participation Index'},
                                                        header=None, trim=True,
                                                        replacements=[['   ', '\t']])
            df = self.data_frames[len(self.data_frames) - 1]
            df.index = reactions

            current = self.skip_until(lines, current, [ts, ts1])

    def parseILDMModified(self, lines, start):
        ts = '**************** Time step'
        ts1 = '****************  Time step'
        current = self.skip_until(lines, start, [ts, ts1])

        while current != -1:
            current = self.skip_until(lines, current, 'Contribution of species to modes')
            if current == -1:
                continue
            current = self.readAnnotatedMatrix(lines, current, sep=' ', header=None, trim=True,
                                               replacements=[['(', ''], [':  ', ': '], ['):', '']])

            current = self.skip_until(lines, current, 'Modes distribution for species')
            if current == -1:
                continue
            current = self.readAnnotatedMatrix(lines, current, trim=True, replacements=[['  ', '\t']])

            current = self.skip_until(lines, current, 'Slow space')
            if current == -1:
                continue
            current = self.readAnnotatedMatrix(lines, current, trim=True, replacements=[['  ', '\t']])

            current = self.skip_until(lines, current, 'Fast space')
            if current == -1:
                continue
            current = self.readAnnotatedMatrix(lines, current, trim=True, replacements=[['  ', '\t']])

            current = self.skip_until(lines, current, [ts, ts1])

    def parseILDM(self, lines, start):

        ts = '**************** Time step'
        ts1 = '****************  Time step'
        current = self.skip_until(lines, start, [ts, ts1])

        while current != -1:
            current = self.skip_until(lines, current, 'Contribution of species to modes')
            if current == -1:
                continue
            current = self.readAnnotatedMatrix(lines, current, sep=' ', header=None, trim=True,
                                               replacements=[['(', ''], [':  ', ': '], ['):', '']])

            current = self.skip_until(lines, current, 'Modes distribution for species')
            if current == -1:
                continue
            current = self.readAnnotatedMatrix(lines, current, trim=True, replacements=[['  ', '\t']])

            current = self.skip_until(lines, current, 'Slow space')
            if current == -1:
                continue
            current = self.readAnnotatedMatrix(lines, current, trim=True, replacements=[['  ', '\t']])

            current = self.skip_until(lines, current, 'Fast space')
            if current == -1:
                continue
            current = self.readAnnotatedMatrix(lines, current, trim=True, replacements=[['  ', '\t']])

            current = self.skip_until(lines, current, 'Reactions slow space')
            if current == -1:
                continue
            current = self.readAnnotatedMatrix(lines, current, trim=True, header=None, replacements=[['  ', '\t']])

            current = self.skip_until(lines, current, [ts, ts1])
