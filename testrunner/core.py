import tomllib
from importlib.resources import files
from RestrictedPython import compile_restricted
from .python_policy import allowed
from .models import TestRunnerResult, SingleTestRunResult

class TestRunner:
    def __init__(self, session_id: str, problem_id: str, input_file_path: str):
        self.session_id = session_id
        self.problem_id = problem_id
        self.input_file_path = input_file_path
        with open(input_file_path) as file:
            source = file.read()
        byte_code = compile_restricted(source, '<inline>', 'exec')
        loc = {}
        exec(byte_code, allowed, loc)
        self.loc = loc
        
    def load_test_cases(self):
        problem_id = self.problem_id
        toml_str = files('testrunner.data').joinpath(f'{problem_id}.toml').read_text()
        return tomllib.loads(toml_str)

    def run_tests(self) -> TestRunnerResult:
        test_cases = self.load_test_cases()['testcases']
        num_pass = 0
        outputs = []
        for single_test_case in test_cases:
            input, expected_output = single_test_case['input'], single_test_case['expected_output']
            test_output = self.run_single_test(input, expected_output)
            if test_output.test_pass:
                num_pass += 1
            outputs.append(test_output)
            
        return TestRunnerResult(
            session_id=self.session_id,
            test_outputs=outputs,
            num_total_tests=len(test_cases),
            num_tests_passed=num_pass,
        )

    def run_single_test(self, input, expected_output) -> SingleTestRunResult:
        actual_output = None
        test_pass = False
        if self.problem_id in self.loc:
            try:
                actual_output = self.loc[self.problem_id](input)
                test_pass = actual_output == expected_output
            except Exception as e:
                actual_output = f'{type(e).__name__} - {str(e)}'
        else:
            actual_output = f'function {self.problem_id} not defined in code'

        return SingleTestRunResult(
            test_pass=test_pass,
            input=input,
            expected_output=expected_output,
            actual_output=actual_output
        )
