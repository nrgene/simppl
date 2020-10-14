import io
import math
import multiprocessing
import time
import unittest
import pytest
from example_module import add_two_numbers
from simppl.simple_pipeline import SimplePipeline


class TestSimplePipeline(unittest.TestCase):

    def test_print_and_run(self):
        output_stream = io.StringIO()
        sp = SimplePipeline(0, 10, output_stream=output_stream)
        sp.print_and_run('echo 5')
        sp.print_and_run('date --version > /dev/null')
        output_stream.seek(0)
        lines = output_stream.readlines()
        output_stream.close()
        self.assertTrue('1) echo 5' in lines[0])
        self.assertTrue('5\n' in lines[1])
        self.assertTrue('Time elapsed echo: 0 s' in lines[2])
        self.assertTrue('2) date --version', lines[3])
        self.assertTrue('Time elapsed date: 0 s' in lines[4])

    def test_print_and_run_with_name(self):
        output_stream = io.StringIO()
        sp = SimplePipeline(0, 10, name=__name__, output_stream=output_stream)
        sp.print_and_run('echo 5')
        output_stream.seek(0)
        lines = output_stream.readlines()
        output_stream.close()
        self.assertTrue(lines[0].endswith(__name__ + ' - INFO - 1) echo 5\n'))
        self.assertTrue(lines[1].endswith('5\n'))

    def test_run_parallel(self):
        available_cpus = multiprocessing.cpu_count()
        self._assert_run_parallel(available_cpus)

    def test_run_parallel_limit_pool(self):
        self._assert_run_parallel(1)

    def _assert_run_parallel(self, available_cpus):
        """
        @:param available_cpus - number of available cpus, must be <= actual available cpus of machine
        execute 3 sleep 1 sec commands
        check that all 3 commands ended after the expeced time
        """
        expected_sleep_seconds = math.ceil(3 / available_cpus)
        output_stream = io.StringIO()
        start = time.time()
        sp = SimplePipeline(0, 10, output_stream=output_stream)
        sp.run_parallel(['sleep 1', 'sleep 1', 'sleep 1'], available_cpus)
        self.assertEqual(math.floor(time.time() - start), expected_sleep_seconds)

    def test_debug_mode(self):
        output_stream = io.StringIO()
        sp = SimplePipeline(0, 10, debug=True, output_stream=output_stream)
        sp.print_and_run('date --version > /dev/null')
        sp.run_parallel(['sleep 0.1', 'sleep 0.4', 'sleep 1'], multiprocessing.cpu_count())
        sp.print_and_run('date > /dev/null')
        output_stream.seek(0)
        print(''.join(output_stream.readlines()))
        output_stream.seek(0)
        lines = output_stream.readlines()
        self.assertTrue('1) date' in lines[0], '1) date should be in first log line')
        for line in lines[1:3]:
            self.assertTrue('2) sleep' in line)
        self.assertTrue('3) date > /dev/null' in lines[4])
        output_stream.close()

    def test_print_and_run_failure(self):
        output_stream = io.StringIO()
        sp = SimplePipeline(0, 10, output_stream=output_stream)
        with pytest.raises(RuntimeError):
            sp.print_and_run('python no_existing.py')

    def test_run_parallel_failure(self):
        sp = SimplePipeline(0, 10)
        with pytest.raises(RuntimeError):
            sp.run_parallel(['python no_existing.py', 'echo hello'], multiprocessing.cpu_count())

    def test_run_clt_debug_mode(self):
        output_stream = io.StringIO()
        sp = SimplePipeline(0, 10, debug=True, output_stream=output_stream)
        sp.print_and_run_clt(add_two_numbers.run, ['arg1', 'arg2'], {'-key1': 'val1', '-key2': 'val2'},
                             {'--flag'})
        output_stream.seek(0)
        lines = output_stream.readlines()
        self.assertTrue('1) python -m <module> add_two_numbers_example arg1 arg2 -key1 val1 -key2 val2 --flag\n',
                        lines[0])


if __name__ == '__main__':
    unittest.main()
