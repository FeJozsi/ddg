
# `src\main` folder

Start date: 2024-02-26

## 2024-02-26 11:28:26

The `src\main` directory houses the essential components of the project.

Currently, it exclusively serves the dg_standard_input.py module,
which encapsulates functionalities mimicking the behavior of SIMULA'67's standard input.  
The module itself does not require a specific input source; wich may be
a text file or a database for example.  
The information describing a Directed Disjunctive Graph can come from input source objects
that meet the requirements of the DgInpSource abstract base class defined in this module.  
Refer to the InputTextFile class in the src\test\test_dg_input_read.py module.
Instances of this class satisfy these requirements, these properties.

You will probably try this command if you have the required Python tool installed:

- `pylint src\main\dg_standard_input.py`
