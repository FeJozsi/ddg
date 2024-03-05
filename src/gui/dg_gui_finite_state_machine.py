"""
This module includes the resources for a control GUI that operates
based on Finite State Machine (FSM) principles.  
It provides the necessary states and transitions for managing GUI operations,
facilitating decision-making, observation, and iteration processes within a
user interface.
"""

from enum import Enum, auto
from typing import List, Union

class MyButton(Enum):
    """
    This class lists the three used buttons
    """
    BACK = 0
    ACTION = 1
    NEXT = 2

class InfluEventSet:
    """
    Represents a set of events whitch can change the given state of GUI
    or could be occurred by the GUI and / or System.
    """
    def __init__(self, by_process: List[str] = None, by_forms: List[str] = None,
                       by_buttons: List[str] = None):
        self.by_process: List[str] = ["Confirmed Close Win"]
        if by_process is not None:
            self.by_process = by_process
        self.by_forms: List[str] = []
        if by_process is not None:
            self.by_forms = by_forms
        self.by_buttons: List[str] = ["", "", ""]
        if by_buttons is not None and len(by_buttons) == 3:
            self.by_buttons = by_buttons

    def is_watching_all(self, event_set):
        """
        Check if self InfluEventSet is interested in one specified by the parameter,
        moreover in its all segments
        """
        e_s: InfluEventSet = event_set
        existance: bool = False
        ret_val: bool = True
        if e_s.by_process:      # It is not important for   all(...)  ...,
            existance = True    # ... but we want return True if there is a real match at least.
            if not all(elem in self.by_process for elem in e_s.by_process):
                ret_val = False
        if e_s.by_forms:
            existance = True
            if not all(elem in self.by_forms for elem in e_s.by_forms):
                ret_val = False
        if any(e_s.by_buttons[i] for i in range(3)):
            existance = True
            if not all(
                    not e_s.by_buttons[i] or e_s.by_buttons[i] == self.by_buttons[i]
                    for i in range(3)):
                ret_val = False
        if not existance:
            return False
        return ret_val
    def is_not_interested(self, event_set):
        """
        Check if self InfluEventSet is not interested in one specified by the parameter at all.
        """
        e_s: InfluEventSet = event_set
        ret_val: bool = True
        if any(elem in self.by_process for elem in e_s.by_process):
            ret_val = False
        if any(elem in self.by_forms for elem in e_s.by_forms):
            ret_val = False
        # if (False if not e_s.by_buttons[0] else e_s.by_buttons[0] == self.by_buttons[0] or
        #     False if not e_s.by_buttons[1] else e_s.by_buttons[1] == self.by_buttons[1] or
        #     False if not e_s.by_buttons[2] else e_s.by_buttons[2] == self.by_buttons[2]):
        #     ret_val = False
        if any(e_s.by_buttons[i] and e_s.by_buttons[i] == self.by_buttons[i] for i in range(3)):
            ret_val = False
        return ret_val
    def is_watching(self, event_set):
        """
        Check if self InfluEventSet is interested in one specified by the parameter,
        in one of its segments at least
        """
        e_s: InfluEventSet = event_set
        if ( not e_s.by_process and
             not e_s.by_forms and
             all(not e_s.by_buttons[i] for i in range(3))
        ):
            return False
        return not self.is_not_interested(e_s)

class DimStep(Enum):
    """
    Represents a dimension of states within the GUI's Finite State Machine (FSM).
    Each DimStep corresponds to a distinct phase in the control process,
    describeing what is happening.
    
    Members:
        INIT_WAIT:       Before eventloop starts.
        DECIDE:          Related to decision preparation or decision-making processes.
        WATCH:           Focused on observation or monitoring by the user without immediate action.
        ONE_ITERATION:   A value indicating a single iteration of the process.
        CONTINUOUS_ITER: A value representing continuous cycles of the process.
        SOME_ITER:       That point the process is essentially independent
                            of how many iterations must be done.
    """
    INIT_WAIT = auto()
    DECIDE = auto()
    WATCH = auto()
    ONE_ITERATION = auto()
    CONTINUOUS_ITER = auto()
    SOME_ITER = auto()

