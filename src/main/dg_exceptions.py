"""
    This module collects the common used custom exceptions.
"""

class EmptyInputError(EOFError):
    """
        Custom exception to reject empty or non-existent or unavailable input.
        (e.g.: "Input cannot be an empty file")
    """

class EarlyInputEOF(EOFError):
    """
        Custom exception for refuse an incomplete input.
        (e.g.: "An early EOF was detected on the input file")
    """

class UnexpectedIORequest(RuntimeError):
    """
        Unexpected subsequent operation on the input file
    """

class InputValueError(ValueError):
    """
        Bad value from the input
    """

class UnexpectedValueType(ValueError):
    """
        Unexpected data value type on the input file
    """