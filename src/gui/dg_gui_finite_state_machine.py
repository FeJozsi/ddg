"""
This module includes the resources for a control GUI that operates
based on Finite State Machine (FSM) principles.  
It provides the necessary states and transitions for managing GUI operations,
facilitating decision-making, observation, and iteration processes within a
user interface.
""" # pylint: disable=C0302 # Too many lines in module (.../1000) (too-many-lines)

from enum import Enum, auto
from typing import List, Union, TypedDict
from datetime import datetime

class NewsType(Enum):
    """
    This class lists the message types of the MyEventStack.message_on_gui signal.
    (See dg_gui_own_event_stack and dg_gui_window modules.)
    
    Members:
        ERROR_WIN:       Modal error window message
        WARNING_WIN:     Modal warning window message
        FILL_NB_MACHINE: Fill Nb. Machines
        FILL_NB_OPER:    Fill Nb. Operations
        FILL_MAX_DEPTH:  Fill Max. Depth
        FILL_TIMEOUT:    Fill Timeout
        FILL_LOG_DETAIL: Fill if ask Log Detail
        FILL_GEN_FILE:   Fill 'Save as path & name'
        FILL_STEPBYSTEP: Fill 'Step by step process'
    """
    ERROR_WIN       = auto()
    WARNING_WIN     = auto()
    FILL_NB_MACHINE = auto()
    FILL_NB_OPER    = auto()
    FILL_MAX_DEPTH  = auto()
    FILL_TIMEOUT    = auto()
    FILL_LOG_DETAIL = auto()
    FILL_GEN_FILE   = auto()
    FILL_STEPBYSTEP = auto()

class MyButton(Enum):
    """
    This class lists the three used control buttons' inside representations.
    The values used in the enum (0, 1 and 2) matter.
    """
    BACK = 0    # see button1
    ACTION = 1  # see button3
    NEXT = 2    # see button4

