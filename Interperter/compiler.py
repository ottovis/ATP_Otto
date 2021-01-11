import functools
from typing import Tuple, Union


def comp_unit(to_exec: list, code: dict, context: str = None, stack: list = [], var_dict: dict = {}) -> Tuple[int, list, list, dict, bool]:
    # print("Stack:", stack)
    # print("Dict:", var_dict)
    if len(to_exec) == 0:
        return 0, stack, var_dict, False

    head, *tail = to_exec
    # print("Excecuting:", head.content, "    ",head.symb_type)
    status, stack, var_dict, return_now = head.excecute(stack, var_dict)

    if not status == 0 or return_now:
        return status, stack, var_dict, return_now

    status, stack, var_dict, return_now = comp_unit(
        tail, code, stack, var_dict)
    return status, code, stack, var_dict, return_now


def gen_dict() -> dict:
    code = {}
    # directives:
    code["directive"] = []
    code["directive"].append(".cpu cortex-m0")
    code["directive"].append(".align 2")
    code["directive"].append(".text")
    code["directive"].append(".global application")

    # strings:
    code["strings"] = []

    # start application
    code["start"] = []
    code["start"].append("PUSH {LR, R4, R5, R6, R7}")

    # usercode
    code["code"] = []

    # end application
    code["end"] = []
    code["end"].append("POP {PC, R4, R5, R6, R7}")

    # macros
    code["macros"] = {}

    return code


def printer(code: dict, name: str):
    with open(name[:-4] + '.asm', mode='w') as f:
        f.write('\n'.join(code["directive"]))
        f.write('\n')
        f.write('\n'.join(code["strings"]))
        f.write('\n')
        f.write('\n'.join(code["start"]))
        f.write('\n')
        f.write('\n'.join(code["code"]))
        f.write('\n')
        f.write('\n'.join(code["end"]))
        f.write('\n')
        # Mag dit alsjebrief niet recursief, ik snap dat het voor de opdracht zelf moet
        # maar hier is het gewoon irritant anders
        for marco in code["macros"]:
            f.write('\n'.join(marco))
            f.write('\n')


def comp(parsed: list) -> Tuple[int, dict]:
    code = gen_dict()
    compiled = comp_unit(parsed, code)
    return compiled[0], compiled[1]


def compiler(parsed: list) -> Tuple[int, dict]:
    exit_status, code = comp(parsed)
    return exit_status, code
