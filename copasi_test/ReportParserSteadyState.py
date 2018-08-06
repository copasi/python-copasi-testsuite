from ReportParser import ReportParser


class ReportParserSteadyState(ReportParser):
    def __init__(self):
        ReportParser.__init__(self)

    def parseLines(self, lines):
        # type: ([str]) -> None

        current = 0

        # read status
        self.status = lines[current].strip()

        # read steady state species
        current = self.skip_until(lines, 0, 'Species	Concentration')
        current = self.readDataFrameWithDescription(lines, current, {'desc': 'steady state species information'})
        self.data_frames[-1] = self.data_frames[-1].set_index('Species')

        # read steady state fluxes
        current = self.readDataFrameWithDescription(lines, current, {'desc': 'steady state flux information'})
        self.data_frames[-1] = self.data_frames[-1].set_index('Reaction')

        # read jacobian
        current = self.readAnnotatedMatrix(lines, current)

        # read eigenvalues
        current = self.readDataFrameWithDescription(lines, current, {'desc': 'Eigenvalues (complete system)'},
                                                    trim=True, replacements=[['Eigenvalues\treal', 'real']])

        # read reduced jacobian
        current = self.readAnnotatedMatrix(lines, current)

        # read eigenvalues
        current = self.readDataFrameWithDescription(lines, current, {'desc': 'Eigenvalues (reduced system)'},
                                                    trim=True, replacements=[['Eigenvalues\treal', 'real']])

        # store stability analysis
        block = ''.join(lines[current:])
        self.stability = block
