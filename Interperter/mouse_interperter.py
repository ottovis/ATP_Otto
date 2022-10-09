from typing import Tuple
try:
    from Interperter.lexer import lexer
    from Interperter.mse_parser import parser
    from Interperter.excecute import excecute
except:
    from lexer import lexer
    from mse_parser import parser
    from excecute import excecute
import sys


def main(file_contents: str) -> int:
    lexed = lexer(file_contents)
    parsed = parser(lexed)
    exit_code = excecute(parsed)
    return exit_code


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please give exactly argument pointing to the file to be executed")
        exit(-1)

    # try:
    with open(sys.argv[1], mode='r') as f:
        file_contents = f.read()
    # except:
    #     print("Try again with existing file")
    #     exit(-2)

    if len(file_contents) == 0:
        print("Empty file!")
        exit(-1)

    exit_code = main(file_contents)
    print( )