class DimProp(Enum):  # dimProperty
    """
    Represents a dimension of states within the GUI's Finite State Machine (FSM).
    Each DimProp corresponds to a distinct phase in the control process,
    describeing what we have earned yet.

    Members:
        INIT_NONE:     Initiate state.
        INP_TYPE:      The type of input has defined.
        INP_DESCRIPT:  The input has defined.
        INPUT_AS_IS:   Input has read. The task has been defined
        INPUT_TECHN:   Established the lower limit
        FIRST_ORDER:   Created the first order of the operations on the machines
        RECENT_RESULT: Achieved the recent result
        LAST_RESULT:   Achieved the last result
    """
    INIT_NONE = auto()
    INP_TYPE = auto()
    INP_DESCRIPT = auto()
    INPUT_AS_IS = auto()
    INPUT_TECHN = auto()
    FIRST_ORDER = auto()
    RECENT_RESULT = auto()
    LAST_RESULT = auto()

class DimBusy(Enum):
    """
    Represents a dimension of states within the GUI's Finite State Machine (FSM).
    Each DimBusy corresponds to a distinct type of happenings are going on.
    
    Members:
        BUSY:         The program works, the eventloop is not started yet.
        MISSING_IDLE: The definition of the input is incomplete
        ORDER_IDLE:   Waiting for data or a command by the user.
        ERROR_IDLE:   The program sends an error message
        WAIT_IDLE:    The program works. It can be paused by user default.
        WATCH_IDLE:   The user makes observation or monitoring without immediate action.
    """
    BUSY = auto()
    MISSING_IDLE = auto()
    ORDER_IDLE = auto()
    ERROR_IDLE = auto()
    WAIT_IDLE = auto()
    WATCH_IDLE = auto()

class DimInpT(Enum): # dimInputType
    """
    Represents a dimension of states within the GUI's Finite State Machine (FSM).
    Each DimInpT corresponds to a distinct type of the input.

    Members:
        TYPE_NONE:  The type of input does not have defined yet.
        RANDOM_GEN: Input is random generated by the program.
        TEXT_INPUT: The input comes from a text file from an URL.
        BOTH_TYPE:  The determination of input data has been completed successfully.
                        The rest of the process is essentially independent of the type of input.
    """
    TYPE_NONE = auto()
    RANDOM_GEN = auto()
    TEXT_INPUT = auto()
    BOTH_TYPE = auto()

