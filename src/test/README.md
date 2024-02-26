
# `src\test` folder

Start date: 2024-02-26

## 2024-02-26 11:59:20

The `src\test` directory houses the test (unittest) components of the project.

Currently, it exclusively serves the test_dg_input_read module,
which tests the src\main\dg_standard_input module.  
In this test, the information describing a Directed Disjunctive Graph is
an object of dg_standard_input.InputTextFile class. This object meets
the requirements of the DgInpSource abstract base class defined in the
src\main\dg_standard_input module.  

You will probably try these commands if you have the required Python tools installed:

- `pylint src\test\test_dg_input_read.py src\main\dg_standard_input.py`
- `python src\test\test_dg_input_read.py inputs\dg_gen_input_38m_11g_20240223121500.txt`

You can execute a command like the second to run the test_dg_input_read module for a test.  
Note: Ensure that your PYTHONPATH contains src/main.
You can check this using $env:PYTHONPATH in a PowerShell Terminal.

The `test_dg_input_read` module reads input data describing a Directed Disjunctive Graph
from a text file and prints it to the standard output (Terminal or Command window).
