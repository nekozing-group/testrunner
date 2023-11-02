import sys
import logging
from testrunner.core import TestRunner
from shared.models import TestRunnerResult, JobResult, JobError, TestRunnerState

log = logging.getLogger(__name__)


def run_job(session_id, input_file_path, problem_id) -> JobResult:
    job_result = JobResult(session_id=session_id)
    test_runner = None
    try:
        test_runner = TestRunner(session_id, problem_id, input_file_path)
        test_runner.init()
        test_result: TestRunnerResult = test_runner.run_tests()
        job_result.test_results = test_result
    except Exception as e:
        state = test_runner.state if test_runner is not None else TestRunnerState.UNKNOWN
        job_error = JobError(error_type=type(e).__name__, message=str(e), testrunner_state=state)
        job_result.error = job_error

    return job_result

if __name__ == "__main__":
    # Check if both arguments are provided
    if len(sys.argv) != 4:
        print("You must provide exactly 3 arguments: <session_id>, <input_file>, <problem_id>")
        sys.exit(1)

    # Extract arguments
    session_id = sys.argv[1]
    input_file_path = sys.argv[2] # the file to execute. this requires mount to be at the same path
    problem_id = sys.argv[3]
    print('received input params: session_id: %s, input_file_path: %s, problem_id: %s' % (session_id, input_file_path, problem_id))

    job_result = run_job(session_id, input_file_path, problem_id)
    
    print('----')
    print(job_result.model_dump_json())