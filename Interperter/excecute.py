import functools
from typing import Tuple, Union



def exec_unit(to_exec: list, output: str = '', stack: Union[list, None] = None, var_dict: Union[dict, None] = None, unit_type: str = "main") -> Tuple[str, int, list, dict, Union[None, str]]:
    # print("Stack:", stack)
    # print("Dict:", var_dict)
    if stack is None:
        stack = []
    if var_dict is None:
        var_dict = {}

    if len(to_exec) == 0:
        return output, 0, stack, var_dict, None

    head, *tail = to_exec
    # print("Excecuting:", head.content, "    ",head.symb_type)
    output, status, stack, var_dict, return_type = head.excecute(output, stack, var_dict)
    
    if not status == 0 or return_type == unit_type:
        # print("Exit by exit symb")
        return output, status, stack, var_dict, None
    
    elif return_type is not None:
        return output, status, stack, var_dict, return_type

    return exec_unit(tail, output, stack, var_dict, unit_type)
    

def exec(parsed: list) -> Tuple[str, int]:
    return exec_unit(parsed)[0:2]

def excecute(parsed: list) -> Tuple[str, int]:
    output, exit_code = exec(parsed)

    return output, exit_code
 
