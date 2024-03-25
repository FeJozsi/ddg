"""
This modul contains functions that draw the elements of the main window according to the state.
"""

# from PyQt6.QtWidgets import (#QApplication, QMainWindow, QFrame, QVBoxLayout, QHBoxLayout,
#                              #QPushButton, QLineEdit, QWidget, QLabel, QFileDialog,
#                              #QStackedWidget, QTextEdit, QGraphicsView, QGraphicsScene,
#                              #QStatusBar, QSpacerItem, QSizePolicy,
#                              QCheckBox
#                              #, QGridLayout, QMessageBox
#                             )
from PyQt6.QtWidgets import QLineEdit

from dg_gui_finite_state_machine import DgState, gui_control_dict, DimInpT # , InfluEventSet
from dg_gui_window import MainWindow, get_main_window_instance  # These occured circular import
from dg_gui_read_only_able_checkbox import ReadOnlyAbleCheckBox

def loc_checkbox_set_checked(rb: ReadOnlyAbleCheckBox, c: bool) -> None:
    """
    Switch the state of a radio button if it is necessary
    """
    if c:
        if not rb.isChecked():
            rb.setChecked(True)
    else:
        if rb.isChecked():
            rb.setChecked(False)
def loc_checkbox_set_disabled(rb: ReadOnlyAbleCheckBox, c: bool) -> None:
    """
    Switch the enable-disable state of a CheckBox if it is necessary
    """
    if c:
        if not rb.is_read_only(): # rb.isEnabled():
            rb.set_read_only(True)
            # rb.setDisabled(True)
    else:
        if rb.is_read_only(): # rb.isEnabled():
            rb.set_read_only(False)
            # rb.setEnabled(True)

def loc_line_edit_set_read_only(le: QLineEdit, c: bool) -> None:
    """
    Switch the read-only state of a QLineEdit if it is necessary
    """
    if c:
        if not le.isReadOnly():
            le.setReadOnly(True)
    else:
        if le.isReadOnly():
            le.setReadOnly(False)

def draw_form_stack_widget(mw: MainWindow, lrs: DgState) -> None:
    """
    Draw forms' frame stack
    See also draw_text_form and draw_gen_form.
    """
    loc_text_form = mw.form_frame.text_form
    loc_gene_form = mw.form_frame.gen_form
    if lrs.input_type in (DimInpT.TYPE_NONE, DimInpT.RANDOM_GEN, DimInpT.TEXT_INPUT):
        if lrs.input_type in (DimInpT.TYPE_NONE, DimInpT.TEXT_INPUT):
            if mw.form_frame.form_stack_widget.currentIndex() == 1:
                mw.form_frame.form_stack_widget.setCurrentIndex(0)
            if lrs.input_type == DimInpT.TYPE_NONE:
                loc_checkbox_set_checked(loc_text_form.text_input_radio, False)
                loc_checkbox_set_checked(loc_text_form.random_gen_radio, False)
                loc_checkbox_set_checked(loc_gene_form.text_input_radio, False)
                loc_checkbox_set_checked(loc_gene_form.random_gen_radio, False)

                loc_checkbox_set_disabled(loc_text_form.text_input_radio, False)
                loc_checkbox_set_disabled(loc_text_form.random_gen_radio, False)
                loc_checkbox_set_disabled(loc_gene_form.text_input_radio, False)
                loc_checkbox_set_disabled(loc_gene_form.random_gen_radio, False)

                loc_text_form.random_gen_radio.setFocus()
                mw.print_status("Please choose to randomly generate " # Directed Disjunctive Graph
                                "a DDG or use a ready-made input text file", -1) # description

            else: # DimInpT.TEXT_INPUT
                loc_checkbox_set_checked(loc_text_form.random_gen_radio, False)
                loc_checkbox_set_checked(loc_gene_form.random_gen_radio, False)
                loc_checkbox_set_checked(loc_text_form.text_input_radio, True)
                loc_checkbox_set_checked(loc_gene_form.text_input_radio, True)

                loc_checkbox_set_disabled(loc_text_form.text_input_radio, True)
                loc_checkbox_set_disabled(loc_text_form.random_gen_radio, True)
                loc_checkbox_set_disabled(loc_gene_form.text_input_radio, True)
                loc_checkbox_set_disabled(loc_gene_form.random_gen_radio, True)

                if (lrs == DgState.IDLE_INPUT_TEXT_DEF and
                    gui_control_dict["prev_state"] == DgState.IDLE_INIT
                   ):
                    loc_text_form.file_input.setFocus()
        else:  # DimInpT.RANDOM_GEN
            if mw.form_frame.form_stack_widget.currentIndex() == 0:
                mw.form_frame.form_stack_widget.setCurrentIndex(1)
            loc_checkbox_set_checked(loc_text_form.random_gen_radio, True)
            loc_checkbox_set_checked(loc_gene_form.random_gen_radio, True)
            loc_checkbox_set_checked(loc_text_form.text_input_radio, False)
            loc_checkbox_set_checked(loc_gene_form.text_input_radio, False)

            loc_checkbox_set_disabled(loc_text_form.text_input_radio, True)
            loc_checkbox_set_disabled(loc_text_form.random_gen_radio, True)
            loc_checkbox_set_disabled(loc_gene_form.text_input_radio, True)
            loc_checkbox_set_disabled(loc_gene_form.random_gen_radio, True)

            if (lrs == DgState.IDLE_RANDOM_GEN and
                gui_control_dict["prev_state"] == DgState.IDLE_INIT
               ):
                loc_gene_form.inputs[0].setFocus()

