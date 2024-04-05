"""
Creating a visual map of PyQt signal usage of dg_*.py modules
"""
from graphviz import Digraph #, Graph

def generate_graph():
    """Generate a graph for the project."""
    # , strict= True, renderer=
    graph = Digraph(name= "dg_modules_graph",
                    comment= 'Modules Dependency Graph',
                    format= 'png',
                    engine= "circo" ) # engine= "dot" , rankdir= "TB"
    graph.attr(fontname= "Arial") # "Times New Roman" "Helvetica"

    my_nodes = ["dg_gui_main",
                "dg_gui_window",
                "dg_gui_draw_on_state",
                "dg_task_manager",
                "dg_gui_own_event_stack"]
    my_signals_nodes = ["my_application_quit", "redraw_my_app_window_on_state", "message_on_gui"]
    # Add nodes I.: modules
    for my_node in my_nodes:
        graph.node(my_node,
                   fontname= "Arial",
                   shape="ellipse" ) # , style="filled" , fillcolor="lightblue"
    # Add nodes II.: signals
    for my_node in my_signals_nodes:
        graph.node(my_node, fontname= "Arial", shape="box", style="filled", color="lightgrey")

    # Add edges I.: construct and serve emit func
    graph.edge("my_application_quit", "dg_gui_own_event_stack",
               label= "constr & serve emit func",
               style= "dashed", fontsize= "12")
    graph.edge("redraw_my_app_window_on_state", "dg_gui_own_event_stack",
               label= "constr & serve emit func",
               style= "dashed", fontsize= "12")
    graph.edge("message_on_gui", "dg_gui_own_event_stack",
               label= "constr & serve emit func",
               style= "dashed", fontsize= "12")
    # Add edges II.: push when ready to receive callable
    graph.edge("dg_gui_window", "dg_gui_main",
               label= "push when ready",
               style= "dashed", fontsize= "12")
    graph.edge("dg_gui_main", "dg_gui_draw_on_state",
               label= "propagate via push",
               style= "dashed", fontsize= "12")
    # Add edges III.: emit
    graph.edge("dg_gui_main", "redraw_my_app_window_on_state",
               label= "emit",
               fontname= "Arial") # , fontsize= "18"  # It works.
    graph.edge("dg_gui_main", "my_application_quit",
               label= "emit",
               fontname= "Arial")
    graph.edge("dg_gui_main", "message_on_gui",
               label= "emit",
               fontname= "Arial")
    graph.edge("dg_task_manager", "message_on_gui",
               label= "emit",
               fontname= "Arial")
    # Add edges IV.: implement
    graph.edge("redraw_my_app_window_on_state", "dg_gui_draw_on_state",
               label= "implement",
               fontname= "Arial")
    # Add edges IV.: listen (connect)
    graph.edge("my_application_quit", "dg_gui_window",
               label= "listen & implem",
               fontname= "Arial")
    graph.edge("redraw_my_app_window_on_state", "dg_gui_window",
               label= "listen",
               fontname= "Arial")
    graph.edge("message_on_gui", "dg_gui_window",
               label= "listen & implem",
               fontname= "Arial")

    # Tricks to rotate:
    # Add nodes III.: hidden start mode
    graph.node("start node", style="invisible")
    # graph.node("start node")
    # Add edges V.: sign "entry point"
    # graph.edge("hidden_start", "dg_gui_main", style="invisible", arrowhead="none")
    graph.edge("start node", "dg_gui_main", style="invisible", arrowhead="none")
    graph.edge("start node", "dg_task_manager", style="invisible", arrowhead="none")
    graph.edge("start node", "my_application_quit", style="invisible", arrowhead="none")
    graph.edge("start node", "redraw_my_app_window_on_state", style="invisible", arrowhead="none")
    graph.edge("start node", "message_on_gui", style="invisible", arrowhead="none")

    # # Tricks to align vertically the three disjoint parts and draw a different way:
    # graph.edge("generate_random_dg_problem", "dg_gui_main", style= "invisible", arrowhead="none")

    # graph.edge("dg_gui_own_event_stack", "dg_task_manager", style= "invisible", arrowhead="none")

    # # graph.edge("dg_gui_own_event_stack", "dg_main", style= "invisible", arrowhead="none")
    # graph.edge("dg_gui_finite_state_machine", "dg_main", style= "invisible", arrowhead="none")
    return graph

my_graph = generate_graph()
my_graph.render(filename= "src/test/dg_signals_graph.dot",
                view= True,
                outfile= "src/test/dg_signals_graph.png")

"""
from graphviz import Digraph

dot = Digraph()

# Default style for modules
dot.attr('node', shape='box', style='filled', color='lightgrey')

# Add module nodes
dot.node('module1', 'Module 1')
dot.node('module2', 'Module 2')

# Custom style for signal nodes
dot.attr('node', shape='ellipse', style='filled', fillcolor='lightblue')

# Add signal nodes
dot.node('signal1', 'Signal A')
dot.node('signal2', 'Signal B')

# Add edges
dot.edges(['module1signal1', 'signal1module2', 'module2signal2'])

# Generate the graph
print(dot.source)  # or dot.render('filename.gv') to save the graph
"""