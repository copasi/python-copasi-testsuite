import os
import re
import sys
import logging

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

from .TaskTypes import TaskTypes
from .RunResult import RunResult
from .TestReport import TestReport
from .TestRunner import TestRunner


def open_url(url):
    import subprocess
    if sys.platform == 'win32':
        os.startfile(url)
    elif sys.platform == 'darwin':
        subprocess.Popen(['open', url])
    else:
        try:
            subprocess.Popen(['xdg-open', url])
        except OSError:
            pass


class TestCase:
    def __init__(self, case_dir):
        self.case_dir = case_dir
        self.id = os.path.basename(os.path.abspath(case_dir))
        self.settings = {}
        self.task_type = TaskTypes.asIs
        self.initializeCase(case_dir)

    def initializeCase(self, directory):
        with open(os.path.join(directory, 'settings.txt'), 'r') as settings_file:
            for raw_line in settings_file:
                index = raw_line.find('#')
                if index < 0:
                    line = raw_line
                else:
                    line = raw_line[0:index].strip()
                index = line.find(':')
                if index != -1:
                    key = line[0:index].strip()
                    value = line[index+1:].strip()
                    self.settings[key] = value

        self.task_type = self.settings.get('task', TaskTypes.asIs)

        if 'atol' not in self.settings:
            self.settings['atol'] = 0.001
        else:
            self.settings['atol'] = float(self.settings['atol'])

        if 'rtol' not in self.settings:
            self.settings['rtol'] = 0.001
        else:
            self.settings['rtol'] = float(self.settings['rtol'])

    def open_settings(self):
        import subprocess
        subprocess.call(os.path.join(self.case_dir, 'settings.txt'), shell=True)

    def open_dir(self):
        open_url(self.case_dir)

    def isValid(self):
        # type: () -> bool
        if not os.path.exists(self.case_dir):
            return False

        if 'task' not in self.settings:
            return False

        if self.id == '':
            return False

        return True

    def format_is_sbml(self):
        if 'format' not in self.settings:
            return False

        return self.settings['format'] == 'sbml'

    def format_is_copasi(self):
        if 'format' not in self.settings:
            return True

        return self.settings['format'] == 'copasi'

    def print_overview(self, stream=None):
        if stream is None:
            stream = sys.stdout

        stream.write("Test:        {0}\n".format(self.id))
        stream.write("TaskType:    {0}\n".format(self.task_type))
        if 'description' in self.settings:
            stream.write("Description: {0}\n".format(self.settings['description']))

    def __repr__(self):
        stream = StringIO()
        self.print_overview(stream)
        stream.seek(0)
        return stream.read()

    def is_export(self):

        if not self.isValid():
            return False

        return 'export' in self.settings['task']

    def get_models(self):
        models = []

        if 'location' not in self.settings:
            return models

        location = self.settings['location']

        if location == '.':
            location = os.path.abspath(self.case_dir)
        elif location.startswith('./'):
            location = location.replace('./', os.path.abspath(self.case_dir) + '/', 1)

        if os.path.isfile(location):
            models.append(location)

        extension = '.cps'
        if self.format_is_sbml():
            extension = '.xml'

        reg = None
        if 'filter' in self.settings:
            reg = re.compile(self.settings['filter'])

        if os.path.isdir(location):
            for (dir_path, dir_names, file_names) in os.walk(location):
                file_names.sort()
                for name in file_names:
                    match = 'match' if reg is None else reg.match(name)
                    if match is None:
                        continue

                    if extension == name[-4:]:
                        models.append(os.path.join(dir_path, name))

        return models

    def generate_model(self, model_file, output_dir):
        import basico
        import COPASI
        file_name = os.path.join(output_dir, 'model-{0}-{1}.cps'.
                                 format(self.id, os.path.splitext(os.path.basename(model_file))[0]))
        report_name = os.path.join(output_dir, 'report-{0}-{1}.txt'.
                                   format(self.id, os.path.splitext(os.path.basename(model_file))[0]))
        dm = basico.load_model(model_file)
        if dm is None:
            return None

        if 'format' in self.settings and self.settings['format'] == 'copasi':
            # disable all other scheduled tasks
            if self.settings['task'] != 'as-is':
                for task in dm.getTaskList():
                    assert(isinstance(task, COPASI.CCopasiTask))
                    task.setScheduled(False)

        task = None
        need_report = False

        if self.settings['task'] == TaskTypes.asIs:
            need_report = True
            for temp_task in dm.getTaskList():
                assert (isinstance(temp_task, COPASI.CCopasiTask))
                if temp_task.isScheduled():
                    task = temp_task
                    break

            if task is None:
                logging.error('No active task found for test {0}'.format(self.id))
                return None

        elif self.settings['task'] == TaskTypes.steadystate:
            need_report = True
            task = dm.getTask('Steady-State')
            assert (isinstance(task, COPASI.CCopasiTask))
            task.setScheduled(True)
            task.setUpdateModel(True)

            method = task.getMethod()
            if 'Resolution' in self.settings:
                method.getParameter('Resolution').setDblValue(float(self.settings['Resolution']))
            if 'Use Newton' in self.settings:
                method.getParameter('Use Newton').setBoolValue(self.settings['Use Newton'].lower() == 'true')
            if 'Use Integration' in self.settings:
                method.getParameter('Use Integration').setBoolValue(self.settings['Use Integration'].lower() == 'true')
            if 'Use Back Integration' in self.settings:
                method.getParameter('Use Back Integration').setBoolValue(self.settings['Use Back Integration'].lower() == 'true')
            if 'Iteration Limit' in self.settings:
                method.getParameter('Iteration Limit').setUIntValue(int(self.settings['Iteration Limit']))
            if 'Maximum duration for forward integration' in self.settings:
                method.getParameter('Maximum duration for forward integration').setUDblValue(float(self.settings['Maximum duration for forward integration']))
            if 'Maximum duration for backward integration' in self.settings:
                method.getParameter('Maximum duration for backward integration').setUDblValue(float(self.settings['Maximum duration for backward integration']))
            if 'Target Criterion' in self.settings:
                p = method.getParameter('Target Criterion')
                if p is None:
                    method.addParameter('Target Criterion', COPASI.CCopasiParameter.Type_STRING)
                    p = method.getParameter('Target Criterion')
                p.setStringValue(self.settings['Target Criterion'])

        elif self.settings['task'] == TaskTypes.timecourse:
            need_report = True
            task = dm.getTask('Time-Course')
            assert (isinstance(task, COPASI.CCopasiTask))
            task.setScheduled(True)
            task.setUpdateModel(True)
            problem = task.getProblem()
            assert (isinstance(problem, COPASI.CTrajectoryProblem))

            if 'method' in self.settings:
                task.setMethodType(COPASI.CCopasiMethod.TypeNameToEnum(self.settings['method']))

            if 'duration' in self.settings:
                problem.setDuration(float(self.settings['duration']))
            if 'steps' in self.settings:
                problem.setStepNumber(int(self.settings['steps']))

            problem = task.getProblem()
            if 'StepNumber' in self.settings:
                problem.getParameter('StepNumber').setUIntValue(int(self.settings['StepNumber']))
            if 'StepSize' in self.settings:
                problem.getParameter('StepSize').setDblValue(float(self.settings['StepSize']))
            if 'Duration' in self.settings:
                problem.getParameter('Duration').setDblValue(float(self.settings['Duration']))

            COPASI.COutputAssistant.getListOfDefaultOutputDescriptions()
            COPASI.COutputAssistant.createDefaultOutput(1000, task, dm)

        elif self.settings['task'] == TaskTypes.scan:
            need_report = True
            task = dm.getTask('Scan')
            assert (isinstance(task, COPASI.CCopasiTask))
            task.setScheduled(True)

        elif self.settings['task'] == TaskTypes.efm:
            need_report = True
            task = dm.getTask('Elementary Flux Modes')
            assert (isinstance(task, COPASI.CCopasiTask))
            task.setScheduled(True)

        elif self.settings['task'] == TaskTypes.optimization:
            need_report = True
            task = dm.getTask('Optimization')
            assert (isinstance(task, COPASI.CCopasiTask))
            task.setScheduled(True)

            if 'method' in self.settings:
                task.setMethodType(COPASI.CCopasiMethod.TypeNameToEnum(self.settings['method']))

        elif self.settings['task'] == TaskTypes.parameterEstimation:
            need_report = True
            task = dm.getTask('Parameter Estimation')
            assert (isinstance(task, COPASI.CFitTask))
            task.setScheduled(True)

            if 'method' in self.settings:
                task.setMethodType(COPASI.CCopasiMethod.TypeNameToEnum(self.settings['method']))

            problem = task.getProblem()
            assert (isinstance(problem, COPASI.CFitProblem))

            # need to copy data files
            exp_set = problem.getExperimentSet()
            assert (isinstance(exp_set, COPASI.CExperimentSet))

            for i in range(exp_set.getExperimentCount()):
                exp = exp_set.getExperiment(i)
                assert (isinstance(exp, COPASI.CExperiment))
                filename = exp.getFileNameOnly()

                if not os.path.isfile(filename) and os.path.isfile(os.path.join(os.path.dirname(model_file), filename)):
                    filename = os.path.join(os.path.dirname(model_file), filename)

                if os.path.isfile(filename):
                    with open(filename, 'r') as data_file:
                        data = data_file.read()
                        new_file = os.path.join(output_dir, os.path.basename(filename))
                        with open(new_file, 'w') as new_data_file:
                            new_data_file.write(data)

                exp.setFileName(filename)

        elif self.settings['task'] == TaskTypes.mca:
            need_report = True
            task = dm.getTask('Metabolic Control Analysis')
            assert (isinstance(task, COPASI.CCopasiTask))
            task.setScheduled(True)
            task.setUpdateModel(True)

        elif self.settings['task'] == TaskTypes.lyap:
            need_report = True
            task = dm.getTask('Lyapunov Exponents')
            assert (isinstance(task, COPASI.CCopasiTask))
            task.setScheduled(True)

        elif self.settings['task'] == TaskTypes.tssa:
            need_report = True
            task = dm.getTask('Time Scale Separation Analysis')
            assert (isinstance(task, COPASI.CCopasiTask))
            task.setScheduled(True)

            if 'method' in self.settings:
                task.setMethodType(COPASI.CCopasiMethod.TypeNameToEnum(self.settings['method']))

            problem = task.getProblem()
            if 'StepNumber' in self.settings:
                problem.getParameter('StepNumber').setUIntValue(int(self.settings['StepNumber']))
            if 'StepSize' in self.settings:
                problem.getParameter('StepSize').setDblValue(float(self.settings['StepSize']))
            if 'Duration' in self.settings:
                problem.getParameter('Duration').setDblValue(float(self.settings['Duration']))

        elif self.settings['task'] == TaskTypes.sensitivities:
            need_report = True
            task = dm.getTask('Sensitivities')
            assert (isinstance(task, COPASI.CCopasiTask))
            task.setScheduled(True)

        elif self.settings['task'] == TaskTypes.moieties:
            need_report = True
            task = dm.getTask('Moieties')
            assert (isinstance(task, COPASI.CCopasiTask))
            task.setScheduled(True)

            reports = dm.getReportDefinitionList()
            assert (isinstance(reports, COPASI.CReportDefinitionVector))

            reports.removeByName('Moieties')

            new_report = reports.createReportDefinition('Moieties', 'Link Matrix and Stoichiometry matrix')
            assert (isinstance(new_report, COPASI.CReportDefinition))
            new_report.setIsTable(False)
            new_report.addFooterItem(dm.getModel().getObject(COPASI.CCommonName('Array=Link matrix(ann)')).getCN())
            new_report.addFooterItem(COPASI.CCommonName('String=\n'))
            new_report.addFooterItem(dm.getModel().getObject(COPASI.CCommonName('Array=Stoichiometry(ann)')).getCN())
            task.getReport().setReportDefinition(new_report)

        elif self.settings['task'] == TaskTypes.crossSection:
            need_report = True
            task = dm.getTask('Cross Section')
            assert (isinstance(task, COPASI.CCopasiTask))
            task.setScheduled(True)

            COPASI.COutputAssistant.getListOfDefaultOutputDescriptions()
            COPASI.COutputAssistant.createDefaultOutput(1000, task, dm)

        elif self.settings['task'] == TaskTypes.lna:
            need_report = True
            task = dm.getTask('Linear Noise Approximation')
            task.setScheduled(True)
            problem = task.getProblem()
            problem.getParameter('Steady-State').setStringValue(dm.getTask(TaskTypes.steadystate).getKey())

        if task is not None and need_report:
            report = task.getReport()
            assert (isinstance(report, COPASI.CReport))
            report.setConfirmOverwrite(False)
            report.setAppend(False)
            report.setTarget(report_name)
            logging.debug('\t Task is:    {0}'.format(task.getObjectName()))
            logging.debug('\t Method is:  {0}'.format(task.getMethod().getObjectName()))

        if dm.saveModel(file_name, True):
            basico.remove_datamodel(dm)
            return file_name

        basico.remove_datamodel(dm)
        return None

    def compare_files(self, expected_file, report_file, **kwargs):
        # type: (str, str) -> RunResult
        if not os.path.isfile(expected_file):
            logging.debug('expected result missing for test {0} looked for {1}'
                          .format(self.id, expected_file))
            return RunResult.EXPECTED_FILE_MISSING

        if not os.path.isfile(report_file):
            logging.debug('report result missing for test {0} looked for {1}'
                          .format(self.id, report_file))
            return RunResult.RESULT_FILE_MISSING

        expected = TestReport(expected_file, self.task_type)
        if not expected.is_valid():
            logging.debug('expected result invalid for test {0}'
                          .format(self.id))
            return RunResult.EXPECTED_FILE_INVALID

        other = TestReport(report_file, self.task_type)
        if not other.is_valid():
            logging.debug('report result invalid for test {0}'
                          .format(self.id))
            return RunResult.RESULT_FILE_INVALID

        # do actual comparison here
        comp = TaskTypes.getComparer(self.task_type)
        if comp is None:
            logging.debug('cannot compare result for test {0}'
                          .format(self.id))
            return RunResult.COMPARE_NOT_IMPLEMENTED

        base_name = os.path.splitext(os.path.basename(expected_file))[0]
        comp.case_id = self.id + ":" + base_name
        atol = kwargs.get('atol', self.settings['atol'])
        rtol = kwargs.get('rtol', self.settings['rtol'])
        compare_result = comp.compare(expected, other, atol=atol, rtol=rtol)
        run_result = compare_result.get_run_result()

        # or return failure
        return run_result

    def compare_result(self, model_file, runner, **kwargs):
        # type: (str, TestRunner) -> RunResult
        output_dir = runner.output_dir
        base_name = os.path.splitext(os.path.basename(model_file))[0]
        report_file = os.path.join(output_dir, 'report-{0}-{1}.txt'.format(self.id, base_name))
        expected_result = os.path.join(self.case_dir, 'report-{0}-{1}.txt'.format(self.id, base_name))
        if not os.path.exists(expected_result) and 'report_file' in self.settings:
            expected_result = os.path.join(self.case_dir, self.settings['report_file'])

        if ('result' in self.settings) and (self.settings['result'] == 'run-only'):
            logging.debug('returning pass result, because of "run-only"')
            return RunResult.PASS

        return self.compare_files(expected_result, report_file, **kwargs)

