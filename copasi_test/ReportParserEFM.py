import pandas

from ReportParser import ReportParser

class ReportParserEFM(ReportParser):
    def __init__(self):
        ReportParser.__init__(self)


    def parseLines(self, lines):
        #type: ([str]) -> None
        current = 2
        self.status = lines[current].strip()


        # read list of modes
        current = self.skip_until(lines, current, '#\t\tReactions\tEquations')
        current = current + 1
        end = self.find_empty(lines, current)
        modes = []
        reversibility = []
        reactions = []
        equations = []
        last = -1
        for no in range(current, end):
            parts = lines[no].strip().split('\t')
            col1 = parts[0].strip()
            col2 = parts[1].strip()
            if len(parts) != 4:
                reactions[last] = reactions[last] + ' + ' + col1
                equations[last] = equations[last] + '; ' + col2
                continue
            col3 = parts[2].strip()
            col4 = parts[3].strip()
            if col1 != '':
                last = int(col1) -1
                modes.append(col1)
                reversibility.append(col2)
                reactions.append(col3)
                equations.append(col4)

        df = pandas.DataFrame({'Mode': modes, 'Reversibility': reversibility, 'Reactions': reactions, 'Equations': equations})
        df = df.set_index('Mode')
        self.data_frames.append(df)
        self.data_descriptions.append({'desc': "Flux modes"})
        current = end + 1

        # read net reactions
        current = self.skip_until(lines, current, '#\tNet Reaction\tInternal Species')
        current = current + 1
        end = self.find_empty(lines, current)
        modes = []
        species = []
        for no in range(current, end):
            parts = lines[no].strip().split('\t')
            if len(parts) != 3:
                continue
            modes.append(parts[0])
            species.append(parts[2])

        df = pandas.DataFrame({'Mode':modes, 'Internal Species': species})
        df = df.set_index('Mode')
        self.data_frames.append(df)
        self.data_descriptions.append({'desc': "Net Reactions"})
        current = end + 1


        # read efm vs reactions
        current = self.skip_until(lines, current, '#\t')
        current = self.readDataFrameWithDescription(lines, current, {'desc': "EFM vs Reactions"})

        # read efm vs species
        current = self.skip_until(lines, current, '#\t')
        self.readDataFrameWithDescription(lines, current, {'desc': "EFM vs Species"})
