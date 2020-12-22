import functools
from typing import Union
import operator
import math




def remove_char(to_remove: list, input_list: list, protected: bool = False) -> list:
    if len(input_list) == 0:
        return []
    head, *tail = input_list
    if head == "\"":
        protected is not protected
    if head in to_remove and not protected:
        return remove_char(to_remove, tail, protected)
    else:
        return head + remove_char(to_remove, tail, protected)


def preprocessor(file_contents: str) -> list:
    # Convert to list
    input_list = list(file_contents)

    # Remove spaces and enters.
    removed_chars = remove_char([' '], input_list)
    
    # Split by line

    # Return preprocessed input
    return removed_chars



def lexer(file_contents: str) -> list:
    processed = preprocessor(file_contents)
    return processed
