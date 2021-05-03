import operator
from typing import Union, Tuple
import math

from error_handler import *
from excecute import exec_unit
from compiler import comp_unit


# base symbol class


class symb_base:
    
    _counter = 0

    # Only allowed to switch when BL to and external function, 
    # else you can overwrite the altstack with old location
    def switch_default_stack(self, code: dict, context: str) -> Tuple[dict, list]:
        code[context[-1]]["code"].append("MOV R5, SP")
        code[context[-1]]["code"].append("MOV SP, R4")
        return code, context

    def switch_alt_stack(self, code: dict, context: str) -> Tuple[dict, list]:
        code[context[-1]]["code"].append("MOV R5, SP")
        code[context[-1]]["code"].append("MOV SP, R4")
        return code, context
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

    def compile(self, code: dict, context: str) -> dict:
        code[context[-1]]['code'].append('MOV R0 #' + str(self.content))
        code[context[-1]]['code'].append('PUSH R0')
        return code, context


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

    def compile(self, code: dict, context: str) -> dict:
        code, context = self.switch_default_stack(code, context)
        code[context[-1]]['code'].append("BL uart_get_int")
        code, context = self.switch_default_stack(code, context)
        code[context[-1]]['code'].append("PUSH R0")
        return code, context


class symb_output(symb_base):
    symb_type = "output"
    content = '!'

    def __str__(self) -> str:
        return "Symbol: " + symb_output.symb_type + ": " + symb_output.content

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        print(stack.pop())
        return 0, stack, var_dict, False

    def compile(self, code: dict, context: str) -> dict:
        code[context[-1]]['code'].append("POP R0")
        code, context = self.switch_default_stack(code, context)
        code[context[-1]]['code'].append("BL uart_print_int")
        code, context = self.switch_default_stack(code, context)
        return code, context


# special symbols


class symb_string(symb_base):
    symb_type = "string"

    def __init__(self, string: str) -> None:
        split = string[1:-1].split('!')
        self.content = split
        self.com_content = string

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

    def compile(self, code: dict, context: str) -> dict:
        name = "text" + str(len(code[context[-1]]['strings']))
        code[context[-1]
             ]['strings'].append(name + ": .asciz " + self.com_content)
        code[context[-1]]['code'].append("LDR R0, =" + name)
        code, context = self.switch_default_stack(code, context)
        code[context[-1]]['code'].append("BL print_asciz")
        code, context = self.switch_default_stack(code, context)
        return code, context


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

    def compile(self, code: dict, context: str) -> dict:
        code[context[-1]]['code'].append("POP {R0, R1}")
        if self.content == operator.add:
            code[context[-1]]['code'].append("ADD R2, R0, R1")
        elif self.content == operator.mul:
            code[context[-1]]['code'].append("MUL R2, R0, R1")
        elif self.content == operator.sub:
            code[context[-1]]['code'].append("SUB R2, R0, R1")
        else:
            # TODO: Dit wordt janken, div'en is kut
            assert False

        code[context[-1]]['code'].append("PUSH R2")

        return code, context


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

    def compile(self, code: dict, context: list) -> dict:
        code[context[-1]]['code'].append("MOV R5, SP")
        code[context[-1]]['code'].append("MOV SP, R4")
        code[context[-1]]['code'].append("POP { PC }")
        context.pop()
        assert False
        # TODO: Add stack switching
        return code, context


class symb_dereference(symb_base):
    symb_type = "dereference"
    content = "."

    def __str__(self) -> str:
        return "Symbol: " + symb_dereference.symb_type + ": " + symb_dereference.content

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        *stack, a = stack
        stack.append(var_dict[a])
        return 0, stack, var_dict, False

    def compile(self, code: dict, context: list) -> dict:

        return code, context


