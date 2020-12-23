from lexer import lexer
from parser import parser
from excecute import excecute
import sys


def main(file_contents: str) -> int:
    lexed = lexer(file_contents)
    parsed = parser(lexed)
    exit_code = excecute(parsed)


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

    main(file_contents)
