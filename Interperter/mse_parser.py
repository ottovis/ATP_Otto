import functools
from typing import Union
import operator
import math

try:
    from Interperter.mse_error_handler import *
    from Interperter.symbols import *
    from Interperter.mse_lexer import split
except:
    from mse_error_handler import *
    from symbols import *
    from mse_lexer import split


def tree_builder(lexed: list, parsed: Union[list, None] = None, is_toplevel: Union[bool, None] = None, is_main: Union[bool, None] = None) -> list:
    if parsed is None:
        parsed = []
    if is_toplevel is None:
        is_toplevel = True
    if is_main is None:
        is_main = True

    if len(lexed) == 0:
        return parsed
    head, *tail = lexed

    try:
        try:
            # Make int if possible, this does seem to break pylance's typechecking
            head = int(head)
        except:
            head = float(head)
            assert False, "Floats are not supported"
    except AssertionError:
        assert False, "Floats are not supported"
    except:
        pass

    assert type(head) is int or type(head) is str or type(head) is list

    if type(head) is int:
        parsed.append(symb_int(head))
    elif type(head) is str:
        assert head[0] != " " or head[-1] != " ", "Lexer is broken, leading and ending spaces should have been stripped"
        if head == "$$":
            return parsed
        elif head == '?':
            parsed.append(symb_input())
        elif head == '!':
            parsed.append(symb_output())
        elif head[0] == '\"':
            assert head[-1] == '\"', "String not closed, somehow the lexer is broken"
            # print(head)
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

        elif head == "^":
            if is_toplevel:
                raise BreakFromTopLevelError
            parsed.append(symb_exit_loop())

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
    elif type(head) is list:
        if head[0][0] == '[':
            assert head[-1] == ']', f"Expected ] but got {head[-1]}, somehow the lexer is broken"
            split_head = split(head[1:-1])
            parsed.append(symb_conditional_execution(
                tree_builder(split_head, [], False, is_main)))
        elif head[0][0] == '(':
            assert head[-1] == ')', f"Expected ) but got {head[-1]}, somehow the lexer is broken"
            split_head = split(head[1:-1]) # remove the brackets
            build = tree_builder(split_head, [], False, is_main) 
            parsed.append(symb_loop(build))
        elif head[0][0] == '#':
            assert head[-1] == '$', f"Expected $ but got {head[-1]}, somehow the lexer is broken"
            assert head[-2] == '@', "The $ is end of macro block, but the @ is needed to return"
            assert len(head[0]) == 2, 'current implemenation only supports 26 macros, so only #A-Z is allowed'
            assert type(head[0][1]) is str, 'Only #A-Z are supported'
            split_head = split(head[1:-1])
            build = tree_builder(split_head, [], is_toplevel, False)
            parsed.append(symb_macro(head[0][1], build))
    else:
        assert False, "This should never happen, type check assert is broken"

    return tree_builder(tail, parsed, is_toplevel, is_main)


def parser(lexed: list) -> list:
    parsed = tree_builder(lexed)
    # print("Printing symbols:")
    # for symbol in parsed:
    #     print(symbol)

    return parsed
