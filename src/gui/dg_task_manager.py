"""
This module is responsible for linking the GUI and Control (FSM) components
to the main operations, which are represented here as tasks.

Tasks that are not ready will be replaced with their corresponding imitated versions.
"""
import os

from abc import ABC, abstractmethod
import asyncio
import inspect
import random

from typing import Type

from dg_gui_finite_state_machine import (DgState, InfluEventSet, NewsType,
                                         state_change_due_to_event,
                                         gui_control_dict)

from dg_gui_own_event_stack import my_event_stack
from dg_gui_window import MainWindow, get_main_window_instance
from dg_exceptions import (EmptyInputError, EarlyInputEOF, UnexpectedValueType,
                           InputValueError, TooLargeDescription, UnknownEncodingError)
from dg_main import InputTextFile
from dg_standard_input import DgStandardInput, dg_inint, dg_inreal, my_dict_for_input # DgInpSource,

REAL_USE: bool = True # False for TEST only, running without real core tasks
"""
This global variable is suitable to distinguish the real mode and the imitated test mode.
     False: the modul runs always an instance of the imitators definitely.
     True:  the modul tries to run the real class objects,
              if their Class already is not ABC (abstract).
"""
# Abstract Base MyTask
class MyTask(ABC):
    """
    Abstract Base MyTask
    """
    @abstractmethod
    async def execute(self) -> int:
        """
        This is the funcionality must be carried out
        """
    @abstractmethod
    def ready(self)-> bool:
        """
        This method can be used to distinguish if the class ready to use.
        """

class CommonRealTask(MyTask):
    """
    This is a common "real" task for tasks whose implementation has not yet been begun.
    This will be the ancestor of real tasks.
    """
    def __init__(self,
                 answers: tuple[str, ...],
                 task_name: str) -> None:
        super().__init__()
        self.answers: tuple[str, ...] = answers
        self.task_name: str = task_name
        self.main_window: MainWindow = get_main_window_instance()
    async def execute(self) -> int:
        # Implementation or pass if not ready
        return 1

class A(CommonRealTask):
    """
    Template for real tasks.
    """
    def __init__(self,
                 answers: tuple[str, ...],
                 task_name: str) -> None:
        super().__init__(answers= answers, task_name= task_name)
    async def execute(self) -> int:
        # Implementation or pass if not ready
        try:
            pass
        except Exception as _: # pylint: disable=W0718 # Catching too general broad-exception-caught
            pass
        return 1


def check_encoding(file_path):
    """ Check the file access and detect code page"""
    fp: str = file_path
    file_size: int
    try:
        file_size = os.path.getsize(fp)
    except OSError as e:
        raise FileNotFoundError(str(e) + "\n") from e

    if file_size > 500 * 1025:
        raise TooLargeDescription("The DDG's description file is too large (> 500 kb)")

    try:
        with open(file_path, "rt",  encoding='cp1250') as file:
            file.read()
        return 'cp1250'
    except UnicodeDecodeError:
        pass
    except OSError as e:
        raise FileNotFoundError(str(e) + "\n") from e

    try:
        with open(file_path, "rt", encoding='utf-8') as file:
            file.read()
        return 'utf-8'
    except UnicodeDecodeError:
        pass
    except OSError as e:
        raise FileNotFoundError(str(e) + "\n") from e

    try:
        with open(file_path, "rt") as file: # pylint: disable=W1514 # Using open without explicitly
            file.read()               #           ... specifying an encoding (unspecified-encoding)
        raise UnknownEncodingError("The encoding of the DDG description file is unknown. "
                                "It is neither UTF-8 nor CP1250")
    except OSError as e:
        raise FileNotFoundError(str(e) + "\n") from e
    except UnicodeError as e:
        raise UnknownEncodingError("The encoding of the DDG description file is unknown. "
                                "It is neither UTF-8 nor CP1250.\n") from e

def my_ordinal(n: int) -> str:
    """ This function returns the text equivalent of a number in the form of an ordinal name """
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix

def my_gep_ind(first_ind: list[int], last_ind: list[int], op_index: int) -> str:
    """
        Search for the index of range 
    """
    ret_value: int = -1
    b: int = min(len(first_ind), len(last_ind))
    for i in range(0, b):
        if first_ind[i] <= op_index <= last_ind[i]: # chained-comparison ...
            ret_value = i                           # ... which just means they are "and"ed together
            break
    return ret_value


def test_read() -> None:
    """
    This is the main function in the BusyInpTextRead.execute().  
    It reads and checks data from input.
    Also it sends messages to the gui with the read data.
    By the way, it does not store data persistently for now.
    """
    index: int = 1
    str_ind: str
    m : int = dg_inint() # Number of operations
    if not bool(m) or m < 1:
        raise InputValueError("Error! The 1st number (data) from the input is incorrect. "
                              "The number of operations must be positive.")
    index += 1
    # print("__" + dg_input_object.input_obj.state)

    g : int = dg_inint() # Number of machines
    if not bool(g) or g < 1 or g > m:
        raise InputValueError("Error! The 2nd number (data) from the input is incorrect. "
                              "The number of machines must be positive, but less then" 
                              "the number of operations.")
    index += 1
    # print(f"[{m}, {g}]")

    fut_ido: float = dg_inreal() # Maximum run time
    if fut_ido is None or fut_ido < 0:
        raise InputValueError("Error! The 3rd number (data) from the input is incorrect. "
                              "The maximum run time can not be negative.")
    index += 1
    max_mely: int = dg_inint() # Maximum depth level of solution tree
    if max_mely is None or max_mely < 0:
        str_ind = my_ordinal(index)
        raise InputValueError(f"Error! The {str_ind} number (data) from the input is incorrect. "
                              "The maximum depth level of solution tree can not be negative.")
    index += 1                           # True if dg_inint() else False
    info_demand: bool = bool(dg_inint()) # Step-by-step information
    if info_demand is None:
        str_ind = my_ordinal(index)
        raise InputValueError(f"Error! The {str_ind} number (data) from the input is incorrect. "
                              "The step-by-step information is missing.")
    index += 1
    # print(f"[{fut_ido}, {max_mely}, {info_demand}]")

    # Number of operations per machine (we need provide a positive integer for each machine,
    #  and their sum should give the total number of operations):
    ind_1: str = my_ordinal(index)
    ind_2: str = my_ordinal(index + g - 1)
    gep_muv_szam: list[int] = []
    for _ in range(0, g):
        gep_muv_szam.append(dg_inint())
        if not bool(gep_muv_szam[-1]) or gep_muv_szam[-1] < 1 or gep_muv_szam[-1] + g - 1 > m:
            str_ind = my_ordinal(index)
            raise InputValueError(f"Error! The {str_ind} number (data) from the input is incorrect."
                                  "\nYou need provide a positive integer for each machine "
                                  f"in the sequence starting at {ind_1} and ending at {ind_2} data,"
                                  " and their sum should give the total number of operations.")
        index += 1
    if m != sum(gep_muv_szam):
        raise InputValueError("Error! You need provide a positive integer for each machine "
                              f"in the sequence starting at {ind_1} and ending at {ind_2} data,"
                              " and their sum should give the total number of operations.")
    # print (gep_muv_szam)

    # Identifiers of operations grouped by machines in sequential order,
    #   with the identifiers of operations on the first machine listed first, and so forth.
    #   We need to specify an equal number of positive number IDs as there are operations.
    #   These number IDs must be distinct, with none exceeding the total number of operations)
    ind_1: str = my_ordinal(index)
    ind_2: str = my_ordinal(index + m - 1)
    muv_azon: list[int] = []
    for _ in range(0, m):
        muv_azon.append(dg_inint())
        if not bool(muv_azon[-1]) or muv_azon[-1] < 1 or muv_azon[-1] > m:
            str_ind = my_ordinal(index)
            raise InputValueError(f"Error! The {str_ind} number (data) from the input is incorrect."
                                  "\nYou need provide a unique positive integer for each operation "
                                  f"in the sequence starting at {ind_1} and ending at {ind_2} data,"
                                  "\nthat can be used later as an operation ID. The value must be "
                                  "less or equal the number of operations.")
        index += 1
    if m != len(set(muv_azon)):
        raise InputValueError("Error! You need provide all operation ID just once and exactly once "
                              f"in the sequence starting at {ind_1} and ending at {ind_2} data.")
    # print (muv_azon)

    test_read_2(g, m, fut_ido, max_mely, info_demand)

    gep_first_ind: list[int] = []
    gep_last_ind: list[int] = []
    test_read_3(gep_muv_szam, gep_first_ind, gep_last_ind)

    test_read_4(muv_azon, gep_first_ind, gep_last_ind, index)