class DgState(Enum):
    """
    Represents the states within the GUI's Finite State Machine (FSM).

    Members:
        1	INIT	                The program started
        2	IDLE_INIT               Deciding type of input
        3	IDLE_RANDOM_GEN	        Form for random generation
        4	IDLE_RAND_GEN_SATISFIED	Form for random gen. filled
        5	BUSY_RAND_GEN_INPUT	    Random generation of input
        6	IDLE_RAND_GEN_ERROR	    Error of Random generation
        7	IDLE_INPUT_TEXT_DEF	    Form for input text file
        8	IDLE_INP_TEXT_SATISFIED	Form for inp. text file filled
        9	BUSY_INP_TEXT_READ	    Read of input text
        10	IDLE_INP_TEXT_ERROR	    Error of Reading input text
        11	IDLE_HAVE_TECHN_INPUT	Deciding about present preliminary analysis
        12	BUSY_TECHN_INP_PRESENT 	Preliminary analysis for lower bound
        13	IDLE_TECHN_INP_ERROR	Error of preliminary analysis
        14	IDLE_TECHN_INP_PRESENT	View of preliminary analysis
        15	IDLE_HAVE_LOWER_BOUND	Deciding about present first order
        16	BUSY_FIRST_ORDER_CREATE	Create first order
        17	IDLE_FIRST_ORD_ERROR	Error of first order
        18	IDLE_FIRST_ORD_PRESENT 	View of first order
        19	IDLE_HAVE_ROOT_INPUT	Deciding about search steps (s by s or cont)
        20	BUSY_SEARCH_OPTIM_EXEC	Searching optimum
        21	IDLE_SEARCH_OPT_ERROR	Error of searching optimum
        22	IDLE_SEARCH_OPT_PAUSE	Deciding about present recent
        23	BUSY_RECENT_OPT_PRESENT	Prepare recent for present
        24	IDLE_RECENT_OPT_ERROR	Error of prepare recent
        25	IDLE_RECENT_OPT_PRESENT	View of recent
        26	IDLE_SEARCH_DONE	    Deciding about present last result
        27	BUSY_RESULTS_PRESENT	Prepare last result for present
        28	IDLE_RESULTS_ERROR	    Error of prepare last result
        29	IDLE_RESULTS_PRESENT	View of last result
        30	STOP	                Stop Program
    """
    INIT                    =(auto(), "The program started")
    IDLE_INIT               =(auto(), "Deciding type of input")
    IDLE_RANDOM_GEN         =(auto(), "Form for random generation")
    IDLE_RAND_GEN_SATISFIED =(auto(), "Form for random gen. filled")
    BUSY_RAND_GEN_INPUT     =(auto(), "Random generation of input")
    IDLE_RAND_GEN_ERROR     =(auto(), "Error of Random generation")
    IDLE_INPUT_TEXT_DEF     =(auto(), "Form for input text file")
    IDLE_INP_TEXT_SATISFIED =(auto(), "Form for inp. text file filled")
    BUSY_INP_TEXT_READ      =(auto(), "Read of input text")
    IDLE_INP_TEXT_ERROR     =(auto(), "Error of Reading input text")
    IDLE_HAVE_TECHN_INPUT   =(auto(), "Deciding about present preliminary analysis")
    BUSY_TECHN_INP_PRESENT  =(auto(), "Preliminary analysis for lower bound")
    IDLE_TECHN_INP_ERROR    =(auto(), "Error of preliminary analysis")
    IDLE_TECHN_INP_PRESENT  =(auto(), "View of preliminary analysis")
    IDLE_HAVE_LOWER_BOUND   =(auto(), "Deciding about present first order")
    BUSY_FIRST_ORDER_CREATE =(auto(), "Create first order")
    IDLE_FIRST_ORD_ERROR    =(auto(), "Error of first order")
    IDLE_FIRST_ORD_PRESENT  =(auto(), "View of first order")
    IDLE_HAVE_ROOT_INPUT    =(auto(), "Deciding about search steps (s by s or cont)")
    BUSY_SEARCH_OPTIM_EXEC  =(auto(), "Searching optimum")
    IDLE_SEARCH_OPT_ERROR   =(auto(), "Error of searching optimum")
    IDLE_SEARCH_OPT_PAUSE   =(auto(), "Deciding about present recent")
    BUSY_RECENT_OPT_PRESENT =(auto(), "Prepare recent for present")
    IDLE_RECENT_OPT_ERROR   =(auto(), "Error of prepare recent")
    IDLE_RECENT_OPT_PRESENT =(auto(), "View of recent")
    IDLE_SEARCH_DONE        =(auto(), "Deciding about present last result")
    BUSY_RESULTS_PRESENT    =(auto(), "Prepare last result for present")
    IDLE_RESULTS_ERROR      =(auto(), "Error of prepare last result")
    IDLE_RESULTS_PRESENT    =(auto(), "View of last result")
    STOP                    =(auto(), "Stop Program")

    def __init__(self, numb: int, desc: str):
        self.nb: int = numb
        self.step: DimStep = None
        self.property: DimProp = None
        self.busy: DimBusy = None
        self.input_type: DimInpT = None
        self.influ_events: InfluEventSet = None
        self.description : str = desc

    def set_prop(self, dim_step: DimStep, dim_property: DimProp,
                 dim_busy: DimBusy, dim_input_type: DimInpT):
        """
        This method fills the DgState member's attributes
        """
        self.step: DimStep = dim_step
        self.property: DimProp = dim_property
        self.busy: DimBusy = dim_busy
        self.input_type: DimInpT = dim_input_type

    def set_influ_events(self, event_set: InfluEventSet):
        """
        This method fills the DgState member's influ_events attribute
        """
        self.influ_events: InfluEventSet = event_set

    @classmethod
    def states_by_prop(cls, prop: Union[Enum, int, str]):
        """
        Returns a list of DgState having the property set by paramater
        """
        ret_val: List[DgState] = []
        if isinstance(prop, DimStep):
            ret_val = [dg_state for dg_state in cls if dg_state.step == prop]
        if isinstance(prop, DimProp):
            ret_val = [dg_state for dg_state in cls if dg_state.property == prop]
        if isinstance(prop, DimBusy):
            ret_val = [dg_state for dg_state in cls if dg_state.busy == prop]
        if isinstance(prop, DimInpT):
            ret_val = [dg_state for dg_state in cls if dg_state.input_type == prop]
        if isinstance(prop, int):
            ret_val = [dg_state for dg_state in cls if dg_state.nb == prop]
        if isinstance(prop, str):
            ret_val = [dg_state for dg_state in cls if prop.lower() in dg_state.description.lower()]
        return ret_val


