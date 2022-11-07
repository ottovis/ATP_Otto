import unittest
from Interperter.mse_parser import parser
from Interperter.symbols import *

class TestParser(unittest.TestCase):
    def test_parser_asserts(self):
        self.assertRaises(AssertionError, parser, [" ", "$$"])
        self.assertRaises(AssertionError, parser, ["2.9", "$$"])
        self.assertRaises(BreakFromMainError, parser, ["@", "$$"])
        self.assertRaises(BreakFromTopLevelError, parser, ["^", "$$"])
        self.assertRaises(AssertionError, parser, [["["], "$$"])
        self.assertRaises(AssertionError, parser, [["[", "]"], "$$"])

    def test_parser_int(self):
        self.assertEqual(parser(["2", "$$"])[0].symb_type, symb_int(2).symb_type)
        self.assertEqual(parser(["2", "$$"])[0].content, symb_int(2).content)

    def test_parser_var(self):
        self.assertEqual(parser(["a", "$$"])[0].symb_type, symb_var("a").symb_type)
        self.assertEqual(parser(["a", "$$"])[0].content, symb_var("a").content)

    def test_parser_input(self):
        self.assertEqual(parser(["?", "$$"])[0].symb_type, symb_input().symb_type)
        self.assertEqual(parser(["?", "$$"])[0].content, symb_input().content)

    def test_parser_output(self):
        self.assertEqual(parser(["!", "$$"])[0].symb_type, symb_output().symb_type)
        self.assertEqual(parser(["!", "$$"])[0].content, symb_output().content)
    
    def test_parser_add(self):
        self.assertEqual(parser(["+", "$$"])[0].symb_type, symb_operator(operator.add).symb_type)
        self.assertEqual(parser(["+", "$$"])[0].content, symb_operator(operator.add).content)

    def test_parser_sub(self):
        self.assertEqual(parser(["-", "$$"])[0].symb_type, symb_operator(operator.sub).symb_type)
        self.assertEqual(parser(["-", "$$"])[0].content, symb_operator(operator.sub).content)
    
    def test_parser_mul(self):
        self.assertEqual(parser(["*", "$$"])[0].symb_type, symb_operator(operator.mul).symb_type)
        self.assertEqual(parser(["*", "$$"])[0].content, symb_operator(operator.mul).content)

    def test_parser_div(self):
        self.assertEqual(parser(["/", "$$"])[0].symb_type, symb_operator(operator.truediv).symb_type)
        self.assertEqual(parser(["/", "$$"])[0].content, symb_operator(operator.truediv).content)
    
    def test_parser_stop(self):
        self.assertEqual(parser(["$", "$$"])[0].symb_type, symb_stop().symb_type)
        self.assertEqual(parser(["$", "$$"])[0].content, symb_stop().content)

    def test_parser_assignment(self):
        self.assertEqual(parser(["=", "$$"])[0].symb_type, symb_assignment().symb_type)
        self.assertEqual(parser(["=", "$$"])[0].content, symb_assignment().content)

    def test_parser_dereference(self):
        self.assertEqual(parser([".", "$$"])[0].symb_type, symb_dereference().symb_type)
        self.assertEqual(parser([".", "$$"])[0].content, symb_dereference().content)

    def test_parser_loop(self):
        self.assertRaises(BreakFromTopLevelError, parser, (["^", "$$"]))
        self.assertEqual(parser([[ "(", "^", ")"], "$$"])[0].symb_type, symb_loop(["^"]).symb_type)
        self.assertEqual(parser([[ "(", "^", ")"], "$$"])[0].content[0].symb_type, symb_loop([symb_exit_loop]).content[0].symb_type)

    def test_parser_conditional_execution(self):
        self.assertEqual(parser([[ "[", "1", "]"], "$$"])[0].symb_type, symb_conditional_execution(["1"]).symb_type)
        self.assertEqual(parser([[ "[", "1", "]"], "$$"])[0].content[0].symb_type, symb_conditional_execution([symb_int]).content[0].symb_type)

    def test_parser_macro(self):
        self.assertEqual(parser([["#A", "@", "$"], "$$"])[0].symb_type, symb_macro("A", []).symb_type)
        self.assertEqual(parser([["#A", "@", "$"], "$$"])[0].content[0].symb_type, symb_macro("A", [symb_exit_macro]).content[0].symb_type)
