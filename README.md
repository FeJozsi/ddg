
# ddg

## Efforts to revive my old SIMULA'67 project dealing with disjunctive graphs, using Python now

Start date: 2024-02-21  
Owner: FeJozsi from Budapest, Hungary  
E-mail: <jfeher@fjm.hu>  

### Theoretical background

2024-02-21 13:59:52

**Directed disjunctive graphs** can be conceptualized as collections of operations and machines,
mirroring our intuitive understanding of these concepts.

- Each *operation* has a designated positive execution time and is assigned
to a specific machine for execution.  
- The workflow on *machines* is independent of the operations and their order,
but each machine can handle only one operation at a time.  
- In general, our task is *to determine the sequence* in which operations are executed
on the machines.

However, we must adhere to specific *technological dependencies* between
operations, which are established at the outset.  

It is evident that technological dependencies cannot form a *cycle* between operations,
as these relations dictate that one operation must precede the other in the sequence.

- Therefore, our objective is *to find an order of operations on all machines that
satisfies the requirements and minimizes the total execution time*.

Many years ago, when I obtained my Master's degree in Mathematics, this task
posed a significant challenge for the computers of that era. However, nowadays,
it can still be challenging depending on the specific circumstances.

- We rewrote the old SIMULA'67 code in Python.

The execution time improved significantly, among others, due to the
increased speed of computers by at least five orders of magnitude.
However, our task has remained extremely complex.

- I have developed a random *"directed disjunctive graph" task generator*
(which will be added first to the repository soon).

With this tool, for example, I managed to create a very resource-intensive
task consisting of one hundred operations and four machines – despite the fact
that we exclude the "hopeless" branches of the solution tree to be traversed
with sufficiently well-founded lower bound estimates.  
The thesis revolved around this topic.

- When we modify a few specific technological dependencies between tasks,
it can *greatly affect* the resources needed to find the optimum solution.

## About the Development Environment

I am developing this project on Windows 10, using Visual Studio Code as the IDE,
within a Python virtual environment.

### python --version

    Python 3.12.1

### pip list

I installed these packages manually in the virtual environment:

    pip install pip
    pip install pylint
    pip install typing_extensions
    pip install PyQt6
    pip install qasync

### The packages' versions in the virtual environment

    Package           Version
    ----------------- -------
    astroid           3.1.0
    colorama          0.4.6
    dill              0.3.8
    isort             5.13.2
    mccabe            0.7.0
    pip               24.0
    platformdirs      4.2.0
    pylint            3.1.0
    PyQt6             6.6.1
    PyQt6-Qt6         6.6.2
    PyQt6-sip         13.6.0
    qasync            0.27.1
    tomlkit           0.12.3
    typing_extensions 4.10.0

## Milestones of developing

Each linked folder contains its own ReadMe file.
Below are only the major "milestones", listed in descending order of recency.

### 2024-03-01 11:40:13 Set up foundational GUI elements, starting point

See the new `src\gui` folder.

### 2024-02-29 15:56:34 Added missing components to the `src\main` folder

Added missing components to the `src\main` folder of the project
in its current state.

- To solve Directed Disjunctive Graphs, you must initiate the `dg_main.py` module.  
See src\main\README.md for details.

### 2024-02-23 12:19:12 Added folders: `src\generate_input` and `inputs`

- The `src\generate_input\generate_random_dg_problem.py` module can generate
text files within the inputs folder, describing random Directed Disjunctive Graphs.  
These files are suitable to serve as input (respectively input template) for the main
functionality of the project.