DgState.INIT                    .set_prop(
                DimStep.INIT_WAIT, DimProp.INIT_NONE    , DimBusy.BUSY        , DimInpT.TYPE_NONE )
DgState.IDLE_INIT               .set_prop(
                DimStep.DECIDE   , DimProp.INIT_NONE    , DimBusy.ORDER_IDLE  , DimInpT.TYPE_NONE )
DgState.IDLE_RANDOM_GEN         .set_prop(
                DimStep.DECIDE   , DimProp.INP_TYPE     , DimBusy.MISSING_IDLE, DimInpT.RANDOM_GEN)
DgState.IDLE_RAND_GEN_SATISFIED .set_prop(
                DimStep.DECIDE   , DimProp.INP_TYPE     , DimBusy.ORDER_IDLE  , DimInpT.RANDOM_GEN)
DgState.BUSY_RAND_GEN_INPUT     .set_prop(
                DimStep.DECIDE   , DimProp.INP_DESCRIPT , DimBusy.WAIT_IDLE   , DimInpT.RANDOM_GEN)
DgState.IDLE_RAND_GEN_ERROR     .set_prop(
                DimStep.DECIDE   , DimProp.INP_DESCRIPT , DimBusy.ERROR_IDLE  , DimInpT.RANDOM_GEN)
DgState.IDLE_INPUT_TEXT_DEF     .set_prop(
                DimStep.DECIDE   , DimProp.INP_TYPE     , DimBusy.MISSING_IDLE, DimInpT.TEXT_INPUT)
DgState.IDLE_INP_TEXT_SATISFIED .set_prop(
                DimStep.DECIDE   , DimProp.INP_TYPE     , DimBusy.ORDER_IDLE  , DimInpT.TEXT_INPUT)
DgState.BUSY_INP_TEXT_READ      .set_prop(
                DimStep.DECIDE   , DimProp.INP_DESCRIPT , DimBusy.WAIT_IDLE   , DimInpT.TEXT_INPUT)
DgState.IDLE_INP_TEXT_ERROR     .set_prop(
                DimStep.DECIDE   , DimProp.INP_DESCRIPT , DimBusy.ERROR_IDLE  , DimInpT.TEXT_INPUT)
DgState.IDLE_HAVE_TECHN_INPUT   .set_prop(
                DimStep.DECIDE   , DimProp.INPUT_AS_IS  , DimBusy.ORDER_IDLE  , DimInpT.BOTH_TYPE )
DgState.BUSY_TECHN_INP_PRESENT  .set_prop(
                DimStep.WATCH    , DimProp.INPUT_AS_IS  , DimBusy.WAIT_IDLE   , DimInpT.BOTH_TYPE )
DgState.IDLE_TECHN_INP_ERROR    .set_prop(
                DimStep.WATCH    , DimProp.INPUT_AS_IS  , DimBusy.ERROR_IDLE  , DimInpT.BOTH_TYPE )
DgState.IDLE_TECHN_INP_PRESENT  .set_prop(
                DimStep.WATCH    , DimProp.INPUT_TECHN  , DimBusy.WATCH_IDLE  , DimInpT.BOTH_TYPE )
DgState.IDLE_HAVE_LOWER_BOUND   .set_prop(
                DimStep.DECIDE   , DimProp.INPUT_TECHN  , DimBusy.ORDER_IDLE  , DimInpT.BOTH_TYPE )
