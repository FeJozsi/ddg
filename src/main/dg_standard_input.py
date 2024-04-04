"""
This module encapsulates the functionality of the SIMULA'67's *standard input*.  
The information describing a Directed Disjunctive Graph may originate from any source
that satisfies the requirements of the `DgInpSource` abstract base class (ABC)
defined in this module.  
When constructing a `DgStandardInput` object, we need to share a valid object that conforms
to the properties of DgInpSource in the constructor's parameter.
"""
from collections.abc import Iterable
from abc import ABC, abstractmethod

from typing import List, Any # , Dict, Optional
from ast import literal_eval

from typing_extensions import deprecated # i m port functools (for the same: @deprecated)?!?!

from dg_exceptions import UnexpectedValueType

class DgInpSource(ABC):
    """
    This class is the origin of the data describing a Directed Disjunctive Graph.
    """
    @abstractmethod
    def serve_line(self) -> str:
        """
        This method serves a new row for processing.
        It does not unconditionally tolerate depending on the implementation that
        there is no more data on the input.

        Raises:
            EmptyInputError: Custom exception to reject empty or non-existent or unavailable input.
            EarlyInputEOF: Custom exception for refuse an incomplete input.
            UnexpectedIORequest: Unexpected subsequent operation on the input file
        """
    @abstractmethod
    def serve_line_if_any(self) -> str:
        """
        This method serves a new row for processing.  
        It tolerates the first time when there is no more data on the input,
        it just sets the "eof" status.

        Raises:
            UnexpectedIORequest: Unexpected subsequent operation on the input file
        """
    @abstractmethod
    def get_state(self) -> str:
        """
        This method serves the state of input.  
        Publicly, it must be "serve" in normal.  
        It may be "eof", "error" and "closed" also.
        """
    # @abstractmethod
    # def set_state(self, s: str) -> None:
    #     pass
    # @abstractmethod
    # def get_source_type(self) -> str:
    #     pass
    @abstractmethod
    def get_source_short_attribute(self) -> str:
        """
        For example input file name.
        """
    @abstractmethod
    def get_source_long_attribute(self) -> str:
        """
        For example input file name with absolute path.
        """
    @abstractmethod
    def close_input(self) -> None:
        """
        Close the input source.
        """

# class Input_text_file:
#     def __init__(self, source_file: str) -> None:
#         self.source_file: str = source_file
#         self.f = open(source_file, "rt", encoding='cp1250')
#         self.state: str = "open"
#         self.buffer: str = None
#     def serve_line(self) -> str:
#         self.buffer = None
#         if self.state in ("open", "serve"):
#             self.state = "busy"
#             while self.state == "busy":
#                 buf: str = self.f.readline()
#                 self.buffer = buf.replace("\n","")
#                 # print("  >"+self.buffer)
#                 if not buf:
#                     self.state = "eof"
#                     self.f.close()
#                     break
#                 if not self.buffer: continue
#                 if self.buffer[0] == "#": continue
#                 self.state = "serve"
#                 break
#         else: self.state = "error"
#         return self.buffer
#     def close_input(self) -> None:
#         if not self.state in ("eof","error","closed"):
#             self.f.close()
#             self.state = "closed"