def draw_text_form(mw: MainWindow, lrs: DgState) -> None:
    """
    Draw text_form
    See also draw_form_stack_widget.
    """
    loc_text_form = mw.form_frame.text_form
    if lrs == DgState.IDLE_INIT:
        loc_line_edit_set_read_only(loc_text_form.file_input, True)
        # loc_text_form.file_input.setText("") # Important: it could work proper after set_read_only
        loc_text_form.browse_button.setText("")
        loc_text_form.browse_button.setDisabled(True)
        for inp in loc_text_form.inputs:
            inp.setText("")
            loc_line_edit_set_read_only(inp, True)

    elif lrs in (DgState.IDLE_INPUT_TEXT_DEF, DgState.IDLE_INP_TEXT_SATISFIED):
        loc_line_edit_set_read_only(loc_text_form.file_input, False)
        loc_text_form.start_debounce_timer() # loc_text_form.debounce_timer.start(500)
        loc_text_form.browse_button.setText("Browse")
        loc_text_form.browse_button.setDisabled(False)
        for inp in loc_text_form.inputs:
            loc_line_edit_set_read_only(inp, True)
        if lrs == DgState.IDLE_INPUT_TEXT_DEF:
            mw.print_status("Please, fill Input path & name of a Directed "
                            "Disjunctive Graph description text file", -1)

    else:
        loc_line_edit_set_read_only(loc_text_form.file_input, True)
        loc_text_form.browse_button.setText("Browse")
        loc_text_form.browse_button.setDisabled(True)
        loc_line_edit_set_read_only(loc_text_form.inputs[0], True)  # Nb. Machines
        loc_line_edit_set_read_only(loc_text_form.inputs[1], True)  # Nb. Operations
        loc_line_edit_set_read_only(loc_text_form.inputs[2], False) # Max. Depth
        loc_line_edit_set_read_only(loc_text_form.inputs[3], False) # Timeout
        loc_line_edit_set_read_only(loc_text_form.inputs[4], False) # Log Detail

def draw_gen_form(mw: MainWindow, lrs: DgState) -> None:
    """
    Draw gen_form
    See also draw_form_stack_widget.
    """
    loc_gen_form = mw.form_frame.gen_form
    if lrs == DgState.IDLE_INIT:
        loc_line_edit_set_read_only(loc_gen_form.file_input, True)
        # loc_gen_form.file_input.setText("") # Important: it could work proper after set_read_only
        loc_gen_form.browse_button.setText("")
        loc_gen_form.browse_button.setDisabled(True)
        # for inp in loc_gen_form.inputs:
        #     inp.setText("")
        #     loc_line_edit_set_read_only(inp, True)

    elif lrs in (DgState.IDLE_RANDOM_GEN, DgState.IDLE_RAND_GEN_SATISFIED):
        loc_line_edit_set_read_only(loc_gen_form.file_input, False)
        loc_gen_form.start_debounce_timer() # loc_gen_form.debounce_timer.start(500)
        loc_gen_form.browse_button.setText("Browse")
        loc_gen_form.browse_button.setDisabled(False)
        for inp in loc_gen_form.inputs:
            loc_line_edit_set_read_only(inp, False)
        if lrs == DgState.IDLE_RANDOM_GEN:
            mw.print_status("Please, fill Nb. Machines, Nb. Operations and "
                        "Save path & name for the new Directed Disjunctive Graph", -1)

    else:
        loc_line_edit_set_read_only(loc_gen_form.file_input, True)
        loc_gen_form.browse_button.setText("Browse")
        loc_gen_form.browse_button.setDisabled(True)
        loc_line_edit_set_read_only(loc_gen_form.inputs[0], True)  # Nb. Machines
        loc_line_edit_set_read_only(loc_gen_form.inputs[1], True)  # Nb. Operations
        loc_line_edit_set_read_only(loc_gen_form.inputs[2], False) # Max. Depth
        loc_line_edit_set_read_only(loc_gen_form.inputs[3], False) # Timeout
        loc_line_edit_set_read_only(loc_gen_form.inputs[4], False) # Log Detail