class InfluEventSet:
    """
    Represents a set of events whitch can change the given state of GUI
    or could be occurred by the GUI and / or System.
    """
    def __init__(self, by_process: Union[List[str], str, None] = None,
                       by_forms: Union[List[str], str, None] = None,
                       by_buttons: Union[List[str], None] = None) -> None:
        self.by_process: List[str] = [] # ["Confirmed Close Win"]
        if by_process is not None:
            if isinstance(by_process, list):
                self.by_process = by_process[0:] # make a copy!
            elif isinstance(by_process, str):
                self.by_process = [by_process]
        self.by_forms: List[str] = []
        if by_forms is not None:
            if isinstance(by_forms, list):
                self.by_forms = by_forms[0:] # make a copy!
            elif isinstance(by_forms, str):
                self.by_forms = [by_forms]
        self.by_buttons: List[str] = ["", "", ""]
        if by_buttons is not None and len(by_buttons) == 3:
            self.by_buttons = by_buttons[0:] # make a copy!
        self.triggered_dtn = datetime.now()
    def __repr__(self) -> str:
        # Filter out empty strings from each list and concatenate them
        filled_elements = [
            element
            for sublist in [self.by_process, self.by_forms, self.by_buttons] if sublist
            for element in sublist if element]
        # Join the non-empty elements with a comma
        return ">-" + ", ".join(filled_elements) + "->"

    def is_watching_all(self, event_set) -> bool:
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
                    not e_s.by_buttons[i] or
                    e_s.by_buttons[i] == self.by_buttons[i] or
                    (e_s.by_buttons[i] == "*" and self.by_buttons[i])
                    for i in range(3)
                    ):
                ret_val = False
        if not existance:
            return False
        return ret_val
    def is_not_interested(self, event_set) -> bool:
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
        if any(
            e_s.by_buttons[i] and
            ( e_s.by_buttons[i] == self.by_buttons[i] or
              ( e_s.by_buttons[i] == "*" and self.by_buttons[i] ) )
            for i in range(3)
            ):
            ret_val = False
        return ret_val
    def is_watching(self, event_set) -> bool:
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
    def dg_merge(self, event_set) -> None:
        """
        Merge self with the InfluEventSet in the event_set parameter
        """
        e_s: InfluEventSet = event_set
        self.by_process = list(set( # combining without empty and duplicate elements
            [item for item in self.by_process if item] + [item for item in e_s.by_process if item]
        ))
        self.by_forms = list(set(
            [item for item in self.by_forms if item] + [item for item in e_s.by_forms if item]
        ))
        # combining the buttons if it is possible
        if e_s.by_buttons is not None and len(e_s.by_buttons) == 3:
            merged_buttons = []
            for item1, item2 in zip(self.by_buttons, e_s.by_buttons):
                if item1 and item2:  # If both items are non-empty
                    # print(self)
                    # print(self.by_process)
                    # print(self.by_forms)
                    # print(self.by_buttons)
                    # print(item1)
                    # print(item2)
                    raise ValueError("Attention InfluEventSet.dg_merge! "
                                     "Both elements are non-empty "
                                    f"at the same position ({item1} and {item2})")
                if item1 or item2:  # If one of the items is non-empty
                    merged_buttons.append(item1 if item1 else item2)
                else:  # If both items are empty
                    merged_buttons.append("")  # or whatever you want in this case
            self.by_buttons = merged_buttons


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
        11	IDLE_HAVE_TECHN_INPUT	Deciding about presenting preliminary analysis
        12	BUSY_TECHN_INP_PRESENT 	Preliminary analysis for lower bound
        13	IDLE_TECHN_INP_ERROR	Error of preliminary analysis
        14	IDLE_TECHN_INP_PRESENT	View of preliminary analysis
        15	IDLE_HAVE_LOWER_BOUND	Deciding about presenting first order
        16	BUSY_FIRST_ORDER_CREATE	Create first order
        17	IDLE_FIRST_ORD_ERROR	Error of first order
        18	IDLE_FIRST_ORD_PRESENT 	View of first order
        19	IDLE_HAVE_ROOT_INPUT	Deciding about search flow (step by step or continuous)
        20	BUSY_SEARCH_OPTIM_EXEC	Searching optimum
        21	IDLE_SEARCH_OPT_ERROR	Error of searching optimum
        22	IDLE_SEARCH_OPT_PAUSE	Deciding about presenting recent
        23	BUSY_RECENT_OPT_PRESENT	Prepare recent for presenting
        24	IDLE_RECENT_OPT_ERROR	Error of prepare recent
        25	IDLE_RECENT_OPT_PRESENT	View of recent
        26	IDLE_SEARCH_DONE	    Deciding about presenting last result
        27	BUSY_RESULTS_PRESENT	Prepare last result for presenting
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
    IDLE_HAVE_TECHN_INPUT   =(auto(), "Deciding about presenting preliminary analysis")
    BUSY_TECHN_INP_PRESENT  =(auto(), "Preliminary analysis for lower bound")
    IDLE_TECHN_INP_ERROR    =(auto(), "Error of preliminary analysis")
    IDLE_TECHN_INP_PRESENT  =(auto(), "View of preliminary analysis")
    IDLE_HAVE_LOWER_BOUND   =(auto(), "Deciding about presenting first order")
    BUSY_FIRST_ORDER_CREATE =(auto(), "Create first order")
    IDLE_FIRST_ORD_ERROR    =(auto(), "Error of first order")
    IDLE_FIRST_ORD_PRESENT  =(auto(), "View of first order")
    IDLE_HAVE_ROOT_INPUT    =(auto(), "Deciding about search flow (step by step or continuous)")
    BUSY_SEARCH_OPTIM_EXEC  =(auto(), "Searching optimum")
    IDLE_SEARCH_OPT_ERROR   =(auto(), "Error of searching optimum")
    IDLE_SEARCH_OPT_PAUSE   =(auto(), "Deciding about presenting recent")
    BUSY_RECENT_OPT_PRESENT =(auto(), "Prepare recent for presenting")
    IDLE_RECENT_OPT_ERROR   =(auto(), "Error of prepare recent")
    IDLE_RECENT_OPT_PRESENT =(auto(), "View of recent")
    IDLE_SEARCH_DONE        =(auto(), "Deciding about presenting last result")
    BUSY_RESULTS_PRESENT    =(auto(), "Prepare last result for presenting")
    IDLE_RESULTS_ERROR      =(auto(), "Error of prepare last result")
    IDLE_RESULTS_PRESENT    =(auto(), "View of last result")
    STOP                    =(auto(), "Stop Program")

    def __init__(self, *args) -> None:
        # self.nb: int = numb # trick: args[0] can be retrived as DgState.XXX.value[0]
        self.step: DimStep | None = None
        self.property: DimProp | None = None
        self.busy: DimBusy | None = None
        self.input_type: DimInpT | None = None
        self.influ_events: InfluEventSet | None = None
        self.transitions: List [DgTransition] = []
        self.description : str = args[1] # It can be retrived as DgState.XXX.value[1] also

    def set_prop(self, dim_step: DimStep, dim_property: DimProp,
                 dim_busy: DimBusy, dim_input_type: DimInpT) -> None:
        """
        This method fills the DgState member's attributes
        """
        self.step = dim_step
        self.property = dim_property
        self.busy = dim_busy
        self.input_type = dim_input_type

    def roll_up_influ_events(self) -> None:
        """
        This method fills the DgState member's influ_events attribute
        """
        if self.transitions:
            event_set: InfluEventSet = InfluEventSet(
                                      by_forms=   self.transitions[0].influence.by_forms,
                                      by_process= self.transitions[0].influence.by_process,
                                      by_buttons= self.transitions[0].influence.by_buttons
            )    # make a copy!
            for tr in self.transitions[1:]:
                event_set.dg_merge(tr.influence)
            self.influ_events = event_set

    def add_transition(self, transition) -> None:
        """
        This method adds (appends) a transition (DgTransition) into the
        list of transitions start from self state (self DgState).
        """
        loc_trans: DgTransition = transition
        self.transitions.append(loc_trans)

    @classmethod
    def states_by_prop(cls, prop: Union[Enum, int, str]) -> List:
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
            ret_val = [dg_state for dg_state in cls if dg_state.value[0] == prop]
        if isinstance(prop, str):
            ret_val = [dg_state for dg_state in cls if prop.lower() in dg_state.description.lower()]
        return ret_val

# -----------------------------------------------------------------------------------
# I. Clarification of state descriptions using the introduced descriptive dimensions:
# -----------------------------------------------------------------------------------
def clarification_of_states() -> None:
    """
    Clarification of state descriptions using the introduced descriptive dimensions
    """
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

