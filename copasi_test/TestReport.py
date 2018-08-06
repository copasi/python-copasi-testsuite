import os

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class TestReport:

    def __init__(self, filename, task = 'as-is'):
        self.content = ''
        self.data_frames = []
        self.data_descriptions = []
        self.filename = filename
        self.task_name = task
        self.description = ''
        self.method = None
        self.problem = None
        self.task = None
        self.status = ''
        self.stability = ''
        self.parseReport(filename, task)
        pass

    def parseReport(self, filename, task):
        from TaskTypes import TaskTypes

        self.filename = filename
        self.task = task

        if not os.path.isfile(filename):
            return self

        parser = TaskTypes.getParser(task)
        if parser is None:
            raise NotImplementedError()

        parser.parserFile(filename)

        parser.applyToReport(self)

    def is_valid(self):
        if not os.path.isfile(self.filename):
            return False

        if len(self.data_descriptions) != len(self.data_frames):
            return False

        return True

    def get_data(self, name):
        for i in range(len(self.data_descriptions)):
            desc = self.data_descriptions[i]['desc']
            if desc == name:
                return self.data_frames[i]
        return None

    def compare_with(self, other, **kwargs):
        from TaskTypes import TaskTypes
        from RunResult import RunResult
        if not isinstance(other, TestReport):
            return RunResult.INVLID_OBJECT
        if other.task_name != self.task_name:
            return RunResult.INVLID_OBJECT

        comp = TaskTypes.getComparer(self.task_name)
        return comp.compare(self, other, **kwargs).get_run_result()

    def open_report(self):
        import subprocess
        subprocess.call(self.filename, shell=True)


    def __repr__(self):
        builder = StringIO()
        builder.write('FileName:   {0}\n'.format(os.path.basename(self.filename)))
        builder.write('TaskType:   {0}\n'.format(self.task))
        if not self.method is None:
            builder.write('Method:     {0}\n'.format(self.method))
        builder.write('isValid:    {0}\n'.format(self.is_valid()))
        builder.write('NumReports: {0}\n'.format(len(self.data_descriptions)))

        if (not self.status is None) and len(self.status.strip()) > 0:
            builder.write('Status:     {0}\n'.format(self.status))

        for desc in self.data_descriptions:
            builder.write('  {0}\n'.format(desc['desc']))
        builder.seek(0)
        return builder.read()

