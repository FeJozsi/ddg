"""
    This module is unit test.  
    It presents how to use dg_standard_input.

Args:
    <input file>: the input text file to be read

Result:
    It writes the data from input to the TERMINAL/Command screen.  
"""

import sys
# sys.path.append('.\\src')  # Add the root directory's src subdir to the Python path
# print(sys.path)

from traceback import print_tb
from io import TextIOWrapper
from os import path

from typing import List

from dg_standard_input import DgInpSource, DgStandardInput, my_dict_for_input
from dg_standard_input import dg_inint, dg_inreal, dg_lastitem

class InputTextFile(DgInpSource):
    """
        This class will be the valid object that conforms
        to the properties of DgInpSource in the  parameter of
        DgStandardInput's constructor.  
        Its copy will be used as is in the main program.
    """
    def __init__(self, source_file_name: str) -> None:
        self.source_file_name: str = source_file_name
        # self.f is an implicit TextIOWrapper object
        # self.f = open(source_file_name, "rt", encoding='cp1250') # encoding='utf-8'
        self.f: TextIOWrapper = None    # The ResourceManager will open the input file
        self.state: str = "open"
        self.buffer: str = None
    def serve_line(self) -> str:
        self.buffer = None
        if self.state in ("open", "serve"):
            self.state = "busy"
            while self.state == "busy":
                buf: str = self.f.readline()
                self.buffer = buf.replace("\n","")
                # print("  >"+self.buffer)
                if not buf:
                    self.state = "eof"
                    self.f.close()
                    break
                if not self.buffer:
                    continue
                if self.buffer[0] == "#":
                    continue
                self.state = "serve"
                break
        else: self.state = "error"
        return self.buffer
    def get_state(self) -> str:
        return self.state
    def get_source_short_attribute(self) -> str:
        return self.source_file_name
    def get_source_long_attribute(self) -> str:
        if self.state in ("open", "busy", "serve"):
            return path.abspath( self.f.name)
        return ""
    def close_input(self) -> None:
        """
        This method close the input file if is still open.
        """
        if not self.state in ("eof","error","closed"):
            self.f.close()
            self.state = "closed"


# def dg_produce_the_input_object_if_not_exists() -> None:
#     global dg_input_object
#     try:
#         # if dg_input_object is None: pass
#         dg_input_object
#     except NameError:
#         dg_input_object = None
#     if dg_input_object is None:
#         p: str = "E:\\JustHere\\sajat\\Vegyes2016-\\AllasKereses\\Python\\WorkPlace\\DiszjGraf\\"
#         dg_input_object = Dg_input("text_file", p +"dg_gen_input_100m_4g_20240220111417.txt") #
#       # dg_input_object = Dg_input("text_file", p +"dg_gen_input_100m_27g_20240219205909.txt")


def teszt_olvasas() -> None:
    """
    This is the main function in this module.  
    It writes the data from input to the TERMINAL/Command screen.
    """
    m : int = dg_inint()
    # print("__" + dg_input_object.input_obj.state)
    g : int = dg_inint()
    print(f"[{m}, {g}]")


    fut_ido: float = dg_inreal()
    max_mely: int = dg_inint()
    info_demand: bool = bool(dg_inint()) # True if dg_inint() else False
    print(f"[{fut_ido}, {max_mely}, {info_demand}]")

    gep_muv_szam: List[int] = []
    for _ in range(0, g):
        gep_muv_szam.append(dg_inint())
    print (gep_muv_szam)

    muv_azon: List[int] = []
    for _ in range(0, m):
        muv_azon.append(dg_inint())
    print (muv_azon)

    azonosito: int = None
    gepje: int = None
    vegrehajt_ido: float = None
    megelozok: List[int] = None

    for _ in range(0, m):
        azonosito = dg_inint()
        gepje = dg_inint()
        vegrehajt_ido = dg_inreal()
        megelozok = []
        seged: int = dg_inint()
        while seged >= 0:
            megelozok.append(seged)
            seged = dg_inint()
        m: str = str(megelozok)
        print(f"[{azonosito}, {gepje}, {vegrehajt_ido}, {m}]")

#    dg_close_input()


class MyResourceManager:
    """
    This is a ResourceManager for open and close the INPUT file under read test
    """
    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        print(f'MyResourceManager {self.name} has been acquired')
        itf: InputTextFile = InputTextFile(arg_str_fn)
        itf.f = open(arg_str_fn, "rt", encoding='cp1250') # encoding='utf-8'
        my_dict_for_input["dg_input_object"] = DgStandardInput(itf)
        print(f'The {itf.get_source_long_attribute()} input file has been opened to write')
        # Return any resource or None if no resource is needed.
        # It can be accessed with the 'as' command element in the 'with ...' command.
        # return self.name

    def __exit__(self, loc_exc_type, loc_exc_value, loc_traceback):
        dsi: DgStandardInput = my_dict_for_input["dg_input_object"]
        itf: InputTextFile = dsi.input_source_obj
        itf.close_input()
        if loc_exc_type is not None:
            print(f"An exception of type {loc_exc_type.__name__} occurred.")
            print(f"Exception message: {loc_exc_value}")
            print("Traceback:")
            print_tb(loc_traceback)
        print(f'MyResourceManager {self.name} has been released')

if len(sys.argv) != 2:
    print("Usage: python test_dg_input_read.py <input file name and/or full path>")
    sys.exit(1)

# Get command-line arguments
arg_str_fn = sys.argv[1]

with MyResourceManager('for->test_dg_input_read'):
    # Perform some operations with the resource
    while not dg_lastitem():
        teszt_olvasas()