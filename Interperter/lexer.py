import functools
from typing import Union, Tuple
import operator
import math

from error_handler import *
from symbols import *


def get_block(input_list: list, to_find: str, output_list: list = []) -> Union[Tuple[list, list], Error]:
    if (len(input_list) == 0):
        raise CodeBlockNotClosedError(output_list)
    head, *tail = input_list
    if head == to_find:
        return tail, output_list + head
    else:
        return get_block(tail, output_list + head)


def get_string(input_list: list, string: str = "\"") -> Union[Tuple[list, str], Error]:
    if (len(input_list) == 0):
        raise StringNotClosedError(string)
    head, *tail = input_list
    if head == "\"":
        return tail, string + head
    else:
        return get_string(tail, string + head)


def split(input_list: list, to_remove: list = [' ']) -> Union[list, Error]:
    if len(input_list) == 0:
        return []
    head, *tail = input_list
    if head == "\"":
        tail, head = get_string(tail, head)
    if head == "[":
        tail, head = get_block(tail, head)
    if head == "(":
        tail, head = get_block(tail, head)
    if head == "#":
        tail, head = get_block(tail, '$')

    if head in to_remove:
        return split(tail)

    else:
        return_value = split(tail)
        return_value.insert(0, head)
        return return_value



def preprocessor(file_contents: str) -> Union[list, Error]:
    # Convert to list
    input_list = list(file_contents)
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
