"""
This modul serves the application's own high level event stack

# Use shared_instance
    from dg_gui_own_event_stack import my_event_stack

    my_event_stack.post_event( influ_event # <InfluEventSet>)
                             ) 
"""
import sys
from datetime import datetime, timedelta
from collections import deque

from PyQt6.QtCore import pyqtSignal, QObject

from dg_gui_finite_state_machine import InfluEventSet

class MyEventStack(QObject):
    """
    This is a FIFO event stack for the application's own high level events
    The Close Win event is exceptionally handled as LIFO (Last In, First Out).
    """
    # Signals for GUI (listen-connect: dg_gui_window.py)
    redraw_my_app_window_on_state = pyqtSignal() # Signals must be a class attribute.
                                                 # This is connected with using QObject.
    my_application_quit = pyqtSignal()
    # Message add-ons data: unique code str, type str, control int, message text str:
    message_on_gui = pyqtSignal(str, str, int, str)

    def __init__(self) -> None:
        super().__init__() # It is very important. This is also connected with using QObject.
        self.start_dtn: datetime = datetime.now()
        self.ready_dtn: datetime | None = datetime.now() + timedelta(seconds=0.100)
        self.busy_start: datetime | None = None
        self.busy_td: timedelta = self.start_dtn - self.start_dtn
        self.my_stack: deque[InfluEventSet] = deque()
    def post_event(self, e: InfluEventSet) -> None:
        """
        Event Posting and Enqueuing
        """
        if (e.is_not_interested(InfluEventSet(by_process="Close Win")) and
            e.is_not_interested(InfluEventSet(by_process="Confirmed Close Win"))):
            if ((not bool(self.busy_start) and
                 bool(e.by_process)) or
                ((not self.ready_dtn or e.triggered_dtn < self.ready_dtn) and
                 not bool(e.by_process))):
                # sys.stderr.write("This is an error message.\n")
                print(f"The event ({e}) was dropped because of too early triggered time.",
                       file= sys.stderr)
                return
            if bool(self.my_stack):
                if self.my_stack[-1].is_watching_all(e): # Last element was the same
                    return
        if (e.is_watching(InfluEventSet(by_process="Close Win")) or
            e.is_watching(InfluEventSet(by_process="Confirmed Close Win"))):
            # self.my_stack.insert(0, e)
            self.my_stack.appendleft(e) # it is exceptionally handled as LIFO (Last In, First Out)
        else:
            self.my_stack.append(e) # for normal FIFO handling
    def set_busy_start(self) -> None:
        """
        This method begins (and sets) the busy state of the event managment.
        """
        if not bool(self.ready_dtn):
            print("The set_busy_start was refused because of busy state in progress.",
                  file= sys.stderr)
            return
        self.busy_start = datetime.now()
        self.ready_dtn = None
    def set_ready_dtn(self) -> None:
        """
        This method finishes the busy state of the event managment.
        """
        if self.busy_start:
            self.busy_td = self.busy_td + (datetime.now() - self.busy_start)
            self.busy_start = None
        self.ready_dtn = datetime.now() + timedelta(seconds=0.100)
    def get_next_prepared_event(self) ->  InfluEventSet | None:
        """
        This method serves the next event to handle and
        removes it from the deque.
        """
        if not bool(self.my_stack):
            return None
        # Remove and return the leftmost (first) element
        return self.my_stack.popleft()
    def emit_redraw_my_app_window_on_state(self) -> None:
        """
        Emit a signal to redraw
        """
        self.redraw_my_app_window_on_state.emit() # Emit a signal to redraw
    def emit_my_application_quit(self) -> None:
        """
        Emit a signal to quit the application
        """
        self.my_application_quit.emit() # Emit a signal to quit
    def emit_message_on_gui(self, m_code: str,
                                  m_type: str = "error_win",
                                  m_control: int = 0,
                                  m_text: str = "Unexpected runtime error") -> None:
        """
        Emit a signal to quit the application
        """
        self.message_on_gui.emit(m_code, m_type, m_control, m_text) # Emit a signal to message

# Create a module-level instance that will be shared
my_event_stack = MyEventStack()
