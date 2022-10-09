from lexer import lexer
from parser import parser
from compiler import compiler, printer
import sys


def main(file_contents: str, name: str) -> int:
    lexed = lexer(file_contents)
    parsed = parser(lexed)
    code, context = compiler(parsed)
    printer(code, name)
    return 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please give exactly argument pointing to the file to be executed")
        exit(-1)

    try:
        with open(sys.argv[1], mode='r') as f:
            file_contents = f.read()
    except:
        print("Try again with existing file")
        exit(-2)

    if len(file_contents) == 0:
        print("Empty file!")
        exit(-1)

    print("\n", "Exit code:", main(file_contents, sys.argv[1]))
