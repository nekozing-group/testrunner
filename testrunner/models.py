from pydantic import BaseModel
from typing import Any, List, Optional

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

class JobError(BaseModel):
    error_type: str
    message: str

class JobResult(BaseModel):
    session_id: str
    error: Optional[JobError] = None
    result: Optional[TestRunnerResult] = None