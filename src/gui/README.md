
# `gui` folder

Start date: 2024-03-01  
This folder contains the project's **GUI modules**.

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
