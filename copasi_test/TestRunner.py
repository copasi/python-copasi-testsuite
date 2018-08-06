import os
import logging
import subprocess
import time

from RunResult import RunResult

isDebug = False

class TestRunner:
    def __init__(self, copasi_se, output_dir):
        # type: (str, str) -> None
        self.version = 'unknown'
        self.executable = copasi_se
        self.suite = None
        if not os.path.exists(self.executable):
            logging.warning("CopasiSE executable not found, hope it is in the path")

        try:
            out = subprocess.check_output([self.executable, '-h'], stderr=subprocess.STDOUT)
            self.version = out.split('\n')[0].strip()
        except:
            pass

        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logging.info("created output_dir {0}".format(self.output_dir))

    def is_valid(self):
        # type: () -> bool
        if not os.path.isfile(self.executable):
            return False

        if not os.path.exists(self.output_dir):
            return False

        return True

    def remove_results(self, case, **kwargs):
        if not case.isValid():
            return

        remove_model = kwargs.get('remove_model', True)
        remove_report = kwargs.get('remove_report', True)
        remove_result = kwargs.get('remove_result', True)

        models = case.get_models()
        for model_file in models:
            model_name = os.path.splitext(os.path.basename(model_file))[0]
            report_file = os.path.join(self.output_dir, 'report-{0}-{1}.txt'.format(case.id, model_name))
            model_file = os.path.join(self.output_dir, 'model-{0}-{1}.cps'.format(case.id, model_name))
            result_file = os.path.join(self.output_dir, 'result-{0}-{1}.xml'.format(case.id, model_name))
            if remove_report and os.path.isfile(report_file):
                os.remove(report_file)
            if remove_model and os.path.isfile(model_file):
                os.remove(model_file)
            if remove_result and os.path.isfile(result_file):
                os.remove(result_file)

    def runTest(self, case, **kwargs):
        # type: (TestCase) -> int
        if not case.isValid():
            return RunResult.TEST_INVALID

        use_existing = kwargs.get('use_existing', False)
        write_result = kwargs.get('write_result', True)

        # generate copasi file
        case.print_overview()
        models = case.get_models()

        t0 = time.clock()

        result = 0

        for model_file in models:

            model_name = os.path.splitext(os.path.basename(model_file))[0]
            logging.debug("Starting test for {0}".format(model_name))
            print ("  model {0}: start for {1}".format(model_name, repr(self)))
            try:
                input_file = case.generate_model(model_file, self.output_dir)
                if input_file is None:
                    logging.warning("Couldn't load model {0}".format(os.path.basename(model_file)))
                    continue

                output_file = os.path.join(self.output_dir, 'result-{0}-{1}.xml'.format(case.id, model_name))
                report_file = os.path.join(self.output_dir, 'report-{0}-{1}.txt'.format(case.id, model_name))

                extra_args = ['--nologo', input_file]

                if write_result:
                    if case.settings['task'] == 'sbml export':
                        extra_args += ['--exportSBML']
                    else:
                        extra_args += ['-s']

                    extra_args += [output_file]

                if not (os.path.isfile(report_file) and use_existing):
                    print ("  model {0}: execute {1}".format(model_name, repr(self)))
                    invoke_result = subprocess.check_call([self.executable] + extra_args)
                print ("  model {0}: compare result".format(model_name))
                result += case.compare_result(model_file, self)
            except:
                if isDebug:
                    import traceback
                    traceback.print_exc()
                logging.error('Failed to run model {0} of case {1}'.format(model_name, case.id))
                return RunResult.EXCEPTION

        logging.info("Test took {0} seconds".format(time.clock() - t0))

        return result

    def __repr__(self):
        if self.version != 'unknown':
            return self.version
        return 'CopasiSE'

    def runTests(self, tests, cancellation_token = None):
        # type: ([TestCase]) -> int
        result = 0
        for case in tests:
            if not cancellation_token is None and cancellation_token(case):
                break
            result += self.runTest(case, write_result=False)
        return  result

