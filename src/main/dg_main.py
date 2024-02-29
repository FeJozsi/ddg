"""
First of all, this main module is responsible for controlling the input
which describes the Directed Disjunctive Graphs to be solved.  
In the current version, input is expected to be provided in a text file format.

The module includes a ResourceManager for manage the input file, within
the scope of which the module executes the main job: searching for the optimal
order of operations on the machines.

Result:
    It writes the data from input and the results to the TERMINAL/Command screen.  
"""
from typing import List

import sys
from traceback import print_tb
from io import TextIOWrapper
from os import path

from vezerles  import Vezerles
from dg_high_level_pseudo_black_boxes import my_control_dict, adatelokeszites, iteraciok, eredmeny
from dg_standard_input import DgInpSource, DgStandardInput, my_dict_for_input
from dg_standard_input import dg_inint, dg_lastitem # , dg_inreal

class InputTextFile(DgInpSource):
    """
        This class will be the valid object that conforms
        to the properties of DgInpSource in the  parameter of
        DgStandardInput's constructor.  
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

class MyResourceManager:
    """
    This is a ResourceManager for open and close the INPUT file
    """
    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        print(f'MyResourceManager {self.name} has been acquired')
        itf: InputTextFile = InputTextFile(arg_str_fn)
        itf.f = open(arg_str_fn, "rt", encoding= 'utf-8') # encoding= 'cp1250'
        # Propagate a new DgStandardInput to the dg_standard_input module
        my_dict_for_input["dg_input_object"] = DgStandardInput(itf)
        print(f'The {itf.get_source_long_attribute()} input file has been opened for processing')
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
    print("Usage: python dg_main.py <input file name and/or full path>")
    sys.exit(1)

# Get command-line arguments
arg_str_fn = sys.argv[1]
dg_o: Vezerles = None

with MyResourceManager('for->test_dg_input_read'):
    # Perform some operations with the resource

    # Main iteration for analyzing one or more disjunctive graphs   # 1230. origin sor
    #
    while not dg_lastitem():
        dg_o = Vezerles(dg_inint(), dg_inint()) # muveletszam: int, gepszam: int
        my_control_dict["dg_o"] = dg_o          # propagate to lower levels
        my_control_dict["step_back"] = False    # initialize
        my_control_dict["continue"] = True      # initialize

        print("* The determination of the minimax critical path length "
              "of a directed disjunctive graph has commenced. *")
        print("* The 'engine' structure (i.e. the main utilized custom class hierarchy) *")
        dg_class_name_list: List = [x.__name__ for x in Vezerles.__mro__]
        dg_class_name_list.reverse()
        print(dg_class_name_list[1:])

        print("** Az input adatok **")
        print("** Műveletszám, gépszám **")
        print((f"[{dg_o.muveletszam}, {dg_o.gepszam}]"))

        # Megelőző elemzést végez
        adatelokeszites()
        print("** Gépeken végrehajtandó műveletek darabszáma a gépek sorrendjében **")
        l: List = [dg_o.gep_muveletszama[k] for k in range(dg_o.gepszam)]
        print(l)
        print("** Művelet azonosítók a gépek sorrendjében, "
              "azaz elöl az első gépen végrehajtandók és így továb **")
        l = [dg_o.muvelet[k].azonosito for k in range(dg_o.muveletszam)]
        print(l)

        if dg_o.megelozo_elemzes_mast_nem_mond():
            dg_o.kezdeti_sorrend_felallitasa()
            iteraciok()
            eredmeny()
            dg_o.print_cp()
        print("* The determination of the minimax critical path length "
              "of the directed disjunctive graph has finished. *")
