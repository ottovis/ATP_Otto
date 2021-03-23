import functools
from typing import Tuple, Union, IO, Any, Dict


def comp_unit(to_exec: list, code: dict) -> Tuple[int, dict, bool]:
    if len(to_exec) == 0:
        return 0, code, False

    head, *tail = to_exec
    # print("Compiling:", head.content, "    ",head.symb_type)
    status, code, return_now = head.compile(code)

    if not status == 0 or return_now:
        return status, code, return_now

    status, code, return_now = comp_unit(tail, code)
    return status, code, return_now


def gen_dict() -> dict:
    code = {}
    code["main"] = {}
    # directives:
    # general
    code["main"]["directive"] = []
    code["main"]["directive"].append(".cpu cortex-m0")
    code["main"]["directive"].append(".align 4")
    code["main"]["directive"].append(
        ".global start print_asciz uart_print_int uart_get_int divide")

    # bss
    code["main"]["bss"] = []
    code["main"]["bss"].append(".bss")
    code["main"]["bss"].append("stack_alt: 1024")
    code["main"]["bss"].append("var_lut: 64")

    ## data / strings
    code["main"]["strings"] = []
    code["main"]["strings"].append(".data")

    # text
    code["main"]["text"] = []
    code["main"]["text"].append(".text")

    # start application
    code["main"]["start"] = []
    code["main"]["start"].append("start:")
    code["main"]["start"].append("PUSH {LR, R4, R5, R6, R7}")
    code["main"]["start"].append("MOV R4, SP")
    code["main"]["start"].append("MOV SP, =stack_alt")

    # usercode
    code["main"]["code"] = []

    # end application
    code["main"]["end"] = []
    code["main"]["end"].append("MOV SP, R4")
    code["main"]["end"].append("POP {PC, R4, R5, R6, R7}")

    # # macros, no longer needed here
    # code["macros"] = {}
    # # TODO: Switch stack!!!

    # no local vars in this lang
    code["assignments"] = {}

    return code


def printer_marco(code: Dict[str, Dict[Any]], f: IO[Any], labels: list = None) -> None:
    if labels is None:
        head, *tail = code
    if len(labels) == 0:
        return
    else:
        head, *tail = labels
    if head == "main":
        printer_marco(code, f, tail)
    f.write('\n'.join(code[head]["start"]))
    f.write('\n'.join(code[head]["code"]))
    f.write('\n'.join(code[head]["end"]))
    printer_marco(code, f, tail)


def printer(code: Dict[str, Dict], name: str):
    # with open(name[:-4] + '.asm', mode='w') as f:
    with open('gen.asm', mode='w') as f:
        f.write('\n'.join(code["main"]["directive"]))
        f.write('\n')
        f.write('\n'.join(code["main"]["bss"]))
        f.write('\n')
        f.write('\n'.join(code["main"]["strings"]))
        f.write('\n')
        f.write('\n'.join(code["main"]["text"]))
        f.write('\n')
        f.write('\n'.join(code["main"]["start"]))
        f.write('\n')
        f.write('\n'.join(code["main"]["code"]))
        f.write('\n')
        f.write('\n'.join(code["main"]["end"]))
        f.write('\n')
        printer_marco(code, f)


def comp(parsed: list) -> Tuple[int, dict]:
    code = gen_dict()
    compiled = comp_unit(parsed, code)
    return compiled[0], compiled[1]


def compiler(parsed: list) -> Tuple[int, dict]:
    exit_status, code = comp(parsed)
    return exit_status, code
