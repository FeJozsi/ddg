
# `src\main` folder

Start date: 2024-02-26  
The `src\main` directory houses the essential components of the project.

## 2024-04-03 13:50:05 Continue development with enhanced input handling

- Introduced custom exceptions for input management, centralized in `src/main/dg_exceptions.py`.
- Refined EOF detection to enhance reliability. For this purpose, the DgInpSource ABC within
the dg_standard_input.py module has been updated with a new method named serve_line_if_any.
This method tolerates the case when no more data is present on the input;
it merely sets the 'eof' status.
- Made input text parsing more flexible while enforcing stricter data type requirements.

Note: Integration of main functions into the GUI is ongoing and far from complete.

## 2024-03-27 11:40:34 Refactor: Resolve MyPy type checking issues across 19 Python files in src

This folder is also affected by the scan. See the ReadMe.md file in the root folder for more details.

## 2024-02-29 10:00:59

I've added the missing parts of the entire project as it is nowdays.  
I intend to equip it with a GUI later on.  
To solve Directed Disjunctive Graphs, you must initiate the dg_main module.
It writes the data from input and the results to the TERMINAL/Command screen.  

You will probably try these commands if you have the required Python tools installed:

- `python src\main\dg_main.py inputs\dg_input.txt`
- `python src\main\dg_main.py inputs\dg_gen_input_38m_11g_20240223121500.txt`
- `python src\main\dg_main.py inputs\dg_gen_input_100m_4g_20240220111417.txt`
- `pylint src\main\dg_link.py`
- `pylint src\main\dg_standard_input.py`
- `pylint src\main\dg_main.py`
- `pylint src\main\dg_high_level_pseudo_black_boxes.py`
- `pylint src\main\finomitasok.py, src\main\megoldasfa.py, src\main\vezerles.py --disable="C0116,C0301,R0902"`
- `pylint src\main\diszjunktiv_graf.py, src\main\diszjunktiv_graf_manipulacioi.py, src\main\Szabad_elek__korlatozas_egy_gepen.py --disable="C0103,C0116,C0301,C0321,R0902,R0912,R0915"`

With the used --disable="C0301, C0116, R0902, C0321, R0915, R0912, C0103" option
we excluded the PYLINT warnings listed below:

- C0103: Class name <"..."> doesn't conform to PascalCase naming style (invalid-name)
- C0116: Missing function or method docstring (missing-function-docstring)
- C0301: Line too long (nnn/100) (line-too-long)
- C0321: More than one statement on a single line (multiple-statements)
- R0902: Too many instance attributes (mm/7) (too-many-instance-attributes)
- R0912: Too many branches (yy/12) (too-many-branches)
- R0915: Too many statements (xx/50) (too-many-statements)

## 2024-02-26 11:28:26

The src\main directory houses the essential components of the project.

Currently, it exclusively serves the dg_standard_input.py module,
which encapsulates functionalities mimicking the behavior of SIMULA'67's standard input.  
The module itself does not require a specific input source; wich may be
a text file or a database for example.  
The information describing a Directed Disjunctive Graph can come from input source objects
that meet the requirements of the DgInpSource abstract base class (ABC) defined in this module.  
Refer to the InputTextFile class in the src\test\test_dg_input_read.py module.
Instances of this class satisfy these requirements, these properties.

You will probably try this command if you have the required Python tool installed:

- `pylint src\main\dg_standard_input.py`