class symb_conditional_execution(symb_base):
    symb_type = "conditional_execution"

    def __init__(self, codeblock: list) -> None:
        symb_base._counter += 1
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
        symb_base._counter += 1
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

    def compile(self, code: dict, context: list) -> dict:
        if self.callsign in code:
            code[context[-1]]["code"].append("BL " + self.callsign)
            context.append(self.callsign)
            return comp_unit(self.content, code, context)
        else:
            code[context[-1]]["code"].append("BL " + self.callsign)
            code[context[-1]]["code"].append("BL " + self.callsign)

            context.append(self.callsign)

            code[self.callsign] = {}
            code[self.callsign]["start"] = []
            code[self.callsign]["code"] = []
            code[self.callsign]["end"] = []

            code[self.callsign]["start"].append(self.callsign + ":")
            code[self.callsign]["start"].append("MOV R7, LR")

            code[self.callsign]["end"].append("MOV PC, R7")
            code, context = comp_unit(self.content, code, context)
            assert context[-1] != self.callsign, "Macro must exit using @"
            return code, context


        code[context[-1]]["code"].append("start_loop" + str(code["loop_tracker"] + ":"))
        code["curr_loop"].append(code["loop_tracker"])
        code["loop_tracker"] += 1
        return code, context


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

    def compile(self, code: dict, context: list) -> dict:
        if self.callsign in code:
            code[context[-1]]["code"].append("BL " + self.callsign)
            context.append(self.callsign)
            return comp_unit(self.content, code, context)
        else:
            code[context[-1]]["code"].append("BL " + self.callsign)
            code[context[-1]]["code"].append("BL " + self.callsign)

            context.append(self.callsign)

            code[self.callsign] = {}
            code[self.callsign]["start"] = []
            code[self.callsign]["code"] = []
            code[self.callsign]["end"] = []

            code[self.callsign]["start"].append(self.callsign + ":")
            code[self.callsign]["start"].append("MOV R7, LR")

            code[self.callsign]["end"].append("MOV PC, R7")
            code, context = comp_unit(self.content, code, context)
            assert context[-1] != self.callsign, "Macro must exit using @"
            return code, context


class symb_exit_macro(symb_base):
    symb_type = "exit_macro"
    content = "@"

    def __str__(self) -> str:
        return "Symbol: " + symb_exit_macro.symb_type + ": " + symb_exit_macro.content

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        return 0, stack, var_dict, True

    def compile(self, code: dict, context: list) -> dict:
        assert context[-1] != "main", "Attempted to use @ to exit main"
        context.pop()
        return code, context


class symb_call_macro(symb_base):
    symb_type = "call_macro"

    def __init__(self, callsign: str) -> None:
        self.callsign = callsign
        self.content = callsign

    def __str__(self) -> str:
        return "Symbol: " + symb_call_macro.symb_type + ": " + str(self.callsign)

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        # var_dict['#' + self.callsign] 
        status, stack, var_dict, return_now = exec_unit(
            var_dict['#' + self.callsign].content, stack, var_dict)
        return status, stack, var_dict, False

    def compile(self, code: dict, context: str) -> dict:
        code[context[-1]]["code"].append("BL " + self.callsign)
        return code, context


class symb_var(symb_base):
    symb_type = "var"

    def __init__(self, var_name: str) -> None:
        self.content = var_name

    def __str__(self) -> str:
        return "Symbol: " + symb_var.symb_type + ": " + str(self.content)

    def excecute(self, stack: list, var_dict: dict) -> Tuple[int, list, dict, bool]:
        stack.append(self.content)
        return 0, stack, var_dict, False

    def compile(self, code: dict, context: str) -> dict:
        if self.content not in code["assignments"]:
            code["assignments"][self.content] = len(code["assignments"])

        code[context[-1]
             ]["code"].append("MOV R0, #" + code["assignments"][self.content])
        code[context[-1]]["code"].append("PUSH R0")
        return code, context


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
        except InvalidAssignmentError:
            assert False
        except:
            pass
        var_dict[a] = b
        return 0, stack, var_dict, False

    def compile(self, code: dict, context: str) -> dict:
        code[context[-1]]["code"].append("POP {R0, R1}")
        code[context[-1]]["code"].append("MOV R2, =var_lut")
        code[context[-1]]["code"].append("STR R1, [R2, R0]")
        return code, context
