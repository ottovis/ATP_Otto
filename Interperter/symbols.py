import operator
from typing import Union, Tuple, Any, List
import math

try:
    from Interperter.mse_error_handler import *
    from Interperter.excecute import exec_unit
    from Interperter.compiler import comp_unit
except:
    from mse_error_handler import *
    from excecute import exec_unit
    from compiler import comp_unit

# base symbol class


class symb_base:

    _counter = 0

    # Only allowed to switch when BL to and external function,
    # else you can overwrite the altstack with old location
    def switch_default_stack(self, code: dict, context: list) -> Tuple[dict, list]:
        code[context[-1]]["code"].append("MOV R5, SP")
        code[context[-1]]["code"].append("MOV SP, R4")
        return code, context

    def switch_alt_stack(self, code: dict, context: list) -> Tuple[dict, list]:
        code[context[-1]]["code"].append("MOV R5, SP")
        code[context[-1]]["code"].append("MOV SP, R4")
        return code, context
# io symbols


class symb_int(symb_base):
    symb_type = "int"

    def __init__(self, interger: int) -> None:
        super(symb_base)
        assert type(interger) == int, "Int should be of type int"
        self.content = interger

    def __str__(self) -> str:
        return "Symbol: " + symb_int.symb_type + ": " + str(self.content)

    def excecute(self, output: str, stack: list, var_dict: dict) -> Tuple[str, int, list, dict, Union[None, str]]:
        stack.append(self.content)
        return output, 0, stack, var_dict, None

    def compile(self, code: dict, context: list) -> Tuple[dict, list]:
        code[context[-1]]['code'].append('MOV R0, #' + str(self.content))
        code[context[-1]]['code'].append(r'PUSH {R0}')
        return code, context


class symb_input(symb_base):
    symb_type = "input"
    content = '?'

    def __str__(self) -> str:
        return "Symbol: " + self.symb_type + ": " + symb_input.content

    def excecute(self, output: str, stack: list, var_dict: dict) -> Tuple[str, int, list, dict, Union[None, str]]:
        got = input("Input (int only): ")
        # ja ja, side effect, maar moet toch input krijgen. Zo functioneel mogelijk gedaan :)
        try:
            stack.append(int(got))
        except:
            print("Please give valid input")
            return self.excecute(output, stack, var_dict)
        return output, 0, stack, var_dict, None

    def compile(self, code: dict, context: list) -> Tuple[dict, list]:
        code, context = self.switch_default_stack(code, context)
        code[context[-1]]['code'].append("BL uart_get_int")
        code, context = self.switch_default_stack(code, context)
        code[context[-1]]['code'].append(r'PUSH {R0}')
        return code, context


class symb_output(symb_base):
    symb_type = "output"
    content = '!'

    def __str__(self) -> str:
        return "Symbol: " + self.symb_type + ": " + symb_output.content

    def excecute(self, output: str, stack: list, var_dict: dict) -> Tuple[str, int, list, dict, Union[None, str]]:
        tmp = stack.pop()
        print(tmp, end=' ')
        output += str(tmp) + ' '
        return output, 0, stack, var_dict, None

    def compile(self, code: dict, context: list) -> Tuple[dict, list]:
        code[context[-1]]['code'].append(r"POP {R0}")
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
        return "Symbol: " + self.symb_type + ": " + str(self.content)

    def print_rec(self, to_print: list, output: str) -> str:
        if len(to_print) == 0:
            return output
        head, *tail = to_print
        output += str(head) + ' '
        print(head, end=" ")
        return self.print_rec(tail, output)

    def excecute(self, output: str, stack: list, var_dict: dict) -> Tuple[str, int, list, dict, Union[None, str]]:
        output = self.print_rec(self.content, output)
        return output, 0, stack, var_dict, None

    def compile(self, code: dict, context: list) -> Tuple[dict, list]:
        name = "text" + str(len(code["main"]['strings']))
        code["main"
             ]['strings'].append(name + ": .asciz " + self.com_content)
        # print(code["main"]['strings'][-1])
        code[context[-1]]['code'].append("LDR R0, =" + name)
        code, context = self.switch_default_stack(code, context)
        code[context[-1]]['code'].append("BL print_asciz")
        code, context = self.switch_default_stack(code, context)
        return code, context


class symb_operator(symb_base):
    symb_type = "operator"

    def __init__(self, operator_to_exec: Any) -> None:
        self.content: Any
        self.content = operator_to_exec

    def __str__(self) -> str:
        return "Symbol: " + self.symb_type + ": " + str(self.content)

    def excecute(self, output: str, stack: list, var_dict: dict) -> Tuple[str, int, list, dict, Union[None, str]]:
        *stack, a, b = stack
        try:
            stack.append(math.floor(self.content(a, b)))
        except:
            raise InvalidOperatorError(a, b, self.content)
        return output, 0, stack, var_dict, None

    def compile(self, code: dict, context: list) -> Tuple[dict, list]:
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

        code[context[-1]]['code'].append(r'PUSH {R2}')

        return code, context