class DgStandardInput:
    """
    This class serves as the SIMULA'67's standard input.  
    When constructing we need to share a valid object that conforms
    to the properties of DgInpSource in the constructor's parameter.
    """
    def __init__(self, input_source_obj: DgInpSource) -> None:
        """
        Args:
            input_source_obj: refers to a valid (not ABC) `DgInpSource` object
        """
      # self.source_type: str = source_type
      # self.source_attribute: str = source_attribute
      # self.input_source_obj: Any = (Input_text_file(source_attribute)
      #                               if source_type == "text_file"
      #                               else None)
        self.input_source_obj: DgInpSource =  input_source_obj
        self.dg_buffer: str = self.input_source_obj.serve_line()
        self.dg_list_buff: List = self.dg_my_eval() # literal_eval(self.dg_buffer)
        self.dg_index: int = 0
      # assert not self.dg_lastitem(), ( # As an assert, it is a bad solutin, ...
      #     "Alert DgStandardInput()! Not waited EOF at first using of input."
      # )  # mostly, without rows above. With ... if not self.dg_lastitem()
           #  ... would better; but it is a job of invoker.
    def ask_line_when_necessary(self, only_ping: bool = False) -> None:
        """
        This method asks for a new input row if it is necessary.
        """
        if self.input_source_obj.get_state() == "serve":
            if self.dg_index >= len(self.dg_list_buff):
                if only_ping:
                    self.dg_buffer = self.input_source_obj.serve_line_if_any()
                else:
                    self.dg_buffer = self.input_source_obj.serve_line()
                if self.input_source_obj.get_state() == "serve":
                    self.dg_list_buff = self.dg_my_eval() # literal_eval(self.dg_buffer)
                else:
                    self.dg_list_buff = []
                self.dg_index = 0
    def dg_my_eval(self) -> List:
        """
        This method gives the values in self.dg_buffer as a list of values.
        """
        values_as_is: Any = literal_eval(self.dg_buffer)
        if values_as_is is None:
            return []
        if isinstance(values_as_is, list):
            return values_as_is
        if isinstance(values_as_is, Iterable) and not isinstance(values_as_is, (str, bytes)):
            return list(values_as_is)
        return [values_as_is]
    def dg_inint(self) -> int:
        """
        This method represents SIMULA'67's ININT.
        It serves an int from the input.
        """
        ret_value: int = -1 # default hiba van
        self.ask_line_when_necessary()
        if (not self.input_source_obj.get_state() == "serve" or
            self.dg_index >= len(self.dg_list_buff)):
            ret_value = -1
        elif isinstance(self.dg_list_buff[self.dg_index], bool):
            # print("---- bool -----")
            ret_value = 1 if self.dg_list_buff[self.dg_index] else 0
            self.dg_index += 1
        elif isinstance(self.dg_list_buff[self.dg_index], int):
            # print("---- int -----")
            ret_value = self.dg_list_buff[self.dg_index]
            self.dg_index += 1
        elif isinstance(self.dg_list_buff[self.dg_index], list):
            # print("---- list -----")
            self.dg_list_buff = self.dg_list_buff[self.dg_index] + [-1]
            self.dg_index = 0
            ret_value = self.dg_inint()     # recursio
        elif ( isinstance(self.dg_list_buff[self.dg_index], Iterable) and
               not isinstance(self.dg_list_buff[self.dg_index], (str, bytes)) ):
            self.dg_list_buff = list(self.dg_list_buff[self.dg_index]) + [-1]
            self.dg_index = 0
            ret_value = self.dg_inint()     # recursio
        else:
            # print("---- else -----")
            # ret_value = -1
            raise UnexpectedValueType("Unexpected data value type on the input file")
        return ret_value
    def dg_inreal(self) -> float:
        """
        This method represents SIMULA'67's INREAL.
        It serves a float from the input.
        """
        ret_value: float = -1.0 # default hiba van
        self.ask_line_when_necessary()
        if (not self.input_source_obj.get_state() == "serve" or
            self.dg_index >= len(self.dg_list_buff)):
            ret_value = -1.0
        elif isinstance(self.dg_list_buff[self.dg_index], int):
            # print("---- int -----")
            ret_value = float(self.dg_list_buff[self.dg_index])
            self.dg_index += 1
        elif isinstance(self.dg_list_buff[self.dg_index], float):
            # print("---- float -----")
            ret_value = self.dg_list_buff[self.dg_index]
            self.dg_index += 1
        else:
            # ret_value = -1.0
            raise UnexpectedValueType("Unexpected data value type on the input file")
        return ret_value
    def dg_lastitem(self) -> bool:
        """
        This method represents SIMULA'67's LASTITEM.
        It checks if the input is at the end-of-file (EOF).
        """
        ret_bool: bool = True
        self.ask_line_when_necessary(only_ping= True)
        if (not self.input_source_obj.get_state() == "serve" or
            self.dg_index >= len(self.dg_list_buff)):
            ret_bool = True
        elif isinstance(self.dg_list_buff[self.dg_index], int):
            ret_bool = False
        elif isinstance(self.dg_list_buff[self.dg_index], float):
            ret_bool = False
        elif isinstance(self.dg_list_buff[self.dg_index], bool):
            ret_bool = False
        elif isinstance(self.dg_list_buff[self.dg_index], list):
            self.dg_list_buff = self.dg_list_buff[self.dg_index] + [-1]
            self.dg_index = 0
            ret_bool = self.dg_lastitem()   # recursio
        elif ( isinstance(self.dg_list_buff[self.dg_index], Iterable) and
               not isinstance(self.dg_list_buff[self.dg_index], (str, bytes)) ):
            self.dg_list_buff = list(self.dg_list_buff[self.dg_index]) + [-1]
            self.dg_index = 0
            ret_bool = self.dg_lastitem()   # recursio
        else:
            raise UnexpectedValueType("Unexpected data value type on the input file")
        return ret_bool
    @deprecated("It must be done in a ResourceManager")
    def close_input(self) -> None:      # deprecated!
        """
        Deprecated: It must be done in a ResourceManager as DgInpSource requires it!
        """
        # self.input_source_obj.close_input()
        #  It must be done in a ResourceManager as DgInpSource requires it

    def get_state(self) -> str:
        """
        This method serves the binded DgInpSource's state.
        See DgInpSource.get_state()
        """
        return self.input_source_obj.get_state()

