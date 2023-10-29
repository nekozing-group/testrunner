import subprocess
import tomllib
import json
from importlib.resources import files
from .models import TestResult, SingleTestRunResult

class TestRunner:
    def __init__(self, session_id: str, problem_id: str, input_file_path: str):
        self.session_id = session_id
        self.problem_id = problem_id
        self.input_file_path = input_file_path
        
    def load_test_cases(self):
        problem_id = self.problem_id
        toml_str = files('testrunner.data').joinpath(f'{problem_id}.toml').read_text()
        return tomllib.loads(toml_str)

    def run_tests(self):
        test_cases = self.load_test_cases()
        num_pass = 0
        outputs = []
        for single_test_case in test_cases:
            input, expected_output = single_test_case['input'], single_test_case['expected_output']
            test_output = self.run_single_test(input, expected_output)
            if test_output.test_pass:
                num_pass += 1
            outputs.append(test_output)
            
        return TestResult(
            session_id=self.session_id,
            num_total_tests=len(test_cases),
            num_tests_passed=num_pass,
        )

    def run_single_test(self, input, expected_output) -> SingleTestRunResult:
        actual_output = None
        test_pass = False
        try:
            result = subprocess.run(['python', self.input_code_path, json.dumps(input)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            actual_output = result.stdout.strip()
            test_pass = json.loads(actual_output) == expected_output
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error code {e.returncode}")
            print("Standard Output:")
            print(e.stdout)
            print("Standard Error:")
            print(e.stderr)
            actual_output = e.stderr

        return SingleTestRunResult(
            test_pass=test_pass,
            input=input,
            expected_output=expected_output,
            actual_output=actual_output
        )
