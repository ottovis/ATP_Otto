import functools
from typing import Tuple, Union



def exec_unit(to_exec: list, stack: list = [], var_dict: dict = {}, unit_type: str = "main") -> Tuple[int, list, dict, Union[None, str]]:
    # print("Stack:", stack)
    # print("Dict:", var_dict)
    if len(to_exec) == 0:
        return 0, stack, var_dict, None

    head, *tail = to_exec
    # print("Excecuting:", head.content, "    ",head.symb_type)
    status, stack, var_dict, return_type = head.excecute(stack, var_dict)
    
    if not status == 0 or return_type == unit_type:
        # print("Exit by exit symb")
        return status, stack, var_dict, None
    
    elif return_type is not None:
        return status, stack, var_dict, return_type

    return exec_unit(tail, stack, var_dict, unit_type)
    

def exec(parsed: list) -> int:
    return exec_unit(parsed)[0]

def excecute(parsed: list) -> int:
    exit_status = exec(parsed)

    return exit_status
 
