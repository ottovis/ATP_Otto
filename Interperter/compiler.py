import functools
from typing import Tuple, Union, IO, Any, Dict


def comp_unit(to_exec: list, code: dict, context: list = ["main"], base_context : str = None, loop : str = None) -> Tuple[dict, list]:

    if base_context is None:
        base_context = context[-1]

    if len(to_exec) == 0:
        return code, context

    head, *tail = to_exec
    # print("Compiling:", head.content, "    ",head.symb_type)
    code, context = head.compile(code, context)

    if base_context not in context:
        return code, context

    if len(context) == 0:
        print("Warning, exited comp_unit by empty context")
        return code, context

    return comp_unit(tail, code, context, base_context)
    


def gen_dict() -> dict:
    code = {}
    code["main"] = {}
    # directives:
    # general
    code["main"]["directive"] = []
    code["main"]["directive"].append(".cpu cortex-m0")
    code["main"]["directive"].append(".align 4")
    code["main"]["directive"].append(
        ".global application, start, print_asciz, uart_print_int, uart_get_int, divide")

    # bss
    code["main"]["bss"] = []
    code["main"]["bss"].append(".bss")
    code["main"]["bss"].append("stack_alt:")
    code["main"]["bss"].append(".skip 1024")
    code["main"]["bss"].append("var_lut:")
    code["main"]["bss"].append(".skip 64")

    ## data / strings
    code["main"]["strings"] = []
    code["main"]["strings"].append(".data")

    # text
    code["main"]["text"] = []
    code["main"]["text"].append(".text")

    # start application
    code["main"]["start"] = []
    code["main"]["start"].append("application:")
    code["main"]["start"].append("PUSH {R4, R5, R6, R7, LR}")
    code["main"]["start"].append("MOV R4, SP")
    code["main"]["start"].append("LDR R6, =stack_alt")
    code["main"]["start"].append("MOV SP, R6")

    # usercode
    code["main"]["code"] = []

    # end application
    code["main"]["end"] = []
    code["main"]["end"].append("MOV SP, R4")
    code["main"]["end"].append("POP {R4, R5, R6, R7, PC}")

    # no local vars in this lang
    code["assignments"] = {}
    code["loop_tracker"] = 0
    code["curr_loop"] = []

    return code


def printer_marco(code: Dict[str, Dict[str, Any]], f: IO[Any], todo: list = None) -> None:
    if todo is None:
        head, *tail = code
    elif len(todo) == 0:
        return
    else:
        head, *tail = todo
    if head == "main" or head == "assignments" or head == "loop_tracker" or head == "curr_loop":
        printer_marco(code, f, tail)
        return
        
    f.write('\n'.join(code[head]["start"]))
    f.write('\n\n')
    f.write('\n'.join(code[head]["code"]))
    f.write('\n\n')
    f.write('\n'.join(code[head]["end"]))
    f.write('\n\n')
    printer_marco(code, f, tail)


def printer(code: Dict[str, Dict], name: str):
    # with open(name[:-4] + '.asm', mode='w') as f:
    with open('gen.asm', mode='w') as f:
        f.write('\n'.join(code["main"]["directive"]))
        f.write('\n\n')
        f.write('\n'.join(code["main"]["bss"]))
        f.write('\n\n')
        f.write('\n'.join(code["main"]["strings"]))
        f.write('\n\n')
        f.write('\n'.join(code["main"]["text"]))
        f.write('\n\n')
        f.write('\n'.join(code["main"]["start"]))
        f.write('\n\n')
        f.write('\n'.join(code["main"]["code"]))
        f.write('\n\n')
        f.write('\n'.join(code["main"]["end"]))
        f.write('\n\n')
        printer_marco(code, f)
            


def compiler(parsed: list) -> Tuple[dict, list]:
    code : dict
    code = gen_dict()
    return comp_unit(parsed, code)
