import operator
from typing import Union, Tuple
import math

from error_handler import *
from excecute import exec_unit

# base symbol class


class symb_base:
    pass
# io symbols


class symb_int(symb_base):
    symb_type = "int"

    def __init__(self, interger: int) -> None:
        super(symb_base)
        self.content = interger

    def __str__(self) -> str:
        return "Symbol: " + symb_int.symb_type + ": " + str(self.content)

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        stack.append(self.content)
        return 0, stack, var_dict, False


class symb_input(symb_base):
    symb_type = "input"
    content = '?'

    def __str__(self) -> str:
        return "Symbol: " + symb_input.symb_type + ": " + symb_input.content

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        got = input("Input (int only): ")
        # ja ja, side effect, maar moet toch input krijgen. Zo functioneel mogelijk gedaan :)
        try:
            stack.append(int(got))
        except:
            print("Please give valid input")
            return self.excecute(stack, var_dict)
        return 0, stack, var_dict, False


class symb_output(symb_base):
    symb_type = "output"
    content = '!'

    def __str__(self) -> str:
        return "Symbol: " + symb_output.symb_type + ": " + symb_output.content

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        print(stack.pop())
        return 0, stack, var_dict, False

# special symbols


class symb_string(symb_base):
    symb_type = "string"

    def __init__(self, string: str) -> None:
        split = string[1:-1].split('!')
        self.content = split

    def __str__(self) -> str:
        return "Symbol: " + symb_int.symb_type + ": " + str(self.content)

    def print_rec(self, to_print: list) -> None:
        if len(to_print) == 0:
            return
        head, *tail = to_print
        print(head, end="\n")
        return self.print_rec(tail)

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        self.print_rec(self.content)
        return 0, stack, var_dict, False


class symb_operator(symb_base):
    symb_type = "operator"

    def __init__(self, operator_to_exec: operator) -> None:
        self.content = operator_to_exec

    def __str__(self) -> str:
        return "Symbol: " + symb_int.symb_type + ": " + str(self.content)

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        *stack, a, b = stack
        try:
            stack.append(math.floor(self.content(a, b)))
        except:
            raise InvalidOperatorError(a, b, self.content)
        return 0, stack, var_dict, False


# class symb_exit(symb_base):
#     symb_type = "exit"
#     content = "$$"


class symb_stop(symb_base):
    symb_type = "stop"
    content = "$"

    def __str__(self) -> str:
        return "Symbol: " + symb_stop.symb_type + ": " + symb_stop.content

    # breaks loop
    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        return 0, stack, var_dict, True


class symb_assignment(symb_base):
    symb_type = "assignment"
    content = "="

    def __str__(self) -> str:
        return "Symbol: " + symb_assignment.symb_type + ": " + symb_assignment.content

    def excecute(self, stack: list, var_dict: dict) -> Union[Tuple[int, list, dict, bool], Error]:
        *stack, b, a = stack
        try:
            int(b)
        except:
            raise InvalidAssignmentError(a, b)
        try:
            int(a)
            raise InvalidAssignmentError(a, b)
        except:
            pass
        var_dict[a] = b
        return 0, stack, var_dict, False


class symb_dereference(symb_base):
    symb_type = "dereference"
    content = "."

    def __str__(self) -> str:
        return "Symbol: " + symb_dereference.symb_type + ": " + symb_dereference.content

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        *stack, a = stack
        stack.append(var_dict[a])
        return 0, stack, var_dict, False


class symb_conditional_execution(symb_base):
    symb_type = "conditional_execution"

    def __init__(self, codeblock: list) -> None:
        self.content = codeblock

    def __str__(self) -> str:
        return "Symbol: " + symb_conditional_execution.symb_type + ": " + str(self.content)

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        popped = stack.pop()
        if popped == 0:
            status, stack, var_dict, return_now = exec_unit(
                self.content, stack, var_dict)
            return status, stack, var_dict, return_now

        return 0, stack, var_dict, False


class symb_loop(symb_base):
    symb_type = "loop"

    def __init__(self, codeblock: list) -> None:
        self.content = codeblock

    def __str__(self) -> str:
        return "Symbol: " + symb_loop.symb_type + ": " + str(self.content)

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        status, stack, var_dict, return_now = exec_unit(
            self.content, stack, var_dict)
        if return_now or not status == 0:
            return status, stack, var_dict, False
        else:
            return self.excecute(stack, var_dict)


class symb_exit_loop(symb_base):
    symb_type = "exit_loop"
    content = "^"

    def __str__(self) -> str:
        return "Symbol: " + symb_exit_loop.symb_type + ": " + symb_exit_loop.content

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        return 0, stack, var_dict, True


class symb_macro(symb_base):
    symb_type = "macro"

    def __init__(self, callsign: str, codeblock: list) -> None:
        self.callsign = callsign
        self.content = codeblock
        self.registered = False

    def __str__(self) -> str:
        return "Symbol: " + symb_macro.symb_type + ": " + str(self.callsign) + ", codeblock: " + str(self.content)

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        if not self.registered:
            var_dict['#' + self.callsign] = self
            self.registered = True
        return exec_unit(self.content, stack, var_dict)


class symb_exit_macro(symb_base):
    symb_type = "exit_macro"
    content = "@"

    def __str__(self) -> str:
        return "Symbol: " + symb_exit_macro.symb_type + ": " + symb_exit_macro.content

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        return 0, stack, var_dict, True


class symb_call_macro(symb_base):
    symb_type = "call_macro"

    def __init__(self, callsign: str) -> None:
        self.callsign = callsign
        self.content = callsign

    def __str__(self) -> str:
        return "Symbol: " + symb_call_macro.symb_type + ": " + str(self.callsign)

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        var_dict['#' + self.callsign]
        status, stack, var_dict, return_now = exec_unit(var_dict['#' + self.callsign].content, stack, var_dict)
        return status, stack, var_dict, False


class symb_var(symb_base):
    symb_type = "var"

    def __init__(self, var_name: str) -> None:
        self.content = var_name

    def __str__(self) -> str:
        return "Symbol: " + symb_var.symb_type + ": " + str(self.content)

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        stack.append(self.content)
        return 0, stack, var_dict, False
