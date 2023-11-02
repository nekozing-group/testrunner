from testrunner.core import TestRunner
from shared.models import TestRunnerResult
from importlib.resources import files
import pytest

def test_happy():
    source_path = str(files('tests.testdata').joinpath(f'sort.py'))
    tr = TestRunner('test_happy', 'sort', source_path)
    result: TestRunnerResult = tr.run_tests()
    assert result.num_total_tests == 4
    assert result.num_tests_passed == 4

def test_compile_error():
    source_path = str(files('tests.testdata').joinpath(f'compile_error.py'))
    with pytest.raises(NameError) as e:
        tr = TestRunner('compile_error', 'compile_error', source_path)

def test_illegal_import():
    source_path = str(files('tests.testdata').joinpath(f'illegal_import.py'))
    with pytest.raises(ImportError) as e:
        tr = TestRunner('illegal_import', 'illegal_import', source_path)

def test_runtime_error():
    source_path = str(files('tests.testdata').joinpath(f'runtime_error.py'))
    tr = TestRunner('sort', 'sort', source_path)
    result: TestRunnerResult = tr.run_tests()
    assert result.num_total_tests == 4
    assert result.num_tests_passed == 0
    assert result.test_outputs[0].actual_output is None
    assert result.test_outputs[0].error_message == 'IndexError - list index out of range'