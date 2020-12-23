import functools
from typing import Union
import operator
import math

from error_handler import *
class symb_base:
    def execute(self):
        pass

class symb_input:
    pass

class symb_output:
    pass

class symb_operator(symb_base):
    def __init__(self, operator_to_exec) -> None:
        self.operator_to_exec = operator_to_exec
    
    def execute(self, a: int, b: int) -> Union[int, InvalidOperatorError]:
        try:
            x = math.floor(self.operator_to_exec(a,b))
        except:
            raise InvalidOperatorError(a, b, self.operator_to_exec)
        return x

class stack:
    def __init__(self):
        self.ptr_to_stack = []


def recurse_lexed(lexed : list, stack_obj : stack) -> Union[list, None]:
    if len(list) == 0:
        return None
    head, *tail = lexed
    to_append = None

    if type(head) == int:
        pass
    if type(head) == str:
        if head == "$$":
            return None
     




def parser(lexed : list) -> list:
    parsed = []
    return parsed



