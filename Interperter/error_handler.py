import operator


class Error(Exception):
    pass


class InvalidOperatorError(Error):
    def __init__(self, a: int, b: int, used_operator: operator) -> None:
        self.message = "invalid operation with " + str(a) + \
            "  and " + str(b) + " using: " + str(used_operator)
        self.expression = str(a) + str(used_operator) + str(b)


class StringNotClosedError(Error):
    def __init__(self, string_block: str):
        self.message = "String block: \"" + string_block + "\" not properly closed"
        self.expression = string_block


class NoEndTokenError(Error):
    def __init__(self):
        self.message = "No end of program token, dont forget to close with $$"


class CodeBlockNotClosedError(Error):
    def __init__(self, code_block: list):
        self.message = "Code block: \"", code_block, "\" not properly closed"
        self.expression = code_block


class BreakFromTopLevelError(Error):
    def __init__(self):
        self.message = "Not in a loop, so ^ has no meaning"


class BreakFromMainError(Error):
    def __init__(self):
        self.message = "Not in a Macro, so @ has no meaning"


class InvalidAssignmentError(Error):
    # Error thrown because of invalid types, so type hinting is a bit hard
    def __init__(self, a: None, b: None):
        self.message = "Invalid Assignment: " + str(a) + " = " + str(b)
