import functools
from typing import Union
import operator
import math

from error_handler import *
from symbols import *
from lexer import split


def tree_builder(lexed: list, parsed: list = [], is_toplevel: bool = True, is_main: bool = True) -> Union[list, Error]:
    if len(lexed) == 0:
        raise NoEndTokenError
    head, *tail = lexed

    assert type(head) is int or str

    if type(head) is int:
        parsed.append(symb_int(head))
    elif type(head) is str:
        if head == "$$":
            return parsed
        elif head == '?':
            parsed.append(symb_input())
        elif head == '!':
            parsed.append(symb_output())
        elif head[0] == '\"':
            assert head[-1] == '\"'
            parsed.append(symb_string(head))
        elif head == '+':
            parsed.append(symb_operator(operator.add))
        elif head == '-':
            parsed.append(symb_operator(operator.sub))
        elif head == '*':
            parsed.append(symb_operator(operator.mul))
        elif head == '/':
            parsed.append(symb_operator(operator.truediv))
        elif head == '$':
            parsed.append(symb_stop())
        elif head == '=':
            parsed.append(symb_assignment())
        elif head == '.':
            parsed.append(symb_dereference())
        elif head[0] == '[':
            assert head[-1] == ']'
            split_head = split(head[1:-1])
            parsed.append(symb_conditional_execution(tree_builder(split_head, [], False, is_main)))
        elif head[0] == '(':
            assert head[-1] == ')'
            split_head = split(head[1:-1])
            parsed.append(symb_loop(tree_builder(split_head, [], False, is_main)))
        elif head == "^":
            if is_toplevel:
                raise BreakFromTopLevelError
            parsed.append(symb_exit_loop())
        elif head[0] == '#':
            assert head[-1] == '$'
            assert head[2] == ' ', 'current implemenation only supports 26 macros'
            assert type(head[1]) is str, 'Only #A-Z are supported'
            split_head = split(head[1:-1])
            parsed.append(symb_macro(head[1], tree_builder(split_head, [], is_toplevel, False)))
        elif head == '@':
            if is_main:
                raise BreakFromMainError
            parsed.append(symb_exit_macro())
        elif head[0] == '~':
            assert len(
                head) == 2, 'current implemenation only supports 26 macros'
            assert type(head[1]) is str
            parsed.append(symb_call_macro(head[1]))
        else:
            parsed.append(symb_var(head))

    return tree_builder(tail, parsed, is_toplevel)


def parser(lexed: list) -> list:
    parsed = []

    return parsed
