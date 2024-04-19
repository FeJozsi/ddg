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
from typing import List, cast

import sys
from traceback import print_tb
from io import TextIOWrapper
from os import path

from dg_link import dg_first
from diszjunktiv_graf import Csatlakozas, Muveletcsucs
from vezerles  import Vezerles
from dg_high_level_pseudo_black_boxes import my_control_dict, adatelokeszites, iteraciok, eredmeny
from dg_standard_input import DgInpSource, DgStandardInput, my_dict_for_input
from dg_standard_input import dg_inint, dg_lastitem # , dg_inreal

from dg_exceptions import EmptyInputError, EarlyInputEOF, UnexpectedIORequest #, InputValueError

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
        self.f: TextIOWrapper | None = None    # The ResourceManager will open the input file
        self.state: str = "open"
        self.buffer: str = ""
    def serve_line(self) -> str:
        self.buffer = ""
        if self.state in ("open", "serve"):
            st: str = self.state
            assert self.f
            self.state = "busy"
            while self.state == "busy":
                buf: str = self.f.readline()
                self.buffer = buf.replace("\n","")
                # print("  >"+self.buffer)
                if not buf:
                    self.state = "eof"
                    self.f.close()
                    # break
                    if st == "open":
                        raise EmptyInputError("Input cannot be an empty file")
                    raise EarlyInputEOF("An early EOF was detected on the input file")
                if not self.buffer:
                    continue
                if self.buffer[0] == "#":
                    continue
                self.state = "serve"
        else:
            self.state = "error"
            raise UnexpectedIORequest("Unexpected subsequent operation on the input file")
        return self.buffer
    def serve_line_if_any(self) -> str:
        self.buffer = ""
        if self.state in ("open", "serve"):
            assert self.f
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
        else:
            self.state = "error"
            raise UnexpectedIORequest("Unexpected subsequent operation on the input file")
        return self.buffer
    def get_state(self) -> str:
        return self.state
    def get_source_short_attribute(self) -> str:
        return self.source_file_name
    def get_source_long_attribute(self) -> str:
        if self.state in ("open", "busy", "serve"):
            assert self.f
            return path.abspath( self.f.name)
        return ""
    def close_input(self) -> None:
        """
        This method close the input file if is still open.
        """
        if not self.state in ("eof","error","closed"):
            assert self.f
            self.f.close()
            self.state = "closed"

def print_input_data_hungarian(l_dg: Vezerles) -> None:
    """
    Prints the input data to the STDOUT in Hungarian.
    """
    print("\n\n\n** Az input adatok **")
    print("** Műveletszám, gépszám **")
    print((f"[{l_dg.muveletszam}, {l_dg.gepszam}]"))
    print("** Futás maximális ideje (sec), "
          "maximális mélységszint, "
          "lépésenkénti információ kérése **")
    print((f"[{l_dg.futas_maximalis_ideje}, {l_dg.maximalis_melysegszint}, {l_dg.info}]"))

    print("** Azon.  Gépje   Időtart.  Megelőzők         **")
    muv: Muveletcsucs
    for k in range(l_dg.muveletszam): # range(0, l_dg.muveletszam) is the same
        muv = l_dg.muvelet[l_dg.muvkod[k]]
        l: List = []                # egyelőre üres a techn. előzmény műveletek listája
        megelozo: Csatlakozas | None = cast(Csatlakozas, dg_first(muv.megelozok))   # FIRST
        while megelozo:
            if megelozo.szomszed.azonosito > 0: # a forrást és nyelőt ki kell hagyni
                l.append(megelozo.szomszed.azonosito)
            megelozo = cast(Csatlakozas, megelozo.suc)
        print((f"[{muv.azonosito:6}, {muv.gepje:6}, {muv.idotartam:8.2f},   "
               f"{str(l)} {' ' * (17-len(str(l)))}]"))
    print("** Gépeken végrehajtandó műveletek darabszáma a gépek sorrendjében **")
    # l = [l_dg.gep_muveletszama[k] for k in range(l_dg.gepszam)]
    # print(l)   These two lines are the same as the one below:
    print(l_dg.gep_muveletszama)
    print("** Művelet azonosítók a gépek sorrendjében, "
          "azaz elöl az első gépen végrehajtandók és így továb **")
    # l = [l_dg.muvelet[k].azonosito for k in range(l_dg.muveletszam)]
    l = [muv.azonosito for muv in l_dg.muvelet] #  This is the same as the one above in comment
    print(l)
    print("\n")

def print_input_data_english(l_dg: Vezerles) -> None:
    """
    Prints the input data to the STDOUT in English.
    """
    print("\n\n\n** The input data **")
    print("** Number of operations, number of machines **")
    print((f"[{l_dg.muveletszam}, {l_dg.gepszam}]"))
    print("** Maximum runtime (sec), "
          "maximum depth level, "
          "request for information per step **")
    print((f"[{l_dg.futas_maximalis_ideje}, {l_dg.maximalis_melysegszint}, {l_dg.info}]"))

    print("** Identif. Machine Duration  Predecessors       **")
    muv: Muveletcsucs
    for k in range(l_dg.muveletszam): # range(0, l_dg.muveletszam) is the same
        muv = l_dg.muvelet[l_dg.muvkod[k]]
        l: List = []                # initially empty list of technical precursor operations
        megelozo: Csatlakozas | None = cast(Csatlakozas, dg_first(muv.megelozok))   # FIRST
        while megelozo:
            if megelozo.szomszed.azonosito > 0: # sources and sinks must be omitted
                l.append(megelozo.szomszed.azonosito)
            megelozo = cast(Csatlakozas, megelozo.suc)
        print((f"[{muv.azonosito:6}, {muv.gepje:6}, {muv.idotartam:10.2f},  "
               f"{str(l)} {' ' * (17-len(str(l)))}]"))
    print("** Number of operations to be carried out on machines in order of machines **")
    # l = [l_dg.gep_muveletszama[k] for k in range(l_dg.gepszam)]
    # print(l)   These two lines are the same as the one below:
    print(l_dg.gep_muveletszama)
    print("** Operation identifiers in order of machines, "
          "i.e., starting with those to be executed on the first machine and so forth **")
    # l = [l_dg.muvelet[k].azonosito for k in range(l_dg.muveletszam)]
    l = [muv.azonosito for muv in l_dg.muvelet] # This is the same as the one above in comment
    print(str(l) + "\n")

