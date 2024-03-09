"""
This module is responsible for linking the GUI and Control (FSM) components
to the main operations, which are represented here as tasks.

Tasks that are not ready will be replaced with their corresponding imitated versions.
"""
from abc import ABC, abstractmethod
import asyncio
import inspect
import random

from typing import Type

from dg_gui_finite_state_machine import (DgState, InfluEventSet,
                                         state_change_due_to_event,
                                         gui_control_dict)

REAL_USE: bool = False # True
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
    """
    async def execute(self) -> int:
        # Implementation or pass if not ready
        pass

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
                 real_task_class: Type[MyTask],
                 imitated_class: Type[MyTask],
                 answers: tuple[str, ...],
                 task_name: str) -> None:
        self.real_task_class: Type[MyTask] = real_task_class
        self.imitated_class: Type[MyTask] = imitated_class
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
            return self.real_task_class() # Instantiate a real, runnable object
        return self.imitated_class(
                        answers= self.answers,
                        task_name= self.task_name) # Instantiate a runnable imitator object

    async def run_task(self) -> str:
        """
        This method execute sthe functionality
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
        print(gui_control_dict["rec_state"])    # DgState. ...

async def carry_out_process() -> None:
    """
    This function carries out a main process of application
    using MyTask classes and TaskFactory.
    """
    loc_rec_state: DgState = gui_control_dict["rec_state"]
    if not loc_rec_state.name.startswith("BUSY_"):
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
    if loc_events:
        loc_answers: tuple[str, ...] = (loc_answer1,
                                        loc_answer2,
                                        loc_events[0])
    else:
        loc_answers: tuple[str, ...] = (loc_answer1,
                                        loc_answer2)
    loc_factory: TaskFactory = None
    if   loc_rec_state == DgState.BUSY_RAND_GEN_INPUT:
        loc_factory = TaskFactory(real_task_class=CommonRealTask,
                                imitated_class= CommonImitatedTask,
                                answers= loc_answers,
                                task_name= loc_rec_state.description)
    elif loc_rec_state == DgState.BUSY_INP_TEXT_READ:
        loc_factory = TaskFactory(real_task_class=CommonRealTask,
                                imitated_class= CommonImitatedTask,
                                answers= loc_answers,
                                task_name= loc_rec_state.description)
    elif loc_rec_state == DgState.BUSY_TECHN_INP_PRESENT:
        loc_factory = TaskFactory(real_task_class=CommonRealTask,
                                imitated_class= CommonImitatedTask,
                                answers= loc_answers,
                                task_name= loc_rec_state.description)
    elif loc_rec_state == DgState.BUSY_FIRST_ORDER_CREATE:
        loc_factory = TaskFactory(real_task_class=CommonRealTask,
                                imitated_class= CommonImitatedTask,
                                answers= loc_answers,
                                task_name= loc_rec_state.description)
    elif loc_rec_state == DgState.BUSY_SEARCH_OPTIM_EXEC:
        loc_factory = TaskFactory(real_task_class=CommonRealTask,
                                imitated_class= CommonImitatedTask,
                                answers= loc_answers,
                                task_name= loc_rec_state.description)
    elif loc_rec_state == DgState.BUSY_RECENT_OPT_PRESENT:
        loc_factory = TaskFactory(real_task_class=CommonRealTask,
                                imitated_class= CommonImitatedTask,
                                answers= loc_answers,
                                task_name= loc_rec_state.description)
    elif loc_rec_state == DgState.BUSY_RESULTS_PRESENT:
        loc_factory = TaskFactory(real_task_class=CommonRealTask,
                                imitated_class= CommonImitatedTask,
                                answers= loc_answers,
                                task_name= loc_rec_state.description)
    else:
        raise ValueError("Attention carry_out_processe! "
                        f"Unknown DgState sate ({loc_rec_state.value}) named {loc_rec_state.name}")
    await loc_factory.run_and_propagate_result()

# # # Just for test for here:
 # Real MyTask (potentially abstract if not fully implemented)
class TestRealTask(MyTask):
    """
    This is a test "real" task.
    """
    async def execute(self) -> int:
        # Implementation or pass if not ready
        pass

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
