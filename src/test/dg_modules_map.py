"""
Creating a visual map of dg_*.py modules and their relationships (imports) in the project
"""
import os
import re
from graphviz import Digraph #, Graph

def scan_for_imports(file_path):
    """Extract imported modules from a Python file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # This regex finds all imported modules; might need adjustments
    imports = re.findall(r'^import (\S+)|^from (\S+) import', content, re.MULTILINE)
    # Flatten the list and remove None
    # my_imports = [imp for imp in sum(imports, ()) if imp]
    my_imports = [imp for imp in sum(imports, ()) if (imp and "dg_" in imp)]
    return set(my_imports)

def generate_graph(loc_project_root):
    """Generate a graph for the project."""
    # , strict= True, renderer=
    graph = Digraph(name= "dg_modules_graph",
                    comment= 'Modules Dependency Graph',
                    format= 'png',
                    engine= "dot" )
    graph.attr(fontname= "Arial") # "Times New Roman" "Helvetica"
    # graph = Digraph(comment='Modules Dependency Graph', format='png', engine= "fdp" )
    # graph = Digraph(comment='Modules Dependency Graph', format='png', engine= "circo" )
    # # # It does not work:
    # # graph = Digraph(comment='Modules Dependency Graph', format='png', engine= "sfdp" )
    # # # It is messy:
    # # graph = Digraph(comment='Modules Dependency Graph', format='png', engine= "neato" )
    # # graph = Digraph(comment='Modules Dependency Graph', format='png', engine= "twopi" )
    # # graph = Digraph(comment='Modules Dependency Graph', format='png', engine= "osage" )
    # # # It is for documentation:
    # # # graph = Graph(comment='Modules Dependency Graph', format='png')

    added_nodes = []
    visited_files = {}
    for root, _, files in os.walk(loc_project_root): # root, dirs, files
        if "sandbox" in root or "test" in root:
            continue
        for file in files:
            if not "dg_" in file:
                continue
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                # module_name = os.path.relpath(file_path,
                #               start=loc_project_root).replace(os.sep, '.').rstrip('.py')
                module_name = file.rstrip('.py')
                # Add nodes I.:
                if module_name not in added_nodes:
                    added_nodes.append(module_name)
                    graph.node(module_name, fontname= "Arial")
                loc_imports = scan_for_imports(file_path)
                for imp in loc_imports:
                    # Add nodes II.:
                    if imp not in added_nodes:
                        graph.node(imp, fontname= "Arial")
                        added_nodes.append(imp)
                # Add edges:
                if module_name not in visited_files:
                    visited_files[module_name] = loc_imports
                    for imp in loc_imports:
                        graph.edge(module_name, imp) # , fontname= "Arial"

    graph.edge("dg_main", "dg_link", style= "dashed")
    # Tricks to align vertically the three disjoint parts and draw a different way:
    graph.edge("generate_random_dg_problem", "dg_gui_main", style= "invisible", arrowhead="none")

    graph.edge("dg_gui_own_event_stack", "dg_task_manager", style= "invisible", arrowhead="none")

    # graph.edge("dg_gui_own_event_stack", "dg_main", style= "invisible", arrowhead="none")
    graph.edge("dg_gui_finite_state_machine", "dg_main", style= "invisible", arrowhead="none")
    return graph

PROJECT_ROOT = 'src'
my_graph = generate_graph(PROJECT_ROOT)
my_graph.render(filename= "src/test/dg_modules_graph.dot",
                view= True,
                outfile= "src/test/dg_modules_graph.png")
