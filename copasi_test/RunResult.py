
class RunResult:
    def __init__(self):
        pass
    PASS = 0
    WARN = 0
    FAIL = 1
    EXPECTED_FILE_MISSING = -1
    RESULT_FILE_MISSING = -2
    TEST_INVALID = -3
    COMPARE_NOT_IMPLEMENTED = -4
    EXPECTED_FILE_INVALID = -5
    RESULT_FILE_INVALID = -6
    INVALID_OBJECT = -7
    EXCEPTION = -8

