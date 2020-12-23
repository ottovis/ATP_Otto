from error_handler import *
import operator
from typing import Union, Tuple


# base symbol class
class symb_base:
    pass

# io symbols


class symb_int(symb_base):
    symb_type = "int"

    def __init__(self, interger: int) -> None:
        self.content = interger


class symb_input(symb_base):
    symb_type = "input"
    content = '?'


class symb_output(symb_base):
    symb_type = "output"
    content = '!'

# special symbols


class symb_string(symb_base):
    symb_type = "string"

    def __init__(self, string: str) -> None:
        self.content = string


class symb_operator(symb_base):
    symb_type = "operator"

    def __init__(self, operator_to_exec: operator) -> None:
        self.content = operator_to_exec

    def execute(self, a: int, b: int) -> Union[int, InvalidOperatorError]:
        try:
            x = math.floor(self.content(a, b))
        except:
            raise InvalidOperatorError(a, b, self.content)
        return x


# class symb_exit(symb_base):
#     symb_type = "exit"
#     content = "$$"


class symb_stop(symb_base):
    symb_type = "stop"
    content = "$"


class symb_assignment(symb_base):
    symb_type = "assignment"
    content = "="


class symb_dereference(symb_base):
    symb_type = "dereference"
    content = "."


class symb_conditional_execution(symb_base):
    symb_type = "conditional_execution"

    def __init__(self, codeblock: list) -> None:
        self.content = codeblock


class symb_loop(symb_base):
    symb_type = "loop"

    def __init__(self, codeblock: list) -> None:
        self.content = codeblock


class symb_exit_loop(symb_base):
    symb_type = "exit_loop"
    content = "^"


class symb_macro(symb_base):
    symb_type = "macro"

    def __init__(self, callsign: str, codeblock: list) -> None:
        self.callsign = callsign
        self.content = codeblock


class symb_exit_macro(symb_base):
    symb_type = "exit_macro"
    content = "@"

class symb_call_macro(symb_base):
    symb_type = "exit_macro"
    def __init__(self, callsign: str) -> None:
        self.callsign = callsign

class symb_var(symb_base):
    symb_type = "exit_macro"
    def __init__(self, var_name: str) -> None:
        self.var_name = var_name