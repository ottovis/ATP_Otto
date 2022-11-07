import unittest
from Interperter.mse_lexer import lexer
from Interperter.mse_error_handler import *


class TestLexer(unittest.TestCase):
    def test_lexer_asserts(self):
        self.assertRaises(AssertionError, lexer, "")
        self.assertRaises(AssertionError, lexer, 234)
        self.assertRaises(AssertionError, lexer, "test")
        self.assertRaises(AssertionError, lexer, "( [ ) ]")
        self.assertRaises(StringNotClosedError, lexer, "test \"test test $$")

    def test_lexer_io(self):
        self.assertEqual(lexer("test $$"), ["test", "$$"])
        self.assertEqual(lexer("test test $$"), ["test", "test", "$$"])
        self.assertEqual(lexer("\"test\" $$"), ["\"test\"", "$$"])
        self.assertEqual(lexer("\"test test\" $$"), ["\"test test\"", "$$"])
        self.assertEqual(lexer("test [ ^ ] test $$"), [
                         "test", ["[", "^", "]"], "test", "$$"])
        self.assertEqual(lexer("test ( ^ ) test $$"), [
                         "test", ["(", "^", ")"], "test", "$$"])
        self.assertEqual(lexer("test #A ^ $ test $$"), [
                         "test", ["#A", "^", "$"], "test", "$$"])
