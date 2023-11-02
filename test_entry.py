from importlib.resources import files
from entrypoint import run_job

def test_run_job():
    source_path = str(files('tests.testdata').joinpath(f'sort.py'))
    result = run_job('test_run_job', source_path, 'sort').test_results
    assert result.num_tests_passed == 4