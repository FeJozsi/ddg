"""
This module generate random Directed Disjunctive Graphs.

Args:
    <muvszam>: number of operations that need to be executed
    <gepszam>: number of machines

    Requierments:
            gepszam > 0,  
            muvszam >= gepszam.  
            Each machine has one operation at least, and
            the result has no round-trip operation cycles.

Result:
    It produce an output text file in the  `inputs` folder of
    the recent root folder of (Python/project) environment.  
    The name template for the output file is:  
        `dg_gen_input_<muvszam>m_<gepszam>g_YYMMDDHHMISS.txt` .

TODO:
    Check the arguments for the Requierments.
"""
import sys
from traceback import print_tb
from io import TextIOWrapper
from os import path
from typing import List

import random
import datetime

class GrdgControl:
    """
    This class represents the main attributes and coroutines
    and is designed to be instantiated only once
    """
    def __init__(self, muvszam: int, gepszam: int) -> None:
        """
        Args:
            muvszam: number of operations that need to be executed
            gepszam: number of machines
        """
        self.muvszam: int = muvszam
        self.gepszam: int = gepszam
        self.mach_suggest: int = 0
        self.l: List[OperationIntput] = []  # all produced random OperationIntput
        self.dtn = datetime.datetime.now()
        self.file_name: str = ("dg_gen_input_" +
                               f"{muvszam}m_{gepszam}g_" +
                               self.dtn.strftime("%Y%m%d%H%M%S") + ".txt")
        self.f: TextIOWrapper = None

    def next_mach_suggest(self) -> int:
        """
        This method steps forward one of the suggested machine ID cycle
        """
        self.mach_suggest += 1
        self.mach_suggest = (self.mach_suggest - 1) % self.gepszam + 1
        return self.mach_suggest
    def random_percent(self) -> int:
        """
        This method randomly determines a number in order to use percentage probability.
        """
        return random.randint(0,99)
    def random_mach(self) -> int:
        """
        This method generates a random machine ID, but also, as far aspossible,
        takes care of the requierment any machine has an operation at least.
        We can use a different probability value in random_percent() >= 66.
        """
        return (self.next_mach_suggest()
                if self.random_percent() >= 66 or self.muvszam <= self.gepszam * 2.5
                else random.randint(1, self.gepszam))
    def random_pred(self) -> int:
        """
        This method randomly determines the number of predecessors
        required for an operation.  
        It can use any other different intervals within reasonable limits.
        """
        return random.randint(1,self.gepszam)
    def random_float(self) -> float:
        """
        This method randomly determines the execution time of an operation.  
        It can use any different intervals of positive numbers.
        """
        return round(random.uniform(17.0, 50.0), 2)
    def random_predec(self) -> int:
        """
        This method states a random Operation's ID for the set of predecessors.
        """
        return random.randint(1,self.muvszam)

class OperationIntput:
    """
    This class scripts a random oparation
    """
    def __init__(self, oi_id: int, machine: int, duration: float) -> None:
        """
        Args:
            oi_id:        An integer ID between 1 .. operations' number (grdg.muvszam)
            machine:      An integer ID between 1 .. machines' number (grdg.gepszam)
            duration:     The execution time of the operation
            predecessors: The list of operations' ID which operations have to precede self
        """
        self.oi_id: int = oi_id             # An integer ID between 1 .. operations' number
        self.machine: int = machine         # An integer ID between 1 .. machines' number
        self.duration: float = duration     # The execution time of the operation
        self.predecessors: List[int] = []   # The list of operations' ID which
                                            #   operations have to precede one with the self.ID
    def oi_description(self) -> str:
        """
        Produce the string format of object
        """
        s: str = str(self.predecessors)
        return (f"[{self.oi_id:6},{self.machine:6},{self.duration:10.2f}, {s}]")
    def establish_dependencies(self) -> None:
        """
        This method sets the predecessors of the operations but not for all
        """
        if grdg.random_percent() >= 45:
            w: int = grdg.random_pred() # the number of predecessors we will put in
            for _ in range(w):
                p: int = grdg.random_predec()
                if (not p == self.oi_id and
                    not p in self.predecessors and
                    not self.oi_id in grdg.l[p-1].predecessors):
                    # self.predecessors.append(p)
                    grdg.l[p-1].predecessors.append(self.oi_id)