class DgTransition:
    """
    This class determines the resulting state caused by an 'influ event'.
    """
    def __init__(self,
                 influence: InfluEventSet,
                 new_state: DgState,
                 new_alter_state: DgState | None = None):
        self.influence: InfluEventSet = influence
        self.new_state : DgState = new_state # for cases based on Random generated input
                                             # and/or for processes going "slow"
        # Here is an alternative for cases based on Text input when it's necessary
        self.new_alter_state : DgState | None = new_alter_state # and/or for processes going "quick"
                                                                # See loc_new_st_alt var. name also.
    def __repr__(self) -> str:
        return repr(self.influence) + self.new_state.name

    def put_accross(self, influ_event: InfluEventSet) -> None:
        """
        This method put across the transition itself in FSM.
        """
        # gui_control_dict["prev_state"] = None
        gui_control_dict["last_influ_event"] = influ_event
        gui_control_dict["last_put_accross"] = self.influence
        # gui_control_dict["rec_state"] = DgState.INIT
        # gui_control_dict["rec_inp_type"] = DimInpT.TYPE_NONE
        # gui_control_dict["quick_flow"] = False
        # gui_control_dict["success"] = False
        # # loc_prev_state: DgState = gui_control_dict["prev_state"]
        loc_rec_state: DgState = gui_control_dict["rec_state"]
        loc_rec_inp_type: DimInpT = gui_control_dict["rec_inp_type"]
        loc_quick_flow: bool = gui_control_dict["quick_flow"]
        loc_success: bool = gui_control_dict["success"]
        loc_new_state: DgState = self.new_state
        loc_new_alter_state: DgState | None = self.new_alter_state

        # # Can the input type be determined?     This part of code can be simplified. See below!
        # if ( loc_rec_state in [DgState.BUSY_RAND_GEN_INPUT, DgState.BUSY_INP_TEXT_READ] and
        #     loc_new_state == DgState.IDLE_HAVE_TECHN_INPUT ):
        #     loc_rec_inp_type = loc_rec_state.input_type # This is the same of ...
        #     # ... (DimInpT.TEXT_INPUT if loc_rec_state == DgState.BUSY_INP_TEXT_READ
        #     #                         else DimInpT.RANDOM_GEN)
        # # Lost knowledge of the input type?
        # if loc_new_state in [DgState.IDLE_INIT,
        #                      DgState.IDLE_RAND_GEN_SATISFIED,
        #                      DgState.IDLE_INP_TEXT_SATISFIED]:
        #     loc_rec_inp_type = DimInpT.TYPE_NONE

        # # Starting states: IDLE_HAVE_TECHN_INPUT and eight others
        # # loc_new_state = DgState.IDLE_RAND_GEN_SATISFIED    # < new_state
        # # loc_new_st_alt = DgState.IDLE_INP_TEXT_SATISFIED   # < new_alter_state
        # Intersection according to input type:
        # Trick: the two If statments below are active in different phases!
        if ( loc_new_state == DgState.IDLE_RAND_GEN_SATISFIED and
             loc_new_alter_state == DgState.IDLE_INP_TEXT_SATISFIED ):
            loc_new_state = ( loc_new_alter_state
                              if loc_rec_inp_type == DimInpT.TEXT_INPUT
                              else loc_new_state )
            loc_new_alter_state = None
        # Redefining the input type:
        if loc_new_state.input_type in [DimInpT.TYPE_NONE, DimInpT.TEXT_INPUT, DimInpT.RANDOM_GEN]:
            loc_rec_inp_type = loc_new_state.input_type

        # # Starting state: BUSY_TECHN_INP_PRESENT
        # # loc_new_state = DgState.IDLE_TECHN_INP_PRESENT   # < new_state
        # # loc_new_st_alt = DgState.IDLE_HAVE_LOWER_BOUND   # < new_alter_state
        # quick flow flag management I.
        # Trick: the two If statments below are active in different phases!
        if (loc_rec_state == DgState.IDLE_HAVE_TECHN_INPUT and
            self.influence.by_buttons[MyButton.ACTION.value] and # 1 //["","Investigate","Continue"]
            self.influence.by_buttons[MyButton.NEXT.value]): # 2
            loc_quick_flow = bool(influ_event.by_buttons[MyButton.NEXT.value]) # 2
        # Intersection according to "quick_flow" flag I.:
        if ( loc_new_state == DgState.IDLE_TECHN_INP_PRESENT and
             loc_new_alter_state == DgState.IDLE_HAVE_LOWER_BOUND ):
            if loc_quick_flow:
                loc_new_state = loc_new_alter_state
                loc_quick_flow = False
            loc_new_alter_state = None

        # success (and/or done) flag management
        #      BUSY_FIRST_ORDER_CREATE:  "FirstOrd Success"
        #      BUSY_SEARCH_OPTIM_EXEC  // IDLE_SEARCH_OPT_PAUSE:    "SearchOpt Success"
        if ( influ_event.by_process and
             influ_event.by_process[0] in ["FirstOrd Success", "SearchOpt Success"]):
            loc_success = True

        # # Starting state: BUSY_FIRST_ORDER_CREATE
        # # alternate pair I.:
        # # loc_new_state = DgState.IDLE_FIRST_ORD_PRESENT   # < new_state
        # # loc_new_st_alt = DgState.IDLE_HAVE_ROOT_INPUT    # < new_alter_state
        # # alternate pair II.:
        # # loc_new_state = DgState.IDLE_FIRST_ORD_PRESENT   # < new_state
        # # loc_new_st_alt = DgState.IDLE_SEARCH_DONE        # < new_alter_state
        # quick flow flag management II.
        # Trick: the two If statments below are active in different phases!
        if (loc_rec_state == DgState.IDLE_HAVE_LOWER_BOUND and
            self.influence.by_buttons[MyButton.ACTION.value] and # 1 //["","Investigate","Continue"]
            self.influence.by_buttons[MyButton.NEXT.value]): # 2
            loc_quick_flow = bool(influ_event.by_buttons[MyButton.NEXT.value]) # 2
        # Intersection according to "quick_flow" flag II.:
        if ( ( loc_new_state == DgState.IDLE_FIRST_ORD_PRESENT and
               loc_new_alter_state == DgState.IDLE_HAVE_ROOT_INPUT ) or
             ( loc_new_state == DgState.IDLE_FIRST_ORD_PRESENT and
               loc_new_alter_state == DgState.IDLE_SEARCH_DONE) ):
            if loc_quick_flow:
                loc_new_state = loc_new_alter_state
                loc_quick_flow = False #  Intentionally not left out!
            loc_new_alter_state = None

        # # Starting state: IDLE_FIRST_ORD_PRESENT
        # # alternate pair:
        # # loc_new_state = DgState.IDLE_HAVE_ROOT_INPUT  # < new_state
        # # loc_new_st_alt = DgState.IDLE_SEARCH_DONE     # < new_alter_state
        # Intersection according to "success" flag:
        if ( loc_new_state == DgState.IDLE_HAVE_ROOT_INPUT and
             loc_new_alter_state == DgState.IDLE_SEARCH_DONE ):
            loc_new_state = loc_new_alter_state if loc_success else loc_new_state
            loc_new_alter_state = None

        if loc_new_alter_state:
            raise RuntimeError("Alert put_accross! "
                              f"Not managed new_alter_state ({loc_new_alter_state})")

        # Redefining flags because step back:
        if loc_new_state in [DgState.IDLE_INIT,
                             DgState.IDLE_RAND_GEN_SATISFIED,
                             DgState.IDLE_INP_TEXT_SATISFIED]:
            loc_quick_flow = False
            loc_success = False

        gui_control_dict["prev_state"] = loc_rec_state
        gui_control_dict["rec_state"] = loc_new_state
        gui_control_dict["rec_inp_type"] = loc_rec_inp_type
        gui_control_dict["quick_flow"] = loc_quick_flow
        gui_control_dict["success"] = loc_success


