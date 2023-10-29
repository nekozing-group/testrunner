from pydantic import BaseModel
from typing import Any, List

class SingleTestRunResult(BaseModel):
    test_pass: bool
    input: Any
    actual_output: Any
    expected_output: Any

class TestRunnerResult(BaseModel):
    session_id: str
    test_outputs: List[SingleTestRunResult]
    num_total_tests: int
    num_tests_passed: int