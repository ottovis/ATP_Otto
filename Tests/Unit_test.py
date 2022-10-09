import unittest
from Interperter.mse_parser import *
from Interperter.mouse_interperter import main as main_interperter
import sys
import io

class TestSystem(unittest.TestCase):
    def __init__(self) -> None:
        self.capturedOutput = io.StringIO()
        sys.stdout = self.capturedOutput

    def reset_stdout(self):
        sys.stdout = sys.__stdout__

    def clear_stdout(self):
        self.capturedOutput.truncate(0)
        self.capturedOutput.seek(0)

    def test_hello_world(self):
        main_interperter("\"Hello World.\" $$")
        unittest.TestCase.assertEqual(self, self.capturedOutput.getvalue(), "Hello World.")
        self.clear_stdout()

    def test_sqrt(self):
        main_interperter("1 N = ( N . N . * ! \" - \" 10 N . - [ ^ ]  N . 1 + N = ) $$")
        unittest.TestCase.assertEqual(self, self.capturedOutput.getvalue(), "1  -  4  -  9  -  16  -  25  -  36  -  49  -  64  -  81  -  100  -  ")
        self.clear_stdout()
        

if __name__ == '__main__':
    unittest.main()