def check_for_cycle(
    cobj: OperationIntput,     # one of operations under test
    pred: List[int],           # id list of predecessors to check
    cpath: List[int],          # actual path has been passed yet
    clevel: int,               # level of recursion
    circle: List[int]          # the first found cyrcle, if any
) -> None:
    """
    This function searches for cycles in the techological graph of established Operations.  
    It serves the result in the circle parameter.  
    The circle will be empty when no cycles in the graph.
    
    Args:
        cobj: one of the operations under test
        pred: id list of predecessors to check
        cpath: actual path has been passed yet
        clevel: level of recursion of the method
        circle: the first found cyrcle, if any
    """
    if circle:
        return
    if cobj.oi_id in cpath[1:] or len(cpath) > len(grdg.l):
        circle.extend(cpath)  # Preserve the original circle list argument. Just we extend it
        return
    if not pred:
        return
    p: int = pred[0]
    if p == cobj.oi_id:
        cpath.append(p)
        circle.extend(cpath)  # Preserve the original circle list
        return
    if pred:
        check_for_cycle(cobj= cobj,
                        pred= pred[1:],
                        cpath= cpath[0:],
                        clevel= clevel,
                        circle= circle)
        if circle:
            return
    if not p in cpath:
        cpath.append(p)
        pred = grdg.l[p-1].predecessors # predecessors
        check_for_cycle(cobj= cobj,
                        pred= pred[0:],
                        cpath= cpath[0:],
                        clevel= clevel + 1,
                        circle= circle)
        if circle:
            return
    else:
        i = cpath.index(p)
        cpath.append(p)
        circle.extend(cpath[i:])  # Preserve the original circle list

def break_cycles() -> None:
    """
    This function resolves all cycles in the techological graph if any.  
    It lists the cases of resolved cycles into the terminal window.
    """
    while True:
        i: int = 0
        x: OperationIntput = None
        y: OperationIntput = None
        for o in grdg.l:
            circle = []
            check_for_cycle(cobj= o,
                            pred= o.predecessors[0:],
                            cpath= [o.oi_id],
                            clevel= 1,
                            circle= circle)
            if circle:
                break
            i += 1
        if circle:
            if circle[0] == circle[-1] and len(circle) >= 2:
                print("The", ",".join(str(oid) for oid in circle), "cycle was broken.")
                x = grdg.l[circle[0]-1]
                y = grdg.l[circle[-2]-1]
                if len(x.predecessors) > len(y.predecessors):
                    x.predecessors.remove(circle[1])
                else:
                    y.predecessors.remove(circle[-1])
            else:
                print(
                    "*----- This result in the parameter circle seems unmanageable: " +
                    str(circle) +
                    " ! -----*")
                break
        elif i >= len(grdg.l):
            break

