import pytest
from otoole.preprocess import create_datafile
import tempfile

from subprocess import run

@pytest.fixture(scope='function')
def create_data_file():

    _, data_file = tempfile.mkstemp()

    url = 'https://raw.githubusercontent.com/OSeMOSYS/simplicity/master/datapackage.json'

    create_datafile(url, data_file)

    return data_file


class Test_RunMathProg():

    def test_mathprog_run_normal(self, create_data_file):

        arguments = ['glpsol', '-m', 'OSeMOSYS_GNU_MathProg/src/osemosys.txt', '-d',
                     create_data_file, '-o', 'results.csv']
        output = run(arguments, capture_output=True, text=True)
        assert 'OPTIMAL LP SOLUTION FOUND' in output.stdout
        assert 'obj =   2.944686269e+04' in output.stdout


    def test_mathprog_run_short(self, create_data_file):

        arguments = ['glpsol', '-m', 'OSeMOSYS_GNU_MathProg/src/osemosys_short.txt', '-d',
                     create_data_file, '-o', 'results_short.csv']
        output = run(arguments, capture_output=True, text=True)
        assert 'OPTIMAL LP SOLUTION FOUND' in output.stdout
        assert 'obj =   2.944686269e+04' in output.stdout

class Test_RunPyomo():

    def test_pyomo_run_normal(self, create_data_file):

        args = ['pyomo', 'solve', '--solver=glpk',
                'OSeMOSYS_Pyomo/OSeMOSYS-Pyomo_2019_05_13.py', create_data_file]
        output = run(args, capture_output=True, text=True)
        assert 'OPTIMAL LP SOLUTION FOUND' in output.stdout
        assert 'obj =   2.944686269e+04' in output.stdout