# -----------------------------------------------------------------------
# II. Connecting transitions to their initial state in four installments:
#     connect_transitions_a(), connect_transitions_b(),
#     connect_transitions_c(), connect_transitions_d()
# -----------------------------------------------------------------------
def connect_transitions_a() -> None:
    """
    Connecting transitions to their initial state. Part a of a,b,c and d.
    """
    loc_influ: InfluEventSet | None = None
    loc_new_state : DgState | None = None
    #   1	INIT	The program started
    loc_influ = InfluEventSet(by_process="Start Eventloop")
    loc_new_state = DgState.IDLE_INIT
    DgState.INIT                    .add_transition( DgTransition(loc_influ, loc_new_state) )

    #  2	IDLE_INIT	Deciding type of input
    loc_influ = InfluEventSet(by_forms="Radio Random")
    loc_new_state = DgState.IDLE_RANDOM_GEN
    DgState.IDLE_INIT               .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_forms="Radio Text")
    loc_new_state = DgState.IDLE_INPUT_TEXT_DEF
    DgState.IDLE_INIT               .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_buttons=["","","Exit"]) # Back, Action, Next
    loc_new_state = DgState.STOP
    DgState.IDLE_INIT               .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_process="Close Win")
    loc_new_state = DgState.STOP
    DgState.IDLE_INIT               .add_transition( DgTransition(loc_influ, loc_new_state) )

    #   3 - 29
    loc_influ = InfluEventSet(by_process="Confirmed Close Win")
    loc_new_state = DgState.STOP
    loc_tran: DgTransition = DgTransition(loc_influ, loc_new_state)
    # Tuple of DgState elements to exclude
    loc_excl = (DgState.INIT, DgState.IDLE_INIT, DgState.STOP)
    for loc_dgst in DgState:
        if loc_dgst not in loc_excl:
            loc_dgst.add_transition(loc_tran)

    #   3	IDLE_RANDOM_GEN	Form for random generation
    loc_influ = InfluEventSet(by_buttons=["Cancel","",""]) # Back, Action, Next
    loc_new_state = DgState.IDLE_INIT
    DgState.IDLE_RANDOM_GEN         .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_forms="Filled (R)")
    loc_new_state = DgState.IDLE_RAND_GEN_SATISFIED
    DgState.IDLE_RANDOM_GEN         .add_transition( DgTransition(loc_influ, loc_new_state) )

    #   4	IDLE_RAND_GEN_SATISFIED	Form for random gen. filled
    loc_influ = InfluEventSet(by_buttons=["Cancel","",""]) # Back, Action, Next
    loc_new_state = DgState.IDLE_INIT
    DgState.IDLE_RAND_GEN_SATISFIED .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_forms="Missing (R)")
    loc_new_state = DgState.IDLE_RANDOM_GEN
    DgState.IDLE_RAND_GEN_SATISFIED .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_buttons=["","","Generate"]) # Back, Action, Next
    loc_new_state = DgState.BUSY_RAND_GEN_INPUT
    DgState.IDLE_RAND_GEN_SATISFIED .add_transition( DgTransition(loc_influ, loc_new_state) )

    #   5	BUSY_RAND_GEN_INPUT	Random generation of input
    loc_influ = InfluEventSet(by_process="Gen Failed")
    loc_new_state = DgState.IDLE_RAND_GEN_ERROR
    DgState.BUSY_RAND_GEN_INPUT     .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_process="Gen Done")
    loc_new_state = DgState.IDLE_HAVE_TECHN_INPUT
    DgState.BUSY_RAND_GEN_INPUT     .add_transition( DgTransition(loc_influ, loc_new_state) )

    #   6	IDLE_RAND_GEN_ERROR	Error of Random generation
    loc_influ = InfluEventSet(by_buttons=["Cancel","",""]) # Back, Action, Next
    loc_new_state = DgState.IDLE_RAND_GEN_SATISFIED
    DgState.IDLE_RAND_GEN_ERROR     .add_transition( DgTransition(loc_influ, loc_new_state) )

def connect_transitions_b() -> None:
    """
    Connecting transitions to their initial state. Part b of a,b,c and d.
    """
    loc_influ: InfluEventSet| None = None
    loc_new_state : DgState| None = None
    #   7	IDLE_INPUT_TEXT_DEF	Form for input text file
    loc_influ = InfluEventSet(by_buttons=["Cancel","",""]) # Back, Action, Next
    loc_new_state = DgState.IDLE_INIT
    DgState.IDLE_INPUT_TEXT_DEF     .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_forms="Filled (T)")
    loc_new_state = DgState.IDLE_INP_TEXT_SATISFIED
    DgState.IDLE_INPUT_TEXT_DEF     .add_transition( DgTransition(loc_influ, loc_new_state) )

    #   8	IDLE_INP_TEXT_SATISFIED	Form for inp. text file filled
    loc_influ = InfluEventSet(by_buttons=["Cancel","",""]) # Back, Action, Next
    loc_new_state = DgState.IDLE_INIT
    DgState.IDLE_INP_TEXT_SATISFIED .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_forms="Missing (T)")
    loc_new_state = DgState.IDLE_INPUT_TEXT_DEF
    DgState.IDLE_INP_TEXT_SATISFIED .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_buttons=["","","Read"]) # Back, Action, Next
    loc_new_state = DgState.BUSY_INP_TEXT_READ
    DgState.IDLE_INP_TEXT_SATISFIED .add_transition( DgTransition(loc_influ, loc_new_state) )

    #   9	BUSY_INP_TEXT_READ	Read of input text
    loc_influ = InfluEventSet(by_process="Read Failed")
    loc_new_state = DgState.IDLE_INP_TEXT_ERROR
    DgState.BUSY_INP_TEXT_READ      .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_process="Read Done")
    loc_new_state = DgState.IDLE_HAVE_TECHN_INPUT
    DgState.BUSY_INP_TEXT_READ      .add_transition( DgTransition(loc_influ, loc_new_state) )

    #  10	IDLE_INP_TEXT_ERROR	Error of Reading input text
    loc_influ = InfluEventSet(by_buttons=["Cancel","",""]) # Back, Action, Next
    loc_new_state = DgState.IDLE_INP_TEXT_SATISFIED
    DgState.IDLE_INP_TEXT_ERROR     .add_transition( DgTransition(loc_influ, loc_new_state) )

def connect_transitions_c() -> None:
    """
    Connecting transitions to their initial state. Part c of a,b,c and d.
    """
    loc_influ: InfluEventSet | None = None
    loc_new_state : DgState | None = None
    loc_new_st_alt : DgState | None = None
    #   11, 13, 15, 17, 19, 21, 22, 24, 28
    loc_influ = InfluEventSet(by_buttons=["Cancel","",""]) # Back, Action, Next
    loc_new_state = DgState.IDLE_RAND_GEN_SATISFIED
    loc_new_st_alt = DgState.IDLE_INP_TEXT_SATISFIED
    # DgState.IDLE_HAVE_TECHN_INPUT   .add_transition( DgTransition(loc_influ,
    #                                                               loc_new_state,
    #                                                               loc_new_st_alt) )
    loc_tran = DgTransition(loc_influ, loc_new_state, loc_new_st_alt)
    loc_incl = (DgState.IDLE_HAVE_TECHN_INPUT,
                DgState.IDLE_TECHN_INP_ERROR,
                DgState.IDLE_HAVE_LOWER_BOUND,
                DgState.IDLE_FIRST_ORD_ERROR,
                DgState.IDLE_HAVE_ROOT_INPUT,
                DgState.IDLE_SEARCH_OPT_ERROR,
                DgState.IDLE_SEARCH_OPT_PAUSE,
                DgState.IDLE_RECENT_OPT_ERROR,
                DgState.IDLE_RESULTS_ERROR
    )
    for loc_dgst in loc_incl:
        loc_dgst.add_transition(loc_tran)

    #  11	IDLE_HAVE_TECHN_INPUT	Deciding about presenting preliminary analysis
    loc_influ = InfluEventSet(by_buttons=["","Investigate","Continue"]) # Back, Action, Next
    loc_new_state = DgState.BUSY_TECHN_INP_PRESENT
    DgState.IDLE_HAVE_TECHN_INPUT   .add_transition( DgTransition(loc_influ, loc_new_state) )

    # 12	BUSY_TECHN_INP_PRESENT 	Preliminary analysis for lower bound
    loc_influ = InfluEventSet(by_process="PreAnalys Failed")
    loc_new_state = DgState.IDLE_TECHN_INP_ERROR
    DgState.BUSY_TECHN_INP_PRESENT  .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_process="PreAnalys Done")
    loc_new_state = DgState.IDLE_TECHN_INP_PRESENT
    loc_new_st_alt = DgState.IDLE_HAVE_LOWER_BOUND
    DgState.BUSY_TECHN_INP_PRESENT  .add_transition( DgTransition(loc_influ,
                                                                loc_new_state,
                                                                loc_new_st_alt) )

    # 13	IDLE_TECHN_INP_ERROR	Error of preliminary analysis
    # It is ready yet. See the two cycles above preparing "Confirmed Close Win" and "Cancel".
    # DgState.IDLE_TECHN_INP_ERROR    .add_transition( DgTransition(loc_influ, loc_new_state) )

    # 14	IDLE_TECHN_INP_PRESENT	View of preliminary analysis
    # "Done Viewing" === "Looked at"
    loc_influ = InfluEventSet(by_buttons=["","","Done Viewing"]) # Back, Action, Next
    loc_new_state = DgState.IDLE_HAVE_LOWER_BOUND
    DgState.IDLE_TECHN_INP_PRESENT  .add_transition( DgTransition(loc_influ, loc_new_state) )

    # 15	IDLE_HAVE_LOWER_BOUND	Deciding about presenting first order
    loc_influ = InfluEventSet(by_buttons=["","Investigate","Continue"]) # Back, Action, Next
    loc_new_state = DgState.BUSY_FIRST_ORDER_CREATE
    DgState.IDLE_HAVE_LOWER_BOUND   .add_transition( DgTransition(loc_influ, loc_new_state) )

    # 16	BUSY_FIRST_ORDER_CREATE	Create first order
    loc_influ = InfluEventSet(by_process="FirstOrd Failed")
    loc_new_state = DgState.IDLE_FIRST_ORD_ERROR
    DgState.BUSY_FIRST_ORDER_CREATE .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_process="FirstOrd Done")
    loc_new_state = DgState.IDLE_FIRST_ORD_PRESENT
    loc_new_st_alt = DgState.IDLE_HAVE_ROOT_INPUT
    DgState.BUSY_FIRST_ORDER_CREATE .add_transition( DgTransition(loc_influ,
                                                                loc_new_state,
                                                                loc_new_st_alt) )
    loc_influ = InfluEventSet(by_process="FirstOrd Success")
    loc_new_state = DgState.IDLE_FIRST_ORD_PRESENT
    loc_new_st_alt = DgState.IDLE_SEARCH_DONE
    DgState.BUSY_FIRST_ORDER_CREATE .add_transition( DgTransition(loc_influ,
                                                                loc_new_state,
                                                                loc_new_st_alt) )

    # 17	IDLE_FIRST_ORD_ERROR	Error of first order
    # It is ready yet. See the two cycles above preparing "Confirmed Close Win" and "Cancel".
    # DgState.IDLE_FIRST_ORD_ERROR    .add_transition( DgTransition(loc_influ, loc_new_state) )

    # 18	IDLE_FIRST_ORD_PRESENT 	View of first order
    loc_influ = InfluEventSet(by_buttons=["","","Done Viewing"]) # Back, Action, Next
    loc_new_state = DgState.IDLE_HAVE_ROOT_INPUT
    loc_new_st_alt = DgState.IDLE_SEARCH_DONE
    DgState.IDLE_FIRST_ORD_PRESENT  .add_transition( DgTransition(loc_influ,
                                                                loc_new_state,
                                                                loc_new_st_alt) )

    # 19	IDLE_HAVE_ROOT_INPUT	Deciding about search flow (step by step or continuous)
    loc_influ = InfluEventSet(by_buttons=["","","Continue"]) # Back, Action, Next
    loc_new_state = DgState.BUSY_SEARCH_OPTIM_EXEC
    DgState.IDLE_HAVE_ROOT_INPUT    .add_transition( DgTransition(loc_influ, loc_new_state) )

def connect_transitions_d() -> None:
    """
    Connecting transitions to their initial state. Part d of a,b,c and d.
    """
    loc_influ: InfluEventSet | None = None
    loc_new_state : DgState | None = None
    # 20	BUSY_SEARCH_OPTIM_EXEC	Searching optimum
    loc_influ = InfluEventSet(by_process="SearchOpt Failed")
    loc_new_state = DgState.IDLE_SEARCH_OPT_ERROR
    DgState.BUSY_SEARCH_OPTIM_EXEC  .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_process="SearchOpt Done")
    # loc_new_state = DgState.IDLE_SEARCH_DONE
    # DgState.B U SY_SEARCH_OPTIM_EXEC  .a d d_transition( DgTransition(loc_influ, loc_new_state) )
    # loc_influ = InfluEventSet(by_buttons=["","PAUSE",""]) # Back, Action, Next
    # loc_new_state = DgState.IDLE_SEARCH_OPT_PAUSE
    # DgState.B U SY_SEARCH_OPTIM_EXEC  .a d d_transition( DgTransition(loc_influ, loc_new_state) )
    loc_new_state = DgState.IDLE_SEARCH_OPT_PAUSE
    DgState.BUSY_SEARCH_OPTIM_EXEC  .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_process="SearchOpt Success")
    loc_new_state = DgState.IDLE_SEARCH_DONE
    DgState.BUSY_SEARCH_OPTIM_EXEC  .add_transition( DgTransition(loc_influ, loc_new_state) )
    # Trick: This event will not appear in event stack. It is only for redraw PAUSE button text.
    loc_influ = InfluEventSet(by_buttons=["","PAUSE",""]) # Back, Action, Next
    loc_new_state = DgState.IDLE_SEARCH_OPT_PAUSE   # See post_event() (in MyEventStack class)
    DgState.BUSY_SEARCH_OPTIM_EXEC  .add_transition( DgTransition(loc_influ, loc_new_state) )

    # 21	IDLE_SEARCH_OPT_ERROR	Error of searching optimum
    # It is ready yet. See the two cycles above preparing "Confirmed Close Win" and "Cancel".
    #DgState.IDLE_SEARCH_OPT_ERROR   .add_transition( DgTransition(loc_influ, loc_new_state) )

    # 22	IDLE_SEARCH_OPT_PAUSE	Deciding about presenting recent
    loc_influ = InfluEventSet(by_buttons=["","","Continue"]) # Back, Action, Next
    loc_new_state = DgState.BUSY_SEARCH_OPTIM_EXEC
    DgState.IDLE_SEARCH_OPT_PAUSE   .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_buttons=["","Investigate",""]) # Back, Action, Next
    loc_new_state = DgState.BUSY_RECENT_OPT_PRESENT
    DgState.IDLE_SEARCH_OPT_PAUSE   .add_transition( DgTransition(loc_influ, loc_new_state) )
    # loc_influ = InfluEventSet(by_process="SearchOpt Done")
    # loc_new_state = DgState.IDLE_SEARCH_DONE
    # DgState.IDLE_SEARCH_OPT_PAUSE   .add_transition( DgTransition(loc_influ, loc_new_state) )

    # 23	BUSY_RECENT_OPT_PRESENT	Prepare recent for presenting
    loc_influ = InfluEventSet(by_process="ResentPres Failed")
    loc_new_state = DgState.IDLE_RECENT_OPT_ERROR
    DgState.BUSY_RECENT_OPT_PRESENT .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_process="ResentPres Done")
    loc_new_state = DgState.IDLE_RECENT_OPT_PRESENT
    DgState.BUSY_RECENT_OPT_PRESENT .add_transition( DgTransition(loc_influ, loc_new_state) )

    # 24	IDLE_RECENT_OPT_ERROR	Error of prepare recent
    # It is ready yet. See the two cycles above preparing "Confirmed Close Win" and "Cancel".
    # DgState.IDLE_RECENT_OPT_ERROR   .add_transition( DgTransition(loc_influ, loc_new_state) )

    # 25	IDLE_RECENT_OPT_PRESENT	View of recent
    loc_influ = InfluEventSet(by_buttons=["","","Done Viewing"]) # Back, Action, Next
    # loc_new_state = DgState.IDLE_SEARCH_OPT_PAUSE
    loc_new_state = DgState.BUSY_SEARCH_OPTIM_EXEC
    DgState.IDLE_RECENT_OPT_PRESENT .add_transition( DgTransition(loc_influ, loc_new_state) )

    # 26	IDLE_SEARCH_DONE	Deciding about presenting last result
    loc_influ = InfluEventSet(by_buttons=["","","Done"]) # Back, Action, Next
    loc_new_state = DgState.IDLE_INIT
    DgState.IDLE_SEARCH_DONE        .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_buttons=["","Investigate",""]) # Back, Action, Next
    loc_new_state = DgState.BUSY_RESULTS_PRESENT
    DgState.IDLE_SEARCH_DONE        .add_transition( DgTransition(loc_influ, loc_new_state) )

    # 27	BUSY_RESULTS_PRESENT	Prepare last result for presenting
    loc_influ = InfluEventSet(by_process="PresentLast Failed")
    loc_new_state = DgState.IDLE_RESULTS_ERROR
    DgState.BUSY_RESULTS_PRESENT    .add_transition( DgTransition(loc_influ, loc_new_state) )
    loc_influ = InfluEventSet(by_process="PresentLast Done")
    loc_new_state = DgState.IDLE_RESULTS_PRESENT
    DgState.BUSY_RESULTS_PRESENT    .add_transition( DgTransition(loc_influ, loc_new_state) )

    # 28	IDLE_RESULTS_ERROR	Error of prepare last result
    # It is ready yet. See the two cycles above preparing "Confirmed Close Win" and "Cancel".
    # DgState.IDLE_RESULTS_ERROR      .add_transition( DgTransition(loc_influ, loc_new_state) )

    # 29	IDLE_RESULTS_PRESENT	View of last result
    loc_influ = InfluEventSet(by_buttons=["","","Done Viewing"]) # Back, Action, Next
    loc_new_state = DgState.IDLE_SEARCH_DONE
    DgState.IDLE_RESULTS_PRESENT    .add_transition( DgTransition(loc_influ, loc_new_state) )

    # 30	STOP	Stop Program
    # It does not have transitions.
    # DgState.STOP                    .add_transition( DgTransition(loc_influ, loc_new_state) )

# -----------------------------------------------------------------------------------------
# III. Roll up influence events (set DgState.influ_events by DgState.roll_up_influ_events() method)
# -----------------------------------------------------------------------------------------
def roll_up_influence_events() -> None:
    """
    Roll up influence events (set DgState.influ_events by DgState.roll_up_influ_events() method)
    """
    for st in DgState:
        st.roll_up_influ_events()

class GuiControlInfo(TypedDict):
    """
    Typing gui_control_dict
    """
    prev_state: DgState | None
    last_influ_event: InfluEventSet | None
    last_put_accross: InfluEventSet | None
    rec_state: DgState
    rec_inp_type : DimInpT
    quick_flow: bool
    success: bool

# gui_control_dict: dict[str, None | DgState | InfluEventSet | DimInpT | bool] = {
gui_control_dict: GuiControlInfo = {
    "prev_state" : None,
    "last_influ_event" : None,
    "last_put_accross" : None,
    "rec_state": DgState.INIT,
    "rec_inp_type" : DimInpT.TYPE_NONE,
    "quick_flow" : False,
    "success" : False
}
"""
This global variable includes some important main gui control property:  
    "prev_state"       - previous DgState,  
    "last_influ_event" - last origin event for putting accross,  
    "last_put_accross" - last event put accross,  
    "rec_state"        - recent DgState,  
    "rec_inp_type"     - recent DimInpT,  
    "quick_flow"       - flag for quick run,  
    "success"          - flag for reaching optimum
"""

def init_fsm() -> None:
    """
    This function completes the DgState Enum objects.
    It must be run only a time to avoid configuration conflicts!
    """
    clarification_of_states()

    connect_transitions_a()
    connect_transitions_b()
    connect_transitions_c()
    connect_transitions_d()

    roll_up_influence_events()

def init_gui_control(not_origin_init: bool = False) -> None:
    """
    This function initializes the gui_control_dict
    """
    gui_control_dict["prev_state"] = None
    gui_control_dict["last_influ_event"] = None
    gui_control_dict["last_put_accross"] = None
    gui_control_dict["rec_state"] = DgState.INIT
    gui_control_dict["rec_inp_type"] = DimInpT.TYPE_NONE
    gui_control_dict["quick_flow"] = False
    gui_control_dict["success"] = False
    if not_origin_init:
        gui_control_dict["prev_state"] = DgState.INIT
        gui_control_dict["last_influ_event"] = InfluEventSet(by_process="Start Eventloop")
        gui_control_dict["last_put_accross"] = DgState.INIT.transitions[0].influence # TRICK: ...
        # ... the value in the line above itself is a InfluEventSet(by_process="Start Eventloop")
        gui_control_dict["rec_state"] = DgState.IDLE_INIT

def state_change_due_to_event(influ_event: InfluEventSet) -> None:
    """
    This function put accross an event in FSM.
    """
    loc_rec_state: DgState = gui_control_dict["rec_state"]
    print(influ_event)
    loc_tr: DgTransition | None = None
    for trans in loc_rec_state.transitions:
        if trans.influence.is_watching_all(event_set= influ_event):
            if not loc_tr:
                loc_tr = trans
            else:
                raise RuntimeError("Alert state_change_due_to_event! "
                                   "The transition cannot be clearly defined by is_watching_all()")
    if not loc_tr:
        # if not gui_control_dict["last_influ_event"].is_watching_all(influ_event):
        if gui_control_dict["prev_state"]:
            for trans in gui_control_dict["prev_state"].transitions:
                if trans.influence.is_watching(event_set= influ_event):
                    loc_tr = trans
                    break
        if not loc_tr:
            raise RuntimeError("Alert state_change_due_to_event! "
                               "The transition cannot be found.\n"
                              f"Recent GUI state: {loc_rec_state}, "
                              f"influence event: {influ_event}."
            )
        return
    loc_tr.put_accross(influ_event= influ_event)
    print(gui_control_dict["rec_state"])

init_fsm() # It must be run only a time to avoid configuration conflicts!
init_gui_control() # It must be run this form next time:  init_gui_control(True)  , if necessary.

 # # # Example usage:
if __name__ == '__main__':
    print(DgState.INIT.value)
    print(DgState.INIT.value[0])
    print(DgState.INIT.value[1])
    print(DgState.INIT.transitions[0].influence)
    #print(DgState.INIT.nb)

    for loc_st in DgState:
        # print(loc_st.name, loc_st.description)
        print(loc_st.value[0], loc_st.name, loc_st.influ_events)

    print(" * " * 33)
    print(gui_control_dict["rec_state"])
    state_change_due_to_event(influ_event= InfluEventSet(by_process="Start Eventloop"))
    print(gui_control_dict["rec_state"])    # DgState.IDLE_INIT
    # state_change_due_to_event(influ_event= InfluEventSet(by_process="Close Win"))
    # print(gui_control_dict["rec_state"])  # DgState.STOP
    # state_change_due_to_event(influ_event= InfluEventSet(by_buttons=["","","Exit"]))
    # print(gui_control_dict["rec_state"])  # DgState.STOP
    print(" * " * 33)
    state_change_due_to_event(influ_event= InfluEventSet(by_forms="Radio Random"))
    print(gui_control_dict["rec_state"])    # DgState.IDLE_RANDOM_GEN
    state_change_due_to_event(influ_event= InfluEventSet(by_forms="Filled (R)"))
    print(gui_control_dict["rec_state"])    # DgState.IDLE_RAND_GEN_SATISFIED
    # state_change_due_to_event(influ_event= InfluEventSet(by_forms="Missing (R)"))
    # print(gui_control_dict["rec_state"])    # DgState.IDLE_RANDOM_GEN
    # state_change_due_to_event(influ_event= InfluEventSet(by_process="Confirmed Close Win"))
    # print(gui_control_dict["rec_state"])    # DgState.STOP
    # state_change_due_to_event(influ_event= InfluEventSet(by_buttons=["Cancel","",""]))
    # print(gui_control_dict["rec_state"])    # DgState.INIT
    print(" * " * 33)
    state_change_due_to_event(influ_event= InfluEventSet(by_buttons=["","","Generate"]))
    print(gui_control_dict["rec_state"])    # DgState.BUSY_RAND_GEN_INPUT
    # state_change_due_to_event(influ_event= InfluEventSet(by_process="Gen Failed"))
    # print(gui_control_dict["rec_state"])    # DgState.IDLE_RAND_GEN_ERROR
    # state_change_due_to_event(influ_event= InfluEventSet(by_buttons=["Cancel","",""]))
    # print(gui_control_dict["rec_state"])    # DgState.IDLE_RAND_GEN_SATISFIED
    print(" * " * 33)
    state_change_due_to_event(influ_event= InfluEventSet(by_process="Gen Done"))
    print(gui_control_dict["rec_state"])    # DgState.IDLE_HAVE_TECHN_INPUT