def draw_button1(mw: MainWindow, lrs: DgState) -> None:
    """
    Draw button1
    """
    loc_bframe = mw.buttons_frame
    loc_button = loc_bframe.button1
    loc_text = None
    if lrs.influ_events.by_buttons[0]:
        loc_text = lrs.influ_events.by_buttons[0]
    if loc_text is not None:
        loc_button.setDisabled(False)
        loc_button.setText(loc_text)
    else:
        loc_button.setText("")
        loc_button.setDisabled(True)

def draw_checkbox2(mw: MainWindow, lrs: DgState) -> None:
    """
    Draw checkbox2 (alias button2)
    """
    loc_bframe = mw.buttons_frame
    loc_checkb = loc_bframe.checkbox2
    if not lrs in (DgState.INIT, DgState.STOP):
        loc_checkb.setDisabled(True)

def draw_button3(mw: MainWindow, lrs: DgState) -> None:
    """
    Draw button3
    """
    loc_bframe = mw.buttons_frame
    loc_button = loc_bframe.button3
    loc_text = None
    if lrs.influ_events.by_buttons[1]:
        loc_text = lrs.influ_events.by_buttons[1]
    if loc_text is not None:
        loc_button.setDisabled(False)
        loc_button.setText(loc_text)
    else:
        loc_button.setText("")
        loc_button.setDisabled(True)

def draw_button4(mw: MainWindow, lrs: DgState) -> None:
    """
    Draw button4
    """
    loc_bframe = mw.buttons_frame
    loc_button = loc_bframe.button4
    loc_text = None
    if lrs.influ_events.by_buttons[2]:
        loc_text = lrs.influ_events.by_buttons[2]
    if loc_text is not None:
        loc_button.setDisabled(False)
        loc_button.setText(loc_text)
    else:
        loc_button.setText("")
        loc_button.setDisabled(True)

def redraw_my_app_window_on_state() -> None:
    """
    Redraw the app window according of recent state.
    It must be run inside the GUI-event-loop's thread.
    """
    main_window: MainWindow = get_main_window_instance()

    main_window.print_status() # erease bottom status line
    main_window.form_frame.text_form.debounce_timer.stop()
    main_window.form_frame.gen_form.debounce_timer.stop()

    loc_recent_state: DgState = gui_control_dict["rec_state"]

    main_window.print_status("FSM message: " + loc_recent_state.description, -1)

    draw_form_stack_widget(mw= main_window, lrs= loc_recent_state)
    draw_text_form(mw= main_window, lrs= loc_recent_state)
    draw_gen_form(mw= main_window, lrs= loc_recent_state)
    draw_button1(mw= main_window, lrs= loc_recent_state)
    draw_checkbox2(mw= main_window, lrs= loc_recent_state)
    draw_button3(mw= main_window, lrs= loc_recent_state)
    draw_button4(mw= main_window, lrs= loc_recent_state)


# This slot was temporary placed here (in dg_gui_draw_on_state) because of module import issues.
# # Originally it was in dg_gui_window:
# #    my_event_stack.redraw_my_app_window_on_state.connect(self.loc_redraw_my_app_window_on_state)

# BUT, this is wrong, because the connected code does not run in QMainWindow's thread.
# MyEventStack.redraw_my_app_window_on_state.connect(redraw_my_app_window_on_state())

# This is ALSO wrong here. Nobody calls (imports) the module.
#   And..., We must be ensured that main window not instantiated before application.
# dg_gui_window.get_main_window_instance().\
#     set_redraw_my_app_window_on_state(redraw_my_app_window_on_state)

# Finally it has went into the dg_gui_main.py
# See in dg_gui_main.py
