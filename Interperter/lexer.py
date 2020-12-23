import functools
from typing import Union
import operator
import math
from error_handler import *


def get_string(input_list: list) -> Union[tuple(list, list), ]:
    if (len(input_list) == 0):
        raise StringNotClosedError
    head, *tail = input_list
    return 

def remove_char(to_remove: list, input_list: list, protected: bool = False) -> list:
    if len(input_list) == 0:
        return []
    head, *tail = input_list
    if head == "\"":
        protected != protected
    if head in to_remove and not protected:
        return remove_char(to_remove, tail, protected)
    else:
        return_value = remove_char(to_remove, tail, protected)
        return_value.insert(0, head)
        return return_value



def preprocessor(file_contents: str) -> list:
    # Convert to list
    input_list = list(file_contents)
    print(input_list)

    # Remove spaces and enters.
    removed_chars = remove_char([' '], input_list)
    print(removed_chars)
    
    # Split by line

    # Return preprocessed input
    return removed_chars



def lexer(file_contents: str) -> list:
    processed = preprocessor(file_contents)
    return processed
