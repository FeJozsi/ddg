
# `src\generate_input` folder

Start date: 2024-02-23

## 2024-02-23 12:37:11

The `src\generate_input\generate_random_dg_problem.py` module can generate
text files within the `inputs` folder located at the same level as the src folder.  
These text files describe random produced Directed Disjunctive Graphs suitable
to serve as input, respectively input template for the main functionality of the project.

The `src\generate_input\generate_random_dg_problem.py` file is entirely written
in Python and does not have any SIMULA'67 background or template,
meaning it is entirely new. The code itself includes numerous docstring comments.

So, please try boldly these commands if you have the required Python tools installed:

- `pylint src/generate_input/generate_random_dg_problem.py`

- `python.exe src/generate_input/generate_random_dg_problem.py 38 11`

The messages come to the Terminal/Command window.  
The output text files describing random produced Directed Disjunctive Graphs
problem come to the `inputs` folder.