# class symb_exit(symb_base):
#     symb_type = "exit"
#     content = "$$"


class symb_stop(symb_base):
    symb_type = "stop"
    content = "$"

    def __str__(self) -> str:
        return "Symbol: " + self.symb_type + ": " + symb_stop.content

    # breaks loop
    def excecute(self, output: str, stack: list, var_dict: dict) -> Tuple[str, int, list, dict, Union[None, str]]:
        assert False, "This symbol should never be executed"
        return output, 0, stack, var_dict, True

    def compile(self, code: dict, context: list) -> dict:
        assert False, "This symbol should never be compiled"
        return code, context


class symb_dereference(symb_base):
    symb_type = "dereference"
    content = "."

    def __str__(self) -> str:
        return "Symbol: " + symb_dereference.symb_type + ": " + symb_dereference.content

    def excecute(self, output: str, stack: list, var_dict: dict) -> Tuple[str, int, list, dict, Union[None, str]]:
        *stack, a = stack
        assert a in var_dict, "Dereferencing non existing var"
        stack.append(var_dict[a])
        return output, 0, stack, var_dict, None

    def compile(self, code: dict, context: list) -> Tuple[dict, list]:
        code[context[-1]]['code'].append(r"POP {R0}")
        code[context[-1]]["code"].append("LDR R2, =var_lut")
        code[context[-1]]['code'].append("LDR R1, [R2, R0]")
        code[context[-1]]['code'].append(r'PUSH {R1}')
        return code, context


class symb_conditional_execution(symb_base):
    symb_type = "conditional_execution"

    def __init__(self, codeblock: list) -> None:
        self.content = codeblock
        self.callsign = "conditinal" + str(symb_base._counter)
        symb_base._counter += 1

    def __str__(self) -> str:
        return "Symbol: " + symb_conditional_execution.symb_type + ": " + str(self.content)

    def excecute(self, output: str, stack: list, var_dict: dict) -> Tuple[str, int, list, dict, Union[None, str]]:
        popped = stack.pop()
        if popped == 0:
            output, status, stack, var_dict, return_type = exec_unit(
                self.content, output, stack, var_dict, self.symb_type)
            return output, status, stack, var_dict, return_type

        return output, 0, stack, var_dict, None

    def compile(self, code: dict, context: list) -> Tuple[dict, list]:
        if self.callsign in code:
            code[context[-1]]["code"].append("BL " + self.callsign)
            context.append(self.callsign)
            return comp_unit(self.content, code, context)
        else:
            code[context[-1]]["code"].append("BL " + self.callsign)

            context.append(self.callsign)

            code[context[-1]] = {}
            code[context[-1]]["start"] = []
            code[context[-1]]["code"] = []
            code[context[-1]]["end"] = []

            code[context[-1]]["start"].append(self.callsign + ":")
            code, context = self.switch_default_stack(code, context)
            code[context[-1]]["start"].append(r"PUSH {LR}")
            code, context = self.switch_alt_stack(code, context)
            code[context[-1]]["start"].append(r"POP {R0}")
            code[context[-1]]["start"].append("CMP R0, #0")
            code[context[-1]]["start"].append("BEQ " + self.callsign + "_end")

            code[context[-1]]["end"].append(self.callsign + "_end:")
            code, context = self.switch_default_stack(code, context)
            code[context[-1]]["end"].append("MOV PC, R7")
            code, context = self.switch_alt_stack(code, context)

            code, context = comp_unit(self.content, code, context)
            if context[-1] == self.callsign:
                context.pop()
                print(
                    "Warning: needed to close symb_conditional_execution, should never be nessesary")
            if self.callsign in context:
                assert False, "Code inside should exit on its own "
            return code, context


class symb_loop(symb_base):
    symb_type = "loop"

    def __init__(self, codeblock: list) -> None:
        self.callsign = "loop" + str(symb_base._counter)
        self.content = codeblock
        symb_base._counter += 1

    def __str__(self) -> str:
        return "Symbol: " + symb_loop.symb_type + ": " + str(self.content)

    def excecute(self, output: str, stack: list, var_dict: dict) -> Tuple[str, int, list, dict, Union[None, str]]:
        output, status, stack, var_dict, return_type = exec_unit(
            self.content, output, stack, var_dict)
        if return_type is self.symb_type:
            return output, status, stack, var_dict, None
        elif return_type is not None:
            return output, status, stack, var_dict, return_type
        else:
            return self.excecute(output, stack, var_dict)

    def compile(self, code: dict, context: list) -> Tuple[dict, list]:

        code[context[-1]]["code"].append(self.callsign + "_start:")
        code, context = comp_unit(self.content, code, context, loop=self.callsign)
        code[context[-1]]["code"].append("B " + self.callsign + "_start:")
        code[context[-1]]["code"].append(self.callsign + "_end:")

        
        if context[-1] == self.callsign:
            context.pop()
            print("Warning: needed to close symb_loop, should never be nessesary")
        if self.callsign in context:
            assert False, "Code inside should exit on its own"
        return code, context