def generate_random_input() -> None:
    """
    This is the main function in this module.  
    It produces a new random directed disjunctive technological graph.
    """

    # Set the seed for the random number generator mechanism for reproducibility (optional)
    # random.seed(4242420001) # You can use any integer value as the seed
    # Reset the seed (optional)
    random.seed()  # Resets the seed to a realy random value series

    # grdg: GrdgControl = GrdgControl(muvszam= muvszam, gepszam= gepszam) < It has made earlier

    satisfied: bool = False      # does any machine have an operation at least?
    inner_order: List[int] = []  # Inner order of operations
    machine_load: List[int] = [] # How many operations is for the machine?

    grdg.f.write(
        "# This is a text file describing a directed disjunctive graph "
        "(for calculating the minmax critical path of it).\n"
        "# Created at date-time: {dt}\n"
        "# (The lines starting with # are comments.)\n"
        "# Number of operations: {muvszam}, number of machines: {gepszam}\n"
        "[{muvszam}, {gepszam}]\n"
        "# Maximum run time: {mrt} sec (0 = no limit), maximum depth level: {mdl} "
        "(0 = no limit), step-by-step information: {info}\n"
        "[{mrt}, {mdl}, {info}]\n\n".
        format(dt=str(grdg.dtn)[:-7],
               muvszam=grdg.muvszam,
               gepszam=grdg.gepszam,
               mrt=20.0,
               mdl=15,
               info=False)
    )
    while not satisfied:
        grdg.l.clear()
        grdg.mach_suggest = 0
        inner_order.clear()
        machine_load.clear()
        for i in range(grdg.muvszam):
            grdg.l.append(OperationIntput( oi_id= i + 1,
                                           machine=  grdg.random_mach(),
                                           duration= grdg.random_float()))
        satisfied = True         # We suppose having a success
        for k in range(grdg.gepszam): # check if the machine k+1 does have a machine?
            w: int = 0
            for o in grdg.l:
                if o.machine == k + 1:
                    inner_order.append(o.oi_id)
                    w += 1
            if not w:
                satisfied = False
                break
            machine_load.append(w) # store the number of operations on the machine k+1

    grdg.f.write(
        "# Number of operations per machine "
        "(we need provide a positive integer for each machine, "
        "and their sum should give the total number of operations):\n"
    )
    grdg.f.write(str(machine_load) + "\n\n")
    grdg.f.write(
        "# Identifiers of operations grouped by machines "
        "in sequential order, with the identifiers of operations "
        "on the first machine listed first, and so forth.\n"
         "#   We need to specify an equal number of positive number IDs "
         "as there are operations. These number IDs must be distinct, "
         "with none exceeding the total number of operations:)\n"
    )
    grdg.f.write(str(inner_order) + "\n\n")

    for o in grdg.l:
        o.establish_dependencies()

    grdg.f.write(
        "# The following data describes the operations, "
        "each in a separate row, as many rows as there are operations. "
        "Their order is arbitrary.\n"
        "#   The structure of these rows: operation identifier, executing machine, "
        "execution time, list of identifiers of preceding operations, that may be empty:\n"
    )

    for o in grdg.l:
        if grdg.random_percent() >= 33: # This is also heuristic, it is an option:
            o.predecessors = []         # clear it sometimes.

    break_cycles()

    for o in grdg.l:
        grdg.f.write(o.oi_description() +"\n")

class MyResourceManager:
    """
    This is a ResourceManager for open and close the OUTPUT file of module appropriately
    """
    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        print(f'MyResourceManager {self.name} has been acquired')
        grdg.f = open(".\\inputs\\" + grdg.file_name, "wt", encoding= 'utf-8')
        print(f'The {path.abspath( grdg.f.name)} output file has been opened to write')
        # Return any resource or None if no resource is needed.
        # It can be accessed with the 'as' command element in the 'with ...' command.
        # return self.name

    def __exit__(self, loc_exc_type, loc_exc_value, loc_traceback):
        grdg.f.close()
        if loc_exc_type is not None:
            print(f"An exception of type {loc_exc_type.__name__} occurred.")
            print(f"Exception message: {loc_exc_value}")
            print("Traceback:")
            print_tb(loc_traceback)
        print(f'MyResourceManager {self.name} has been released')

if len(sys.argv) != 3:
    print("Usage: python generate_random_dg_problem.py <number of operations> <number of machines>")
    sys.exit(1)

# Get command-line arguments
arg_numb_op = int(sys.argv[1])
arg_numb_mc = int(sys.argv[2])

grdg: GrdgControl = GrdgControl(muvszam= arg_numb_op, gepszam= arg_numb_mc)
"""
It is the main control object of process
"""
with MyResourceManager('for->generate_random_dg_problem'):
    # Perform some operations with the resource
    generate_random_input()