def test_read_2(g, m, fut_ido, max_mely, info_demand) -> None:
    """
    It sends messages to the gui with the read data
    """
    my_event_stack.emit_message_on_gui("TR01", NewsType.FILL_NB_MACHINE, m_text= str(g))
    my_event_stack.emit_message_on_gui("TR02", NewsType.FILL_NB_OPER, m_text= str(m))
    my_event_stack.emit_message_on_gui("TR03", NewsType.FILL_TIMEOUT, m_text= str(fut_ido))
    my_event_stack.emit_message_on_gui("TR04", NewsType.FILL_MAX_DEPTH, m_text= str(max_mely))
    my_event_stack.emit_message_on_gui("TR05", NewsType.FILL_LOG_DETAIL, m_text= str(info_demand))

def test_read_3(gep_muv_szam, gep_first_ind, gep_last_ind) -> None:
    """
    It prepares for continue reading and checking data from input
    """
    # for i in range(0, len(gep_muv_szam)):  # consider-using-enumerate
    for i, gepen in enumerate(gep_muv_szam):
        if i == 0:
            gep_first_ind.append(0)
            gep_last_ind.append(gepen - 1)
        else:
            gep_first_ind.append(gep_last_ind[-1] + 1)
            gep_last_ind.append(gep_last_ind[-1] + gepen)

def test_read_4(muv_azon, gep_first_ind, gep_last_ind, index) -> None:
    """
    It continues reading and checking data from input.
    """

    # The following data describes the operations, each in a separate row, as many rows as
    #   there are operations, in the basic case. Their order is arbitrary.
    #   The structure of these rows: operation identifier,
    #                                executing machine ID nb,
    #                                execution time,
    #                                list of identifiers of preceding operations, that may be empty
    m: int = len(muv_azon)
    g: int = len(gep_first_ind)
    azonosito: int
    gepje: int
    vegrehajt_ido: float
    megelozok: list[int]
    muv_ids_new: list[int] = []
    muv_index: int
    my_gep_id: int
    for _ in range(0, m):
        azonosito = dg_inint()
        if not bool(azonosito) or azonosito < 1 or azonosito > m:
            str_ind = my_ordinal(index)
            raise InputValueError(f"Error! The {str_ind} number (data) from the input is incorrect."
                                  f" We found {azonosito}.\n"
                                  "Instead of this, you need provide a positive number as an "
                                  "operation ID. The value must be less or equal the number "
                                  "of operations.")
        index += 1
        muv_ids_new.append(azonosito)

        gepje = dg_inint()
        if not bool(gepje) or gepje < 1 or gepje > g:
            str_ind = my_ordinal(index)
            raise InputValueError(f"Error! The {str_ind} number (data) from the input is incorrect."
                                  f" We found {gepje}.\n"
                                  "Instead of this, you need provide a positive number as an "
                                  "machine ID. The value must be less or equal the number "
                                  "of machines.")
        muv_index = muv_azon.index(azonosito)
        if not gep_first_ind[gepje - 1] <= muv_index <= gep_last_ind[gepje - 1]:
            my_gep_id = my_gep_ind(first_ind= gep_first_ind,
                                   last_ind= gep_last_ind,
                                   op_index= muv_index) + 1
            str_ind = my_ordinal(index)
            raise InputValueError(f"Error! The {str_ind} number (data) from the input is incorrect."
                                  f" We found {gepje} as machine ID. The proper value would be "
                                  f"{my_gep_id}.\n"
                                  "Because the ID of the operation in the previous listing is "
                                  "in the range belonging to the machine mentioned later.\n"
                                  "Identifiers of operations grouped by machines in sequential "
                                  "order, with the identifiers of operations on the first machine "
                                  "listed first, and so forth, in that previous operation ID list.")
        index += 1

        vegrehajt_ido = dg_inreal()
        if not bool(vegrehajt_ido) or vegrehajt_ido < 0.0000001:
            str_ind = my_ordinal(index)
            raise InputValueError(f"Error! The {str_ind} number (data) from the input is incorrect."
                                  f" We found {vegrehajt_ido}.\n"
                                  "Instead of this, you need provide a positive number as the "
                                  "execution time of operation.")
        index += 1

        megelozok = []
        seged: int = dg_inint()
        while seged >= 0:
            if not bool(seged) or seged < 1 or seged > m:
                str_ind = my_ordinal(index)
                raise InputValueError(f"Error! The {str_ind} number (data) from the input is wrong."
                                      f" We found {seged}.\n"
                                      "Instead of this, you need provide a positive number as an "
                                      "identifier (operation ID) of a preceding operation. "
                                      "The ID must be less or equal the number of operations.")
            if seged == azonosito or seged in megelozok:
                str_ind = my_ordinal(index)
                raise InputValueError(f"Error! The {str_ind} number (data) from the input is wrong."
                                      f" We found {seged}.\n"
                                      "You should not serve an operation ID as a preceding "
                                      "operation which equal with the base operation ID or "
                                      "it has already loaded as a preceding.")
            megelozok.append(seged)
            index += 1
            seged = dg_inint()
        # ms: str = str(megelozok)
        # print(f"[{azonosito}, {gepje}, {vegrehajt_ido}, {ms}]")

    if m != len(set(muv_ids_new)):
        raise InputValueError("Error! You need provide all operation ID just once and exactly once "
                              "in the sequence of detailed data of operations.")

