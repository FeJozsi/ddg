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

class UnexpectedValueType(ValueError):
    """
        Unexpected data value type on the input file
    """

class InputValueError(ValueError):
    """
        Bad value from the input
    """

class TooLargeDescription(FileNotFoundError):
    """
        The DDG description file is too large (> 500 kb)
    """

class UnknownEncodingError(FileNotFoundError):
    """
        The encoding of the DDG description file is unknown. It is neither UTF-8 nor CP1250
    """

class InputSyntaxError(SyntaxError):
    """
        The DDG description input file has a SyntaxError.
    """

class MissingOutputPath(FileNotFoundError):
    """
        The output folder for the file to be generated does not exist
    """

class InaccessibleOutputPath(FileNotFoundError):
    """
        The output file can not be opened for write
    """
