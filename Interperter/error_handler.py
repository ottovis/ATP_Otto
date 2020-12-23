import operator


class Error(Exception):
    pass


class InvalidOperatorError(Error):
    def __init__(self, a: int, b: int, used_operator: operator) -> None:
        self.message = "invalid operation with " + a + \
            "  and " + b + " using: " + used_operator
        self.expression = str(a, operator, b)


class StringNotClosedError(Error):
    def __init__(self, string_block):
        self.message = "String block: \"" + string_block + "\" not properly closed"
        self.expression = string_block
