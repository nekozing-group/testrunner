import tomllib
from importlib.resources import files
from RestrictedPython import compile_restricted
from .python_policy import allowed
from shared.models import TestRunnerResult, SingleTestRunResult, TestRunnerState

class TestRunner:
    def __init__(self, session_id: str, problem_id: str, input_file_path: str):
        self.state = TestRunnerState.INIT
        self.session_id = session_id
        self.problem_id = problem_id
        self.input_file_path = input_file_path

    # explicit init for state tracking
    def init(self):
        self.state = TestRunnerState.LOAD
        with open(self.input_file_path) as file:
            source = file.read()
        self.state = TestRunnerState.COMPILE
        byte_code = compile_restricted(source, '<inline>', 'exec')
        loc = {}
        self.state = TestRunnerState.BYTE_CODE
        exec(byte_code, allowed, loc)
        self.loc = loc
        self.state = TestRunnerState.READY
        
    def load_test_cases(self):
        problem_id = self.problem_id
        toml_str = files('shared.data').joinpath(f'{problem_id}.toml').read_text()
        return tomllib.loads(toml_str)

    def run_tests(self) -> TestRunnerResult:
        if (self.state != TestRunnerState.READY):
            raise ValueError(f'Invalid TestRunner state: {self.state}. TestRunner must be in READY state')
        self.state = TestRunnerState.LOAD_TESTCASE
        test_cases = self.load_test_cases()['testcases']
        num_pass = 0
        outputs = []
        self.state = TestRunnerState.RUN_TESTS
        for single_test_case in test_cases:
            input, expected_output = single_test_case['input'], single_test_case['expected_output']
            test_output = self.run_single_test(input, expected_output)
            if test_output.test_pass:
                num_pass += 1
            outputs.append(test_output)
            
        self.state = TestRunnerState.COMPLETE
        return TestRunnerResult(
            session_id=self.session_id,
            test_outputs=outputs,
            num_total_tests=len(test_cases),
            num_tests_passed=num_pass,
        )

    def run_single_test(self, input, expected_output) -> SingleTestRunResult:
        actual_output = None
        test_pass = False
        error_message = None
        if self.problem_id in self.loc:
            try:
                actual_output = self.loc[self.problem_id](input)
                test_pass = actual_output == expected_output
            except Exception as e:
                error_message = f'{type(e).__name__} - {str(e)}'
        else:
            actual_output = f'function {self.problem_id} not defined in code'

        return SingleTestRunResult(
            test_pass=test_pass,
            error_message=error_message,
            input=input,
            expected_output=expected_output,
            actual_output=actual_output
        )
