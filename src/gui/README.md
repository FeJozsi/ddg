
# `gui` folder

Start date: 2024-03-01  
This folder contains the project's **GUI modules**.

## 2024-03-22 11:38:24 enhance: Improve UI feedback and async stability, refine FSM event handling

- Added debounce timer for text input form's textChanged signal to optimize user input handling.
- Replaced Button2 with a checkbox for user-controlled "Step by step process" toggling.
- Enhanced MainWindow's paintEvent to ensure correct termination of the painting session,
improving background image management.
- Upgraded exception handling for async daemons (process_event_stack and carry_out_processes),
securing the application's quit process.
- Extended carry_out_processes daemon functionality to emit redraw_my_app_window_on_state signal,
facilitating state-aware UI updates.
- Refined FSM's state_change_due_to_event method for increased resilience against redundant
high-level events, enhancing system robustness.

Ongoing development and enhancements continue to integrate and stabilize application functionality.

You will probably try this command if you have the required Python tool installed:

- `python src\gui\dg_gui_main.py`

## 2024-03-21 20:07:28 feat(gui): Integrate GUI modules and enhance functionality

- Integrated GUI's ready modules: gui-main, FSM, task manager.
- Separated MainWindow (dg_gui_window) and window update functionalities (dg_gui_draw_on_state)
into a distinct module from gui-main (dg_gui_main).
- Introduced a new QCheckBox variant (dg_gui_read_only_able_checkbox) with read-only capability.
- Implemented a high-level event stack module for enhanced event management.
- Integrated pyqtSignals for safe application quit and window updates based on FSM state transitions.
- Expanded the FSM to handle 30 states, with 4 initial states now operational.
- Timestamped high-level events for better tracking.
- Added asynchronous event stack processing (async def process_event_stack) in gui-main module.
- Implemented on_about_to_quit event handling in gui-main module.

You will probably try these commands if you have the required Python tools installed:

- `python src\gui\dg_gui_main.py`
- `pylint src\gui\dg_gui_draw_on_state.py`
- `pylint src\gui\dg_gui_own_event_stack.py`
- `pylint src\gui\dg_gui_read_only_able_checkbox.py`
- `pylint src\gui\dg_gui_window.py`

## 2024-03-13 12:41:48 Refine UI elements and interactions in dg_gui_main.py

This update to the `src/gui/dg_gui_main.py` module brings focused improvements
to enhance functionality:

- Enhanced Transparency: Adjusted transparency levels on certain controls, further improving
the visual hierarchy and user focus on essential interactions.
- Dialog Differentiation: Fine-tuned the behavior and appearance of open and save file dialogs,
tailoring them to their specific use cases.
- Radio Buttons Engagement: Involved the existing radio buttons more prominently in the demonstration
of the GUI's capabilities, highlighting their role in user choices and interface dynamics.

We have reached the threshold of the integration of the elements that form the basis
of the GUI completed so far.
This milestone underscores our commitment to developing a coherent and user-friendly interface,
laying a solid foundation for future enhancements and features.

A new screenshot, `dg_gui_Screenshot_20240313.PNG`, has been added to the `doc` folder,
providing a current view of the GUI's appearance for reference and documentation purposes.

## 2024-03-12 23:49:52 feat(gui): Add resizable GUI module view with paged components and ChatGPT-inspired background

Implemented a new module `src/gui/dg_gui_main.py` that centralizes all GUI components
and control details for enhanced maintainability. The main features include:

- Resizability: Ensures the GUI dynamically adapts to different window sizes,
improving user experience.
- Paged Navigation: Utilizes QStackedWidget to facilitate "paging" through
different parts of the application, offering a streamlined navigation experience.
- Transparent Controls: Introduces a background image visible through the controls,
adding to the aesthetic appeal of the interface.

You will probably try these commands if you have the required Python tools installed:

- `pylint src\gui\dg_gui_main.py`
- `python src\gui\dg_gui_main.py`

## Enhance GUI aesthetics in PyQt6 design by adding background image and refining fonts

- Added a background image to `src/gui/gui_pyqt6_my_design.py` to improve the visual
appeal of the preview GUI design.
- Refined font styles for better readability and consistency with the new background.

## feat(gui): Launch async `dg_task_manager` with dynamic simulation & auto-switch

- Initiated src\gui\dg_task_manager.py, creating an async framework tailored
for managing the application's main flow operations, aligning with the Model concept.
- Implemented self-contained testing capability, enabling the module to independently
simulate main operation calls. The async architecture ensures seamless operation
and testing flexibility.
- Enhanced the simulation with automatic switching functionality, designed to transition
to real main tasks upon their assumed completion, simulating a real operational environment.
- Integrated randomized imitate behavior for task outcomes, allowing simulated tasks
to result in either "Done" or "Failed" states, thereby introducing variability
and realism into the testing process.
- Directly builds upon and complements the src\gui\dg_gui_finite_state_machine.py module
completed yesterday, with no updates needed for the finite state machine module today.

This set of enhancements not only establishes a robust framework for future development
but also significantly advances the simulation's fidelity and operational readiness.

You will probably try these commands if you have the required Python tools installed:

- `pylint src\gui\dg_task_manager.py`
- `python src\gui\dg_task_manager.py`

## 2024-03-08 19:48:44 FSM module (`dg_gui_finite_state_machine.py`) development completed

FSM module development completed: fully operational and independently testable by itself.  
Upcoming efforts will integrate it with the main application flow, with minor adjustments needed,
and will extensively update the GUI for full operational integration.

It is an important Update also on Typing Enhancements. Revising our
inaccurate approach to `dict` Typing.

You will probably try these commands if you have the required Python tools installed:

- `pylint src\gui\dg_gui_finite_state_machine.py`
- `python src\gui\dg_gui_finite_state_machine.py`

## 2024-03-07 20:35:55 Continued developing dg_gui_finite_state_machine.py (I.)

In this latest update, we've made significant advancements in the
`dg_gui_finite_state_machine.py`
module by implementing new state management functions.

A new DgTransition class has been established. The contents of
`doc\FSM states and transfers.ods` have been meticulously mapped,
ensuring a complete representation of all GUI state transitions in the system.

## 2024-03-05 15:15:38 Added dg_gui_finite_state_machine.py module

Added the dg_gui_finite_state_machine.py module as is now.
The implementation has to be continued.

## 2024-03-04 16:48:51 Added 'FSM states and transitions.ods' spreadsheet

Added the design document `doc\FSM states and transitions.ods` to outline the
proposed FSM (Finite State Machines) states and transitions for the GUI,
pending implementation.

## 2024-03-01 16:08:44 Initialize GUI with async task simulation and file open dialog

Set up basic GUI structure for future development.
Implemented asynchronous task simulation to test async functionality.
Added file open dialog box for file selection capabilities.

## 2024-03-01 11:24:02 Set up foundational GUI elements, starting point

By default, this folder contains the project's GUI modules.

The GUI is just getting started and isn't finished yet.
We're working on making it better and easier to use.
Right now, it's like a rough draft, not the final version.
