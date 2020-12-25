import functools
from typing import Union, Tuple
import operator
import math
import csv

from error_handler import *
from symbols import *


# def get_block(input_list: list, to_find: str, output_list: list = []) -> Union[Tuple[list, list], Error]:
#     if (len(input_list) == 0):
#         raise CodeBlockNotClosedError(output_list)
#     head, *tail = input_list
#     assert len(to_find) == 1, "Only ever search for single closing char"
#     if head == to_find:
#         output_list.append(head)
#         return tail, output_list
#     else:
#         output_list.append(head)
#         return get_block(tail, to_find, output_list)


def get_string(input_list: list, string: str = "") -> Union[Tuple[list, str], Error]:
    if (len(input_list) == 0):
        raise StringNotClosedError(string)
    head, *tail = input_list
    if head[-1] == "\"":
        return  string + head, tail
    else:
        return get_string(tail, string + head + " ") 



def __split(to_split: list, to_find: Union[str, list] = None) -> Union[Error, Tuple[list, list]]:
    to_remove = [' ']

    head, *tail = to_split
    if len(tail) == 0 or head == to_find:
        return [head], tail

    if head[0] == "\"":
        head, tail = get_string(to_split)

    if head == "(":
        head, tail = __split(tail, ")")
        head = ["("] + head

    if head == "[":
        head, tail = __split(tail, "]")
        head = ["["] + head

    if head[0] == "#":
        saved = head
        head, tail = __split(tail, "$")
        head = [saved] + head

    if to_find is None:
        return [head] + __split(tail, to_find)[0], []
    else:
        tmp, tail = __split(tail, to_find)
        tmp = [head] + tmp
        return tmp, tail

def split(to_split: list)-> Union[Error, list]:
    return __split(to_split)[0]

def preprocessor(file_contents: str) -> Union[list, Error]:
    # Convert to list
    input_list = file_contents.split()
    print(input_list)

    # Remove spaces and enters.
    split_chars = split(input_list)
    print(split_chars)

    # Return preprocessed input
    return split_chars


def tokenize(processed: list) -> list:
    return processed


def lexer(file_contents: str) -> list:
    processed = preprocessor(file_contents)
    tokenized = tokenize(processed)
    return tokenized
