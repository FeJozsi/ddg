
# `src\generate_input` folder

Start date: 2024-02-23
Generate text files describe random produced Directed Disjunctive Graphs

## 2024-03-27 11:40:34 Refactor: Resolve MyPy type checking issues across 19 Python files in src

This folder is also affected by the scan. See the ReadMe.md file in the root folder for more details.

## 2024-02-23 12:37:11

The `src\generate_input\generate_random_dg_problem` module can generate
text files within the `inputs` folder located at the same level as the src folder.  
These text files describe random produced Directed Disjunctive Graphs suitable
to serve as input, respectively input template for the main functionality of the project.

The `src\generate_input\generate_random_dg_problem` file is entirely written
in Python and does not have any SIMULA'67 background or template,
meaning it is entirely new. The code itself includes numerous docstring comments.

So, please try boldly these commands if you have the required Python tools installed:

- `pylint src/generate_input/generate_random_dg_problem.py`

- `python.exe src/generate_input/generate_random_dg_problem.py 38 11`

The messages go to the Terminal/Command window.  
The output text files describing random produced Directed Disjunctive Graphs
problem go to the `inputs` folder.
