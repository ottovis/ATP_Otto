import functools
from typing import Tuple, Union



def exec_unit(to_exec: list, stack: list = [], var_dict: dict = {}) -> Tuple[int, list, dict, bool]:
    # print("Stack:", stack)
    # print("Dict:", var_dict)
    if len(to_exec) == 0:
        return 0, stack, var_dict, False

    head, *tail = to_exec
    # print("Excecuting:", head.content, "    ",head.symb_type)
    status, stack, var_dict, return_now = head.excecute(stack, var_dict)
    
    if not status == 0 or return_now:
        return status, stack, var_dict, return_now

    status, stack, var_dict, return_now = exec_unit(tail, stack, var_dict)
    return status, stack, var_dict, return_now
    

def exec(parsed: list) -> int:
    return exec_unit(parsed)[0]

def excecute(parsed: list) -> int:
    exit_status = exec(parsed)

    return exit_status
 