class BusyInpTextRead(CommonRealTask):
    """
    The real task for DgState.BUSY_INP_TEXT_READ status.
    "Read of input text"
    """
    def __init__(self,
                 answers: tuple[str, ...],
                 task_name: str) -> None:
        super().__init__(answers= answers, task_name= task_name)
    async def execute(self) -> int:
        file_path: str = self.main_window.form_frame.text_form.file_input.text()
        loc_encoding: str
        try:
            loc_encoding = check_encoding(file_path)
            # read via text mode
            with open(file_path, "rt", encoding= loc_encoding) as loc_file:
                itf: InputTextFile = InputTextFile(file_path)
                itf.f = loc_file
                # Propagate a new DgStandardInput to the dg_standard_input module
                my_dict_for_input["dg_input_object"] = DgStandardInput(itf)

                test_read()
        except (FileNotFoundError, TooLargeDescription, UnknownEncodingError, InputValueError,
                EmptyInputError, EarlyInputEOF, UnexpectedValueType) as e:
            my_event_stack.emit_message_on_gui("TR11",
                           m_text= "An exception occurred, the task was interrupted.\n\n"
                           "Details:\n" + str(e))
            return 0
        except (MemoryError, SystemError, OverflowError, SyntaxError,
                LookupError, ImportError, AssertionError, AttributeError,
                BufferError, NameError, ArithmeticError, StopAsyncIteration,
                StopIteration, TypeError): # , RecursionError
            raise # by itself is used to re-raise the current exception
        except Exception as e: # pylint: disable=W0718 # Catching too general broad-exception-caught
            my_event_stack.emit_message_on_gui("TR12",
                           m_text= "An UNEXPECTED exception occurred, the task was interrupted.\n\n"
                           "Details:\n" + str(e))
            return 0
        return 1
    # Existance of ready() method signs the Class is not ABC
    def ready(self) -> bool:
        return True

class CommonImitatedTask(MyTask):
    """
    This is a common test "imitated" task for tasks whose implementation has not yet been finished.
    """
    def __init__(self,
                 answers: tuple[str, ...],
                 task_name: str) -> None:
        super().__init__()
        self.answers: tuple[str, ...] = answers
        self.task_name: str = task_name

    async def execute(self) -> int:
        print(self.task_name, "> Executing as imitated task.")
        loc_time_out = random.randint(2,5)
        await asyncio.sleep(loc_time_out) # sleep(5)
        print("Executing imitated task ended.")
        if random.randint(0,99) > 85:
            loc_ret_val = 0
        else:
            loc_ret_val = random.randint(1,len(self.answers)-1)
        return loc_ret_val # 0
    # Existance of ready() method signs the Class is not ABC
    def ready(self) -> bool:
        return True


# MyTask Factory
class TaskFactory:
    """
    This class creates relation between FSM and the tasks
    """
    def __init__(self,
                 real_task_class: Type[CommonRealTask],
                 imitated_class: Type[CommonImitatedTask],
                 answers: tuple[str, ...],
                 task_name: str) -> None:
        self.real_task_class: Type[CommonRealTask] = real_task_class
        self.imitated_class: Type[CommonImitatedTask] = imitated_class
        self.answers: tuple[str, ...] = answers
        self.task_name: str = task_name
    def get_task(self) -> MyTask:
        """
        This method gives an appropriate object depending on the REAL_USE global variable,
        to run it using its execute() method.

        REAL_USE global variable:
            False: the method serves a new imitator object definitely.
            True:  the method tries to serve a new real object,
                     if its Class already is not ABC.
        """
        if REAL_USE and not inspect.isabstract(self.real_task_class):
            return self.real_task_class(
                            answers= self.answers,
                            task_name= self.task_name) # Instantiate a real, runnable object
        return self.imitated_class(
                        answers= self.answers,
                        task_name= self.task_name) # Instantiate a runnable imitator object

    async def run_task(self) -> str:
        """
        This method executes the functionality
        via a task object.

        REAL_USE global variable:
            False: the method runs the imitator's object definitely.
            True:  the method tries to run the real class' object,
                     if their Class already is not ABC.
        """
        loc_task: MyTask = self.get_task()
        loc_result: int = await loc_task.execute()
        return self.answers[loc_result]
    async def run_and_propagate_result(self) -> None:
        """
        This method executes the functionality
        via a task object, and propagates the result
        vie the state_change_due_to_event() function of FSM.

        REAL_USE global variable:
            False: the method runs the imitator's object definitely.
            True:  the method tries to run the real class' object,
                     if their Class already is not ABC.
        """
        loc_respond: str = await self.run_task()
        print(self.task_name, ":", loc_respond)
        loc_event: InfluEventSet = InfluEventSet(by_process= loc_respond)
        state_change_due_to_event(influ_event= loc_event)

async def carry_out_process() -> None:
    """
    This function carries out a main process of application
    using MyTask classes and TaskFactory.
    """
    loc_rec_state: DgState = gui_control_dict["rec_state"]
    if not (loc_rec_state.name.startswith("BUSY_") and loc_rec_state.influ_events):
        return
    loc_events: list[str] = [event for event
                                   in loc_rec_state.influ_events.by_process
                                   if "Failed" in event]
    loc_answer1: str = loc_events[0]
    loc_events            = [event for event
                                   in loc_rec_state.influ_events.by_process
                                   if "Done" in event]
    loc_answer2: str = loc_events[0]
    loc_events            = [event for event
                                   in loc_rec_state.influ_events.by_process
                                   if "Success" in event]
    loc_answers: tuple[str, ...]
    if loc_events:
        loc_answers = (loc_answer1, loc_answer2, loc_events[0])
    else:
        loc_answers = (loc_answer1, loc_answer2)
    loc_factory: TaskFactory | None = None
    if   loc_rec_state == DgState.BUSY_RAND_GEN_INPUT:
        loc_factory = TaskFactory(real_task_class=CommonRealTask, # type: ignore
                                imitated_class= CommonImitatedTask,
                                answers= loc_answers,
                                task_name= loc_rec_state.description)
    elif loc_rec_state == DgState.BUSY_INP_TEXT_READ:
        loc_factory = TaskFactory(real_task_class=BusyInpTextRead, # type: ignore
                                imitated_class= CommonImitatedTask,
                                answers= loc_answers,
                                task_name= loc_rec_state.description)
    elif loc_rec_state == DgState.BUSY_TECHN_INP_PRESENT:
        loc_factory = TaskFactory(real_task_class=CommonRealTask, # type: ignore
                                imitated_class= CommonImitatedTask,
                                answers= loc_answers,
                                task_name= loc_rec_state.description)
    elif loc_rec_state == DgState.BUSY_FIRST_ORDER_CREATE:
        loc_factory = TaskFactory(real_task_class=CommonRealTask, # type: ignore
                                imitated_class= CommonImitatedTask,
                                answers= loc_answers,
                                task_name= loc_rec_state.description)
    elif loc_rec_state == DgState.BUSY_SEARCH_OPTIM_EXEC:
        loc_factory = TaskFactory(real_task_class=CommonRealTask, # type: ignore
                                imitated_class= CommonImitatedTask,
                                answers= loc_answers,
                                task_name= loc_rec_state.description)
    elif loc_rec_state == DgState.BUSY_RECENT_OPT_PRESENT:
        loc_factory = TaskFactory(real_task_class=CommonRealTask, # type: ignore
                                imitated_class= CommonImitatedTask,
                                answers= loc_answers,
                                task_name= loc_rec_state.description)
    elif loc_rec_state == DgState.BUSY_RESULTS_PRESENT:
        loc_factory = TaskFactory(real_task_class=CommonRealTask, # type: ignore
                                imitated_class= CommonImitatedTask,
                                answers= loc_answers,
                                task_name= loc_rec_state.description)
    else:
        raise ValueError("Attention carry_out_process! "
                        f"Unknown DgState sate ({loc_rec_state.value}) named {loc_rec_state.name}")
    await loc_factory.run_and_propagate_result()

