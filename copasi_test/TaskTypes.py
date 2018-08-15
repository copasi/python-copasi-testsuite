from ReportParser import ReportParser
from ReportParserSteadyState import ReportParserSteadyState
from ReportParserTimeCourse import ReportParserTimeCourse
from ReportParserScan import ReportParserScan
from ReportParserEFM import ReportParserEFM
from ReportParserOptimization import ReportParserOptimization
from ReportParserParameterEstimation import ReportParserParameterEstimation
from ReportParserMCA import ReportParserMCA
from ReportParserLyap import ReportParserLyap
from ReportParserTSSA import ReportParserTSSA
from ReportParserSensitivities import ReportParserSensitivities
from ReportParserMoieties import ReportParserMoieties
from ReportParserCrossSection import ReportParserCrossSection
from ReportParserLNA import ReportParserLNA
from ReportParserAsIs import ReportParserAsIs
from ReportParserXML import ReportParserXML


from ResultComparer import ResultComparer
from ResultComparerSteadyState import ResultComparerSteadyState
from ResultComparerTimeCourse import ResultComparerTimeCourse
from ResultComparerMCA import ResultComparerMCA
from ResultComparerEFM import ResultComparerEFM
from ResultComparerOptimization import ResultComparerOptimization
from ResultComparerPE import ResultComparerPE
from ResultComparerLyap import ResultComparerLyap
from ResultComparerTssa import ResultComparerTssa
from ResultComparerSensitivities import ResultComparerSensitivities
from ResultComparerMoieties import ResultComparerMoieties


class TaskTypes:
    def __init__(self):
        pass

    steadystate = 'Steady-State'
    timecourse = 'Time-Course'
    scan = 'Scan'
    efm = 'Elementary Flux Modes'
    optimization = 'Optimization'
    parameterEstimation = 'Parameter Estimation'
    mca = 'Metabolic Control Analysis'
    lyap = 'Lyapunov Exponents'
    tssa = 'Time Scale Separation Analysis'
    sensitivities = 'Sensitivities'
    moieties = 'Moieties'
    crossSection = 'Cross Section'
    lna = 'Linear Noise Approximation'
    asIs = 'as-is'
    exportSBML = 'sbml export'

    @staticmethod
    def getParser(task_type):
        # type: (str) -> ReportParser
        parser = {
            TaskTypes.steadystate: ReportParserSteadyState(),
            TaskTypes.timecourse: ReportParserTimeCourse(),
            TaskTypes.scan: ReportParserScan(),
            TaskTypes.efm: ReportParserEFM(),
            TaskTypes.optimization: ReportParserOptimization(),
            TaskTypes.parameterEstimation: ReportParserParameterEstimation(),
            TaskTypes.mca: ReportParserMCA(),
            TaskTypes.lyap: ReportParserLyap(),
            TaskTypes.tssa: ReportParserTSSA(),
            TaskTypes.sensitivities: ReportParserSensitivities(),
            TaskTypes.moieties: ReportParserMoieties(),
            TaskTypes.crossSection: ReportParserTimeCourse(),
            TaskTypes.lna: ReportParserLNA(),
            TaskTypes.exportSBML: ReportParserXML(),
            TaskTypes.asIs: ReportParserAsIs()
        }.get(task_type, ReportParserAsIs())

        if parser is not None:
            parser.task_type = task_type

        return parser

    @staticmethod
    def getComparer(task_type):
        # type: (str) -> ResultComparer
        parser = {
            TaskTypes.steadystate: ResultComparerSteadyState(),
            TaskTypes.timecourse: ResultComparerTimeCourse(),
            TaskTypes.scan: ResultComparer(),
            TaskTypes.efm: ResultComparerEFM(),
            TaskTypes.optimization: ResultComparerOptimization(),
            TaskTypes.parameterEstimation: ResultComparerPE(),
            TaskTypes.mca: ResultComparerMCA(),
            TaskTypes.lyap: ResultComparerLyap(),
            TaskTypes.tssa: ResultComparerTssa(),
            TaskTypes.sensitivities: ResultComparerSensitivities(),
            TaskTypes.moieties: ResultComparerMoieties(),
            TaskTypes.crossSection: ResultComparerTimeCourse(),
            TaskTypes.lna: ResultComparer(),
            TaskTypes.exportSBML: ResultComparer(),
            TaskTypes.asIs: ResultComparer()
        }.get(task_type, None)

        if parser is not None:
            parser.task_type = task_type

        return parser