class symb_exit_loop(symb_base):
    symb_type = "exit_loop"
    content = "^"

    def __str__(self) -> str:
        return "Symbol: " + symb_exit_loop.symb_type + ": " + symb_exit_loop.content

    def excecute(self, output: str, stack: list, var_dict: dict) -> Tuple[str, int, list, dict, Union[None, str]]:
        return output, 0, stack, var_dict, symb_loop.symb_type

    def compile(self, code: dict, context: list) -> Tuple[dict, list]:
        if context[-1][0:4] == "loop":
            assert context[-1] != "main", "Cant use exit loop to exit main program"
            context.pop()
            return code, context

        else:
            assert context[-1] != "main", "Cant use exit loop to exit main program"
            context.pop()
            return self.compile(code, context)


class symb_macro(symb_base):
    symb_type = "macro"

    def __init__(self, callsign: str, codeblock: list) -> None:
        self.callsign = "macro_" + callsign
        self.content = codeblock

    def __str__(self) -> str:
        return "Symbol: " + symb_macro.symb_type + ": " + str(self.callsign) + ", codeblock: " + str(self.content)

    def excecute(self, output: str, stack: list, var_dict: dict) -> Tuple[str, int, list, dict, Union[None, str]]:
        if self.callsign not in var_dict:
            var_dict[self.callsign] = self
        return exec_unit(self.content, output, stack, var_dict, self.symb_type)

    def compile(self, code: dict, context: list) -> Tuple[dict, list]:
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

            code[self.callsign]["end"].append(self.callsign + "_end:")
            code[self.callsign]["end"].append("MOV PC, R7")
            code, context = comp_unit(self.content, code, context)
            assert context[-1] != self.callsign, "Macro must exit using @"
            return code, context


class symb_exit_macro(symb_base):
    symb_type = "exit_macro"
    content = "@"

    def __str__(self) -> str:
        return "Symbol: " + symb_exit_macro.symb_type + ": " + symb_exit_macro.content

    def excecute(self, output: str, stack: list, var_dict: dict) -> Tuple[str, int, list, dict, Union[None, str]]:
        return output, 0, stack, var_dict, symb_macro.symb_type

    def compile(self, code: dict, context: list) -> Tuple[dict, list]:
        assert context[-1] != "main", "Attempted to use @ to exit main"
        context.pop()
        return code, context


class symb_call_macro(symb_base):
    symb_type = "call_macro"

    def __init__(self, callsign: str) -> None:
        self.callsign = "macro_" + callsign
        self.content = callsign

    def __str__(self) -> str:
        return "Symbol: " + symb_call_macro.symb_type + ": " + str(self.callsign)

    def excecute(self, output: str, stack: list, var_dict: dict) -> Tuple[str, int, list, dict, Union[None, str]]:
        return var_dict[self.callsign].excecute(output, stack, var_dict)

    def compile(self, code: dict, context: list) -> Tuple[dict, list]:
        code[context[-1]]["code"].append("BL " + self.callsign)
        return code, context


class symb_var(symb_base):
    symb_type = "var"

    def __init__(self, var_name: str) -> None:
        self.content = var_name

    def __str__(self) -> str:
        return "Symbol: " + symb_var.symb_type + ": " + str(self.content)

    def excecute(self, output: str, stack: list, var_dict: dict) -> Tuple[str, int, list, dict, Union[None, str]]:
        stack.append(self.content)
        return output, 0, stack, var_dict, None

    def compile(self, code: dict, context: list) -> Tuple[dict, list]:
        if self.content not in code["assignments"]:
            code["assignments"][self.content] = str(len(code["assignments"]))

        code[context[-1]]["code"].append("LDR R0, =" +
                                         str(code["assignments"][self.content]))
        code[context[-1]]["code"].append(r"PUSH {R0}")
        return code, context


class symb_assignment(symb_base):
    symb_type = "assignment"
    content = "="

    def __str__(self) -> str:
        return "Symbol: " + symb_assignment.symb_type + ": " + symb_assignment.content

    def excecute(self, output: str, stack: list, var_dict: dict) -> Tuple[str, int, list, dict, Union[None, str]]:
        *stack, b, a = stack

        # Assert that a is an int and b is a string. Cannot be convertable to int
        assert type(a) == str, "Cannot assign a string to a variable" 
        assert type(b) == int, "Cannot assign to a int"

        # try:
        #     int(b)
        # except:
        #     raise InvalidAssignmentError(a, b)
        # try:
        #     int(a)
        #     raise InvalidAssignmentError(a, b)
        # except InvalidAssignmentError:
        #     assert False
        # except:
        #     pass

        var_dict[a] = b
        return output, 0, stack, var_dict, None

    def compile(self, code: dict, context: list) -> Tuple[dict, list]:
        code[context[-1]]["code"].append("POP {R0, R1}")
        code[context[-1]]["code"].append("LDR R2, =var_lut")
        code[context[-1]]["code"].append("STR R1, [R2, R0]")
        return code, context