# # # Just for test for here:
 # Real MyTask (potentially abstract if not fully implemented)
class TestRealTask(MyTask):
    """
    This is a test "real" task. It is not ready yet.
    """
    async def execute(self) -> int:
        # Implementation or pass if not ready
        return 1

# Imitated MyTask
class ImitatedTask(MyTask):
    """
    This is a test "imitated" task.
    """
    def __init__(self,
                 answers: tuple[str, ...],
                 task_name: str) -> None:
        super().__init__()
        self.answers: tuple[str, ...] = answers
        self.task_name: str = task_name
    async def execute(self) -> int:
        print(self.task_name, "> Executing as imitated task.")
        loc_time_out = random.randint(2,5)
        await asyncio.sleep(loc_time_out) # sleep(5)
        print("Executing imitated task ended.")
        if random.randint(0,99) > 85:
            loc_ret_val = 0
        else:
            loc_ret_val = random.randint(1,len(self.answers)-1)
        return loc_ret_val # 0
    # Existance of ready() method signs the Class is not ABC
    def ready(self) -> bool:
        return True

async def async_main():
    """
    This function is for test only
    """
    # global REAL_USE
    # REAL_USE = False # for test mode, without linked with main functionality

    loc_factory = TaskFactory(real_task_class=TestRealTask,
                              imitated_class= ImitatedTask,
                              answers= ("Done","Failed","Success"),
                              task_name= "Test task")
    # Assuming RealTask class is not fully implemented and thus abstract,
    # the factory will return an instance of ImitatedTask class instead.
    result_val = await loc_factory.run_task()
    print(loc_factory.task_name, ":", result_val)

    print(" . " * 33)

    print(gui_control_dict["rec_state"])
    state_change_due_to_event(influ_event= InfluEventSet(by_process="Start Eventloop"))
    print(gui_control_dict["rec_state"])    # DgState.IDLE_INIT

    state_change_due_to_event(influ_event= InfluEventSet(by_forms="Radio Text"))
    print(gui_control_dict["rec_state"])    # DgState.IDLE_INPUT_TEXT_DEF
    state_change_due_to_event(influ_event= InfluEventSet(by_forms="Filled (T)"))
    print(gui_control_dict["rec_state"])    # DgState.IDLE_INP_TEXT_SATISFIED

    state_change_due_to_event(influ_event= InfluEventSet(by_buttons=["","","Read"]))
    print(gui_control_dict["rec_state"])    # DgState.BUSY_INP_TEXT_READ

    await carry_out_process()

# # # Example usage:
if __name__ == '__main__':
    asyncio.run(async_main())
