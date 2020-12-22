import functools
from typing import Union
import operator
import math

class error_type_base:
    def __init__(self):
        pass

class error_type_invalid_operation(error_type_base):
    def __init__(self, a : int, b : int, used_operator : operator):
        self.a = a
        self.b = b
        self.used_operator = used_operator

    def __str__(self):
        return "invalid operation with " + self.a + " and " + self.b + " using: " self.used_operator

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
    
    def execute(self, a : int, b : int) -> Union[int, error_type_invalid_operation]:
        try:
            x = math.floor(self.operator_to_exec(a,b))
        except:
            return error_type_invalid_operation(a, b)
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



