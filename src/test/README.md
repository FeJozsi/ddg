
# `src\test` folder

Start date: 2024-02-26
The `src\test` directory houses the test (unittest) components of the project.

## 2024-04-05 11:31:10 Added dg_signals_graph.py to visualize the usage of the pyqtSignal() mechanism

- Added `dg_signals_graph.py` to visualize the usage of the pyqtSignal() mechanism.
The results are created in this folder, but the latest ones are placed in the doc folder
for documentation purposes.
- Introduced a new signal (message_on_gui) to update the GUI from an asynchronous thread.

You will probably try this command if you have the required Python tools and the Graphviz installed:

- `python src\test\dg_signals_map.py`

## 2024-04-04 14:56:02 Added dg_modules_map.py for module relationship visualization

Added `dg_modules_map.py` for visualizing import relationships between modules.
The results are created in this folder, but the latest ones are placed in the doc folder
for documentation purposes.

You will probably try this command if you have the required Python tools and the Graphviz installed:

- `python src\test\dg_modules_map.py`

## 2024-04-03 13:50:05 Continue development with enhanced input handling

- Implemented the use of new custom exceptions for input management.
- Implemented the DgInpSource class's new serve_line_if_any method.

For more details, see src/main/README.md.

## 2024-03-27 11:40:34 Refactor: Resolve MyPy type checking issues across 19 Python files in src

This folder is also affected by the scan. See the ReadMe.md file in the root folder for more details.

## 2024-02-26 11:59:20

Currently, it exclusively serves the test_dg_input_read module,
which tests the src\main\dg_standard_input module.  
The information describing a Directed Disjunctive Graph must be
a real object of a subclass of DgInpSource abstract base class (ABC).  
The instances of test_dg_input_read.DgInpSource class meet
the requirements of the DgInpSource abstract base class defined in the
src\main\dg_standard_input module.  

You will probably try these commands if you have the required Python tools installed:

- `pylint src\test\test_dg_input_read.py src\main\dg_standard_input.py`
- `python src\test\test_dg_input_read.py inputs\dg_gen_input_38m_11g_20240223121500.txt`

You can execute a command like the second to run the test_dg_input_read module for a test.  
Note: Ensure that your PYTHONPATH contains src/main.  
(You can check this using $env:PYTHONPATH in a PowerShell Terminal.  
You can set it using $env:PYTHONPATH = "src/main;src/test" if it was empty.)  
You also may consider to apply the .vscode\settings.json file with the new sets below for VSC:

    { ...
        "python.autoComplete.extraPaths": [
            "src/main"
        ],
        "python.analysis.extraPaths": [
            "src/main"
        ]
    ... }

The `test_dg_input_read` module reads input data describing a Directed Disjunctive Graph
from a text file and prints it to the standard output (Terminal or Command window).
See the comments of the module also.
