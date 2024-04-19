
# `gui` folder

Start date: 2024-03-01  
This folder contains the project's **GUI modules**.

## 2024-04-19 09:31:49 New milestone: Completed developer testing for BusySearchOptimExec task

- GUI remains responsive throughout.
- Implemented pausability for long-running processes.
- Optimized QTextEditOutputStream to maintain text character count within normal bounds without
impacting search speed.
- Development continues on the remaining two core functionalities.

## 2024-04-17 15:29:06 Integrated the 5th core functionality

- Refactored the FSM (Finite State Machine) to simplify handling user-triggered
PAUSES between iterations of searching for the optimum.
- Integrated the 5th core functionality in the BusySearchOptimExec class for searching the optimum
in the DDG within the Task Factory. Strong developer tests will have to be carried out.
- Corrected various typos and addressed pylint issues.

Development continues with the two remaining core functionalities.

## 2024-04-16 20:58:23 Updated the application's background

Updated the application's background to a new, more relevant design.
Implemented aspect ratio preservation for the background image upon window resize.

## 2024-04-15 19:45:01 Integrated the 4th core function

Integrated the 4th core function, enabling the presentation of the initial established order of
DDG operations on the machines. Implemented by the Task Manager's BusyFirstOrderCreate class.

## 2024-04-12 19:59:28 Completed integration of the third core function

Completed integration of the third core function, enabling the presentation of data from the
input DDG descriptive file and the results of initial analyses. Provided by the Task Manager's
BusyTechnInpPresent class.

## 2024-04-11 20:26:52 Enhancements and Integrations in DDG Generation

- Completed integration of the second core function, enabling initiation of new DDG descriptive
file generation with filled-in properties from the application's GUI.
Provided by the Task Manager's BusyRandGenInput class.
- Significant changes occurred in the instantiation of the GrdgControl instance within
the src\generate_input\generate_random_dg_problem.py module.
A more parameterizable version has been derived from its original form.
- Implemented a confirmation overwrite message window to prevent unintentional accidental
overwrites when handling the 'Generate' button click event.
- User permission to continue is communicated through the newly introduced
initiate_generation_new_ddg pyqtSignal() emission, triggering appropriate high-level event
and entering the custom event stack for main process control.
- Refined the user input options on the form for text file generation. Users can now specify
either a folder or a full path with a file name, and can also browse for it specifically,
distinguishing between the two modes. If necessary, the program generates a unique output file name.

Development continues with further enhancements to core functionalities.

## 2024-04-09 16:44:37 Enhancements and Refactorings in GUI Module and Event Management

- Refactored module: dg_gui_read_only_able_checkbox.py renamed to dg_gui_prepare_window.py
- Began implementing handling for message_on_gui PyQT signal in src\gui\dg_gui_draw_on_state.py
- Improved robustness of high-level event management by utilizing MyEventStack.set_busy_start()
and MyEventStack.set_ready_dtn() methods
- Introduced new abstraction layer for Real Tasks in Task Manager to handle exceptions more effectively
- Enhanced exception handling for improved reliability
- Extended high-level event management to include core event processing
- Improved clarity and informativeness of input syntax checks
- Additionally, successfully resolved a challenging issue in the asyncio-PyQt environment
caused by the use of the exec() method, which impacted the event loop mechanism.

## 2024-04-09 15:02:56 refactor: dg_gui_read_only_able_checkbox.py renamed to dg_gui_prepare_window.py

The dg_gui_read_only_able_checkbox.py module has been renamed to dg_gui_prepare_window.py, because
it contains not only ReadOnlyAbleCheckBox(QCheckBox) but some other classes and function for
the Main GUI Window.

## 2024-04-05 23:39:47 The first real task of the Task Factory has been created

We reached a new milestone.  
`The first real task` of the Task Factory has been done (in the dg_task_manager module).  
This task (represented by `BusyInpTextRead(CommonRealTask)` class) reads the Directed Disjunctiv
Graph description input file and checks all requirements of data.
It sends messages to the GUI about the most important attributes of description data.  
Introduced also the `NewsType` enum (see in dg_gui_finite_state_machine module) to control
the handle of asynchronous GUI messages.

Development continues with the integration of core functionalities and GUI enhancements.

## 2024-04-05 11:31:10 Added dg_signals_graph.py to visualize the usage of the pyqtSignal() mechanism

- Added src\test\dg_signals_graph.py to visualize the usage of the pyqtSignal() mechanism.
The generated dot and PNG files have been placed in the doc folder.
- Introduced a new signal (`message_on_gui` signal) to update the GUI from an asynchronous thread.
- Refactored to utilize the `MyButton` enum, replacing direct usage of indices 0, 1, 2.

Development continues with the integration of core functionalities and GUI enhancements.

## 2024-04-04 14:56:02 Added dg_modules_map.py for module relationship visualization

Added src\test\dg_modules_map.py for visualizing import relationships between modules.
Placed dot and PNG outputs in the doc folder.
Removed sensitive references in comments to ensure relationship accuracy.

## 2024-03-27 11:40:34 Refactor: Resolve MyPy type checking issues across 19 Python files in src

This folder is also affected by the scan. See the ReadMe.md file in the root folder for more details.

## 2024-03-25 11:08:41 refactor: Streamline form structure and improve UI guidance

- Implemented consistent FSM status messages, enhancing clarity and reliability
in application state communication.
- Overhauled the form class hierarchy, including AbstractFormMixin, BaseForm, and their child classes
TextForm and GenForm, for improved unification and complexity management across the UI components.
- Introduced tooltips for form controls, significantly enhancing user interface guidance
and providing better context and usability to end-users.

These changes mark another step forward in our ongoing efforts to refine the application's
architecture and user experience, with continued focus on integration and stability enhancements.

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
- ~~pylint src\gui\dg_gui_read_only_able_checkbox.py~~
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