def aktualis_optimalis_megoldas_nyomtatasa_english(l_dg: Vezerles, last_flag: bool = True) -> None:
    """
    Print recent or the last (optimal) solution
    """
    smuv: Muveletcsucs | None = None
    if last_flag:
        l_dg.megmaradt_fixalt_elek_eltavolitasa()
        l_dg.aktualis_optimalis_sorrend_visszaallitas()
    l_dg.kritikus_ut_odafele()
    l_dg.kritikus_uthosszak_visszafele()
    for k in range(l_dg.gepszam):
        smuv = l_dg.muvelet[l_dg.gep_elso_muvelete[k]]
        while smuv.gepen_elozo is not None:
            smuv = smuv.gepen_elozo
        print(f"* Order of operations on machine {k+1} *")
        print("** ID.   Source Duration     Sink **")
        while smuv is not None:
            print(f"{smuv.azonosito:6} {smuv.forrastol1:8.2f} "
                  f"{smuv.idotartam:8.2f} {smuv.nyeloig2:8.2f}")
            smuv = cast(Muveletcsucs, smuv.gepen_koveto)
    # print("* Throughput time: {:8.2f}, final lower bound (baseline): {:8.2f} *".format(
    #                           l_dg.nyelo.forrastol1,
    #                           l_dg.viszonyitasi_alap))
    # assert l_dg.nyelo
    # print(f"* Throughput time: {l_dg.nyelo.forrastol1:8.2f} *")


class MyResourceManager:
    """
    This is a ResourceManager for open and close the INPUT file
    """
    def __init__(self, name: str):
        self.name = name

    def __enter__(self) -> None:
        print(f'MyResourceManager {self.name} has been acquired')
        itf: InputTextFile = InputTextFile(arg_str_fn)
        itf.f = open(arg_str_fn, "rt", encoding= 'utf-8') # encoding= 'cp1250'
        # Propagate a new DgStandardInput to the dg_standard_input module
        my_dict_for_input["dg_input_object"] = DgStandardInput(itf)
        print(f'The {itf.get_source_long_attribute()} input file has been opened for processing')
        # Return any resource or None if no resource is needed.
        # It can be accessed with the 'as' command element in the 'with ...' command.
        # return self.name

    def __exit__(self, loc_exc_type, loc_exc_value, loc_traceback) -> None:
        dsi: DgStandardInput | None = my_dict_for_input["dg_input_object"]
        assert dsi
        itf: DgInpSource = dsi.input_source_obj
        itf.close_input()
        if loc_exc_type is not None:
            print(f"An exception of type {loc_exc_type.__name__} occurred.")
            print(f"Exception message: {loc_exc_value}")
            print("Traceback:")
            print_tb(loc_traceback)
        print(f'MyResourceManager {self.name} has been released')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python dg_main.py <input file name and/or full path>")
        sys.exit(1)

    # Get command-line arguments
    arg_str_fn = sys.argv[1]
    dg_o: Vezerles | None = None

    with MyResourceManager('for->test_dg_input_read'):
        # Perform some operations with the resource

        # Main iteration for analyzing one or more disjunctive graphs   # 1230. origin sor
        #
        while not dg_lastitem():
            dg_o = Vezerles(dg_inint(), dg_inint()) # muveletszam: int, gepszam: int
            my_control_dict["dg_o"] = dg_o          # propagate to lower levels
            my_control_dict["step_back"] = False    # initialize
            my_control_dict["my_continue"] = True   # initialize

            print("* The determination of the minimax critical path length "
                "of a directed disjunctive graph has commenced. *")
            print("* The 'engine' structure (i.e. the main utilized custom class hierarchy) *")
            dg_class_name_list: List = [x.__name__ for x in Vezerles.__mro__]
            dg_class_name_list.reverse()
            print(dg_class_name_list[1:])

            # print("** Az input adatok **")
            # print("** Műveletszám, gépszám **")
            # print((f"[{dg_o.muveletszam}, {dg_o.gepszam}]"))

            # Megelőző elemzést végez
            adatelokeszites()
            # print("** Gépeken végrehajtandó műveletek darabszáma a gépek sorrendjében **")
            # l: List = [dg_o.gep_muveletszama[k] for k in range(dg_o.gepszam)]
            # print(l)
            # print("** Művelet azonosítók a gépek sorrendjében, "
            #     "azaz elöl az első gépen végrehajtandók és így továb **")
            # l = [dg_o.muvelet[k].azonosito for k in range(dg_o.muveletszam)]
            # print(l)
            print_input_data_hungarian(dg_o)

            if dg_o.megelozo_elemzes_mast_nem_mond():
                dg_o.kezdeti_sorrend_felallitasa()
                iteraciok()
                eredmeny()
                dg_o.print_cp()
            print("* The determination of the minimax critical path length "
                "of the directed disjunctive graph has finished. *")