# my_dict_for_input: Dict[str, Optional[DgStandardInput]] = {"dg_input_object": None}
my_dict_for_input: dict[str, DgStandardInput | None] = {"dg_input_object": None}
"""
This global dictionary can content an important object:
a DgStandardInput object with "dg_input_object" key.
For proper work of functions below it must be filled before.
"""

def dg_lastitem() -> bool:
    """
    This function represents SIMULA'67's LASTITEM.
    It checks if the input is at the end-of-file (EOF).
    It propagates the DgStandardInput.dg_lastitem() method.
    """
    if (my_dict_for_input["dg_input_object"] is None
        or not isinstance(my_dict_for_input["dg_input_object"], DgStandardInput)
    ):
        return True
    o: DgStandardInput = my_dict_for_input["dg_input_object"]
    return o.dg_lastitem()

def dg_inint() -> int:
    """
    This method represents SIMULA'67's ININT.
    It serves an int from the input.
    It propagates the DgStandardInput.dg_inint() method.
    """
    if (my_dict_for_input["dg_input_object"] is None
        or not isinstance(my_dict_for_input["dg_input_object"], DgStandardInput)
    ):
        return -1
    o: DgStandardInput = my_dict_for_input["dg_input_object"]
    return o.dg_inint()

def dg_inreal() -> float:
    """
    This method represents SIMULA'67's INREAL.
    It serves a float from the input.
    It propagates the DgStandardInput.dg_inreal() method.
    """
    if (my_dict_for_input["dg_input_object"] is None
        or not isinstance(my_dict_for_input["dg_input_object"], DgStandardInput)
    ):
        return -1.0
    o: DgStandardInput = my_dict_for_input["dg_input_object"]
    return o.dg_inreal()

@deprecated("It must be done in a ResourceManager")
def dg_close_input() -> None:   # deprecated!
    """
    Deprecated: It must be done in a ResourceManager as DgInpSource requires it!
    """
    # global dg_input_object
    # try:
    #     dg_input_object
    # except NameError:
    #     dg_input_object = None
    # if dg_input_object is not None: dg_input_object.close_input()
    # dg_input_object = None
        #  It must be done in a ResourceManager as DgInpSource requires it
