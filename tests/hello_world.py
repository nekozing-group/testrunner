import subprocess

def test_solution():
    output = subprocess.check_output(['python', './input/solution.py'])
    assert output.decode('utf-8').strip() == 'hello world'