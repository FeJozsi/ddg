"""
This module serves as the entry point for the graphical user interface (GUI) version
of the project. It initializes the application's main window and starts the event loop,
effectively launching the GUI.

Key Components:
- The module utilizes the MainWindow class (defined within this project)
to set up the GUI environment, including creating the main window
"""

import sys
import asyncio
from typing import List
import traceback

from PyQt6.QtWidgets import QApplication

import qasync

# from typing_extensions import deprecated

# Ensure you import your MainWindow class correctly
from dg_gui_window import get_main_window_instance
# import dg_gui_window

from dg_gui_finite_state_machine import ( InfluEventSet, DgState, # DimInpT,
                                          state_change_due_to_event,
                                          gui_control_dict
                                         )
from dg_task_manager import carry_out_process

from dg_gui_draw_on_state import redraw_my_app_window_on_state

# from dg_gui_draw_on_state import draw_form_stack_widget
# # The line above triggered:
# #  ImportError: cannot import name 'draw_form_stack_widget' from partially
# #               initialized module 'dg_gui_draw_on_state' (most likely due to
# #               a circular import)
# import dg_gui_draw_on_state     <<< was the temporary solution
# [[The reason was: dg_gui_draw_on_state.py contained: from d g _gui_main import M a inWindow]]
from dg_gui_own_event_stack import my_event_stack

original_stdout = sys.stdout  # Save a reference to the original standard output

# async def i n itialize_process(mw: M a inWindow):
def initialize_process():
    """
    Prepare for starting own high level event loop
    """
    print(gui_control_dict["rec_state"])    # DgState.INIT
    state_change_due_to_event(influ_event= InfluEventSet(by_process="Start Eventloop"))
    print(gui_control_dict["rec_state"])    # DgState.IDLE_INIT

    # loc_recent_state: DgState = gui_control_dict["rec_state"]
    # r e draw_my_app_window_on_state(main_window= mw, recent_state= loc_recent_state)
    my_event_stack.emit_redraw_my_app_window_on_state()

async def process_event_stack() -> None: # (mw: M a inWindow):
    """
    Continuously process the high-level event stack.
    This coroutine will check for a condition to exit at each iteration to allow graceful shutdown.
    """
    try:
        while True:
            # Your event processing logic here
            # Check if there are events in your high-level event-stack
            # Process them accordingly
            event: InfluEventSet = my_event_stack.get_next_prepared_event()
            if event is not None:
                state_change_due_to_event(influ_event= event)
                if gui_control_dict["rec_state"] == DgState.STOP:
                    break
                my_event_stack.emit_redraw_my_app_window_on_state()

            # Simulate async work with sleep
            await asyncio.sleep(0.1)  # Prevents hogging the CPU, adjust the sleep time as needed
        print("The process_event_stack() was broken.",
                file= sys.stderr)
    except Exception as e: # pylint: disable=W0718 # Catching too general
                           #  ... exception Exception (broad-exception-caught)
        gui_control_dict["rec_state"] = DgState.STOP
        print(f"The process_event_stack raised an exception: {e}",
                file= sys.stderr)
        traceback.print_exc(file=sys.stderr)

    my_event_stack.emit_my_application_quit()

async def carry_out_processes() -> None:
    """
    Carry out the processes depending on the current state
    """
    try:
        while True:
            if gui_control_dict["rec_state"] == DgState.STOP:
                break
            # Check if there is a task to execute
            if gui_control_dict["rec_state"].name.startswith("BUSY_"):
                await carry_out_process()
                await asyncio.sleep(0.00001) # Prevents hogging the CPU, adjust the time as needed
                my_event_stack.emit_redraw_my_app_window_on_state()
                continue
            # Simulate async work with sleep
            await asyncio.sleep(0.1)  # Prevents hogging the CPU, adjust the sleep time as needed
    except Exception as e: # pylint: disable=W0718 # Catching too general
                           #  ... exception Exception (broad-exception-caught)
        gui_control_dict["rec_state"] = DgState.STOP
        print(f"The carry_out_processes raised an exception: {e}",
                file= sys.stderr)
        traceback.print_exc(file=sys.stderr)

        my_event_stack.emit_my_application_quit()

def on_about_to_quit(tasks: List[asyncio.Task]):
    """
    Cancel all tasks.
    It is strange, but it will be run twice.
    """
    # Restore the original stdout
    sys.stdout = original_stdout

    for task in tasks:
        if task.done():
            if task.cancelled():
                print("The task was cancelled.")
            else:
                try:
                    result = task.result()
                    print("Task completed with result:", result)
                except Exception as e: # pylint: disable=W0718 # Catching too general
                                       #  ... exception Exception (broad-exception-caught)
                    print("The task raised an exception:", e)
            print("task.cancel() omitted")
        else:
            print("task.cancel() run")
            task.cancel()
    print("Tasks are being cancelled...")

# def my_exception_handler(_, context): # loop
#     # context["message"] will always be there; but context["exception"] may not
#     msg = context.get("exception", context["message"])
#     print(f"Caught an asyncio exception: {msg}", file= sys.stderr)

def dg_gui_main():
    """
    This function is the main runable one of the GUI controlled version of ddg project.
    """
    app = QApplication(sys.argv)
    # mainWindow = M a inWindow() // AsyncApp(max_char= 1300)
    # mainWindow.show()
    # sys.exit(app.exec())

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    # loc_loop = asyncio.get_event_loop()
    # loc_loop.set_exception_handler(my_exception_handler) It does not work.

    # main_window = MainWindow()
    # main_window = mw
    main_window = get_main_window_instance()

    main_window.set_redraw_my_app_window_on_state(redraw_my_app_window_on_state)

    main_window.show()

    # # await i n itialize_process(main_window)  "await" allowed only within async function
    # asyncio.run(i n itialize_process(main_window))
    # Schedule i n itialize_process without using asyncio.run():
    #   Since you're already in an async environment managed by qasync,
    #   directly scheduling your coroutine with the event loop might be more appropriate.
    #   asyncio.run() is generally used as the main entry point to run an async
    #   program and will create a new event loop, which is not what you want
    #   since qasync already sets up an event loop for you.
    initialize_process()
    tasks = [
        # asyncio.ensure_future() is used to schedule
        #    i n itialize_process() and process_event_stack()
        #    for execution in the asyncio event loop.
        #    This allows both your GUI and async tasks
        #    to run concurrently.
        # asyncio.ensure_future(i n itialize_process(main_window)),
        asyncio.ensure_future(process_event_stack()),
        asyncio.ensure_future(carry_out_processes())
    ]

    app.aboutToQuit.connect(lambda: on_about_to_quit(tasks))

    with loop:
        try:
            # (loop.)run_forever() is designed to keep the (loop) running
            #   until (loop.)stop() is explicitly called.
            loop.run_forever()  # This line triggers the aboutToQuit event when ...
        finally:                #   ... when the main window closed by the user
            loop.run_until_complete(    # It triggers the aboutToQuit also ...
                 loop.shutdown_asyncgens()
                                   )    #   ... as it seems at line below in Debug session.
            # loop.run_until_complete( tasks[0] )  # It triggers the aboutToQuit also
            loop.close()

    print("The post Application life begins")  # This will now run after the loop is closed.

if __name__ == "__main__":
    dg_gui_main()
    # asyncio.run(dg_gui_main())
