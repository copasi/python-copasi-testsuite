import os
import logging
import subprocess
import time
import threading
import traceback

from .RunResult import RunResult

support_parallelism = True
try:
    from joblib import Parallel, delayed
    import multiprocessing
except ImportError:
    support_parallelism = False

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

isDebug = True


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
            logging.debug("created output_dir {0}".format(self.output_dir))

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

    def compareTest(self, case, **kwargs):
        models = case.get_models()
        result = 0
        for model_file in models:

            model_name = os.path.splitext(os.path.basename(model_file))[0]
            logging.info("Comparing test {0} for {1}".format(case.id, model_name))
            result += case.compare_result(model_file, self, **kwargs) != RunResult.PASS

        return result

    def compareTestAgainstOther(self, case, other, **kwargs):
        # type: (TestCase, TestRunner, Any) -> int
        models = case.get_models()
        result = 0
        for model_file in models:

            base_name = os.path.splitext(os.path.basename(model_file))[0]
            this_report_file = os.path.join(self.output_dir, 'report-{0}-{1}.txt'.format(case.id, base_name))
            other_report_file = os.path.join(other.output_dir, 'report-{0}-{1}.txt'.format(case.id, base_name))
            logging.info("Comparing test {0} for {1}".format(case.id, base_name))
            result += case.compare_files(this_report_file, other_report_file, **kwargs) != RunResult.PASS

        return result

    def runTest(self, case, **kwargs):
        # type: (TestCase.TestCase,**kwargs) -> int
        if not case.isValid():
            return RunResult.TEST_INVALID

        use_existing = kwargs.get('use_existing', False)
        write_result = kwargs.get('write_result', True)

        # generate copasi file
        logging.debug(repr(case))
        models = case.get_models()

        t0 = time.clock()

        result = 0

        for model_file in models:

            model_name = os.path.splitext(os.path.basename(model_file))[0]
            logging.info("Starting test {0} for {1}".format(case.id,model_name))
            logging.debug("  model {0}: start for {1}".format(model_name, repr(self)))
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
                    logging.debug("  model {0}: execute {1}".format(model_name, repr(self)))
                    self.call_copasi(case, [self.executable] + extra_args)

                logging.debug("  model {0}: compare result".format(model_name))
                result += case.compare_result(model_file, self) != RunResult.PASS

            except Exception as e:
                if 'ignore_exception' in case.settings and case.settings['ignore_exception'].lower() == 'true':
                    continue

                if isinstance(e, ValueError):
                    logging.error('Failed to run model {0} of case {1}:\n{2}\n'.format(model_name, case.id, str(e)))
                else:
                    if isDebug:
                        err_msg = StringIO()
                        traceback.print_exc(file=err_msg)
                        err_msg.seek(0)
                        logging.error(
                            'Failed to run model {0} of case {1}:\n{2}'.format(model_name, case.id, err_msg.read()))
                    else:
                        logging.error('Failed to run model {0} of case {1}'.format(model_name, case.id))
                return RunResult.EXCEPTION

        logging.debug("Test took {0} seconds".format(time.clock() - t0))

        return result

    @staticmethod
    def call_copasi(case, *popenargs, **kwargs):
        t0 = time.clock()
        p = subprocess.Popen(*popenargs, stderr=subprocess.PIPE, stdout=subprocess.PIPE,  **kwargs)

        if 'timeout' in case.settings:
            timeout_sec = int(case.settings['timeout'])
            timer = threading.Timer(timeout_sec, p.kill)
            try:
                timer.start()
                stdout, stderr = p.communicate()
            finally:
                timer.cancel()
        else:
            stdout, stderr = p.communicate()

        logging.debug('\tran for {0} seconds'.format(time.clock() - t0))

        retcode = p.returncode
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            if len(stderr) > 0:
                raise ValueError(stderr)
            raise subprocess.CalledProcessError(retcode, cmd)

        if len(stderr) > 0:
            logging.debug(stderr)

        return 0

    def __repr__(self):
        if self.version != 'unknown':
            return self.version
        return 'CopasiSE'

    def runTests(self, tests, cancellation_token=None):
        # type: ([TestCase]) -> int
        result = 0
        for case in tests:
            if cancellation_token is not None and cancellation_token(case):
                break
            result += self.runTest(case, write_result=False)
        return result

    def runTestsParallel(self, tests, n_jobs=-1, cancellation_token=None):
        # type: ([TestCase]) -> int

        if not support_parallelism:
            return self.runTests(tests, cancellation_token)

        result = Parallel(n_jobs=n_jobs, prefer='processes')\
            (delayed(self.runTest)(case, write_result=False) for case in tests)
        result = sum(result)
        return result