DgState.BUSY_FIRST_ORDER_CREATE .set_prop(
                DimStep.WATCH    , DimProp.INPUT_TECHN  , DimBusy.WAIT_IDLE   , DimInpT.BOTH_TYPE )
DgState.IDLE_FIRST_ORD_ERROR    .set_prop(
                DimStep.WATCH    , DimProp.INPUT_TECHN  , DimBusy.ERROR_IDLE  , DimInpT.BOTH_TYPE )
DgState.IDLE_FIRST_ORD_PRESENT  .set_prop(
                DimStep.WATCH    , DimProp.FIRST_ORDER  , DimBusy.WATCH_IDLE  , DimInpT.BOTH_TYPE )
DgState.IDLE_HAVE_ROOT_INPUT    .set_prop(
                DimStep.DECIDE   , DimProp.FIRST_ORDER  , DimBusy.ORDER_IDLE  , DimInpT.BOTH_TYPE )
DgState.BUSY_SEARCH_OPTIM_EXEC  .set_prop(
                DimStep.SOME_ITER, DimProp.RECENT_RESULT, DimBusy.WAIT_IDLE   , DimInpT.BOTH_TYPE )
DgState.IDLE_SEARCH_OPT_ERROR   .set_prop(
                DimStep.SOME_ITER, DimProp.RECENT_RESULT, DimBusy.ERROR_IDLE  , DimInpT.BOTH_TYPE )
DgState.IDLE_SEARCH_OPT_PAUSE   .set_prop(
                DimStep.DECIDE   , DimProp.RECENT_RESULT, DimBusy.ORDER_IDLE  , DimInpT.BOTH_TYPE )
DgState.BUSY_RECENT_OPT_PRESENT .set_prop(
                DimStep.WATCH    , DimProp.RECENT_RESULT, DimBusy.WAIT_IDLE   , DimInpT.BOTH_TYPE )
DgState.IDLE_RECENT_OPT_ERROR   .set_prop(
                DimStep.WATCH    , DimProp.RECENT_RESULT, DimBusy.ERROR_IDLE  , DimInpT.BOTH_TYPE )
DgState.IDLE_RECENT_OPT_PRESENT .set_prop(
                DimStep.WATCH    , DimProp.RECENT_RESULT, DimBusy.WATCH_IDLE  , DimInpT.BOTH_TYPE )
DgState.IDLE_SEARCH_DONE        .set_prop(
                DimStep.DECIDE   , DimProp.LAST_RESULT  , DimBusy.ORDER_IDLE  , DimInpT.BOTH_TYPE )
DgState.BUSY_RESULTS_PRESENT    .set_prop(
                DimStep.WATCH    , DimProp.LAST_RESULT  , DimBusy.WAIT_IDLE   , DimInpT.BOTH_TYPE )
DgState.IDLE_RESULTS_ERROR      .set_prop(
                DimStep.WATCH    , DimProp.LAST_RESULT  , DimBusy.ERROR_IDLE  , DimInpT.BOTH_TYPE )
DgState.IDLE_RESULTS_PRESENT    .set_prop(
                DimStep.WATCH    , DimProp.LAST_RESULT  , DimBusy.WATCH_IDLE  , DimInpT.BOTH_TYPE )
DgState.STOP                    .set_prop(
                DimStep.INIT_WAIT, DimProp.INIT_NONE    , DimBusy.BUSY        , DimInpT.TYPE_NONE )

# # # Example usage:
# print(DgState.INIT)         # Output: DgState.INIT
# print(DgState.INIT.step)    # Output: DimStep.INIT_WAIT
# print(DgState.STOP.busy)    # Output: DimBusy.BUSY
# print(DgState.STOP)         # Output: DgState.STOP
# print(DgState.states_by_prop(DimStep.WATCH))
# print(DgState.states_by_prop(DimProp.LAST_RESULT))
# print(DgState.states_by_prop(DimBusy.BUSY))
# print(DgState.states_by_prop(DimInpT.RANDOM_GEN))
# print(DgState.states_by_prop(27))
# print(DgState.states_by_prop("fill"))
