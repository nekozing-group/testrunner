import sys
import logging
from testrunner.core import TestRunner
from shared.models import TestRunnerResult, JobResult, JobError

log = logging.getLogger(__name__)

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

    job_result = JobResult(session_id=session_id)

    try:
        # if not os.path.isfile(input_file_path):
        #     print(f'could not get code to run: {input_file_path}')
        #     print(f'os.path.isdir("/input"): {os.path.isdir("/input")}')
        #     raise FileExistsError('could not get code to run: {input_file_path}')
        test_runner = TestRunner(session_id, problem_id, input_file_path)    
        result: TestRunnerResult = test_runner.run_tests()
        job_result.result = result
    except Exception as e:
        job_error = JobError(error_type=type(e).__name__, message=str(e))
        job_result.error = job_error
    
    print(job_result)
    print('----')
    print(job_result.model_dump_json())