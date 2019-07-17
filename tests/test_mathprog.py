import pytest

from subprocess import run

class Test_RunMathProg():

    def test_mathprog_run_normal(self):

        arguments = ['glpsol', '-m', 'OSeMOSYS_GNU_MathProg/src/osemosys.txt', '-d', 
                     'Training_Case_Studies/utopia.txt', '-o', 'results.csv']
        output = run(arguments, capture_output=True, text=True)
        assert 'OPTIMAL LP SOLUTION FOUND' in output.stdout
        assert 'obj =   2.944686269e+04' in output.stdout


    def test_mathprog_run_short(self):

        arguments = ['glpsol', '-m', 'OSeMOSYS_GNU_MathProg/src/osemosys_short.txt', '-d', 
                     'Training_Case_Studies/utopia.txt', '-o', 'results_short.csv']
        output = run(arguments, capture_output=True, text=True)
        assert 'OPTIMAL LP SOLUTION FOUND' in output.stdout
        assert 'obj =   2.944686269e+04' in output.stdout