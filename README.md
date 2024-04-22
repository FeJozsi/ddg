
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
    pip install mypy
    pip install graphviz

### The packages' versions in the virtual environment

    Package           Version
    ----------------- -------
    astroid           3.1.0
    colorama          0.4.6
    dill              0.3.8
    graphviz          0.20.3
    isort             5.13.2
    mccabe            0.7.0
    mypy              1.9.0
    mypy-extensions   1.0.0
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

### 2024-04-22 19:14:23 Important milestone achieved: Final core function integration

Completed integration of the last core function; implemented in the class BusyResultsPresent
in Task Manager. This function is now responsible for presenting optimal search results.  
So, `we have achieved the minimum goal` of providing a `GUI` for the core functionality, mirroring
the capabilities of the original DDG SIMULA'67 program.  

For more details, see `src\gui\README.md`.

Next steps:

- Develop graphical presentations of result graphs.
- Translate all originally Hungarian texts and messages into English.
- Rewrite the SIMULA'67 program's Python mirror code in src\main folder into more elegant Python.
(The code is already in Python, but it lacks elegance.)

Immediate priority:

- Perform a comprehensive revision to ensure the application is environment-independent
and ready for download.

### 2024-04-19 09:31:49 Completed developer testing for the BusySearchOptimExec task

This core function, implemented by the `BusySearchOptimExec` task, enables the search for the
optimum in Directed Disjunctive Graphs (DDGs). For more details, see src\gui\README.md.

### 2024-04-05 23:39:47 The first real task of the Task Factory has been created

We reached a new milestone. `The first real task` of the GUI's Task Factory has been done
(in the dg_task_manager module).  
This task (represented by BusyInpTextRead(CommonRealTask) class) reads the Directed Disjunctiv
Graph description input file and checks all requirements of data.

For more details, see src\gui\README.md.

### 2024-03-27 11:40:34 Refactor: Resolve MyPy type checking issues across 19 Python files in src

This commit addresses and eliminates `MyPy type checking issues` identified in 20 Python source files
spanning all sub-folders under the src directory. A prevalent issue corrected in this process
involved variable initialization with None as an initial value, which often led to type inference
challenges. The resolution of these issues marks a significant improvement in our code's type
safety and adherence to static typing conventions.

Development and integration efforts continue unabated, with a focus on maintaining high code quality
and leveraging static analysis tools to preemptively identify and mitigate potential issues.

### 2024-03-13 12:41:48 We have reached the threshold of the integration

We have reached the threshold of the integration of the elements that form the basis
of the GUI completed so far. See the `src/gui` folder for news and updates on our ongoing
work to refine and expand the application's graphical user interface.

A new screenshot, `dg_gui_Screenshot_20240313.PNG`, has been added to the `doc` folder,
providing a current view of the GUI's appearance for reference and documentation purposes.

This milestone underscores our commitment to developing a coherent and user-friendly interface,
laying a solid foundation for future enhancements and features.

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
