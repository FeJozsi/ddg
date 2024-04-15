"""
This modul contains functions that draw the elements of the main window according to the state.
"""
# import sys
import os

from PyQt6.QtWidgets import QLineEdit, QMessageBox #, QErrorMessage

from dg_gui_finite_state_machine import DgState, MyButton, NewsType, gui_control_dict, DimInpT
from dg_gui_window import MainWindow, get_main_window_instance  # These occured circular import
from dg_gui_prepare_window import ReadOnlyAbleCheckBox
from dg_gui_own_event_stack import my_event_stack

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
    if lrs.influ_events and lrs.influ_events.by_buttons[MyButton.BACK.value]: # 0
        loc_text = lrs.influ_events.by_buttons[MyButton.BACK.value] # 0
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
        if lrs in (DgState.IDLE_HAVE_ROOT_INPUT, DgState.BUSY_SEARCH_OPTIM_EXEC,
                   DgState.IDLE_SEARCH_OPT_PAUSE, DgState.BUSY_RECENT_OPT_PRESENT,
                   DgState.IDLE_RECENT_OPT_PRESENT):
            loc_checkb.setEnabled(True)
        else:
            loc_checkb.setDisabled(True)

def draw_button3(mw: MainWindow, lrs: DgState) -> None:
    """
    Draw button3
    """
    loc_bframe = mw.buttons_frame
    loc_button = loc_bframe.button3
    loc_text = None
    if lrs.influ_events and lrs.influ_events.by_buttons[MyButton.ACTION.value]: # 1
        loc_text = lrs.influ_events.by_buttons[MyButton.ACTION.value] # 1
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
    if lrs.influ_events and lrs.influ_events.by_buttons[MyButton.NEXT.value]: # 2
        loc_text = lrs.influ_events.by_buttons[MyButton.NEXT.value] # 2
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
# # my_event_stack.r e draw_my_app_window_on_state.connect(self.loc_r e draw_my_app_window_on_state)

# BUT, this is wrong, because the connected code does not run in QMainWindow's thread.
# MyEventStack.r e draw_my_app_window_on_state.connect(r e draw_my_app_window_on_state())

# This is ALSO wrong here. Nobody calls (imports) the module.
#   And..., We must be ensured that main window not instantiated before application.
# dg_gui_window.get_main_window_instance().\
#     set_r e draw_my_app_window_on_state(r e draw_my_app_window_on_state)

# Finally it has went into the dg_gui_main.py
# See in dg_gui_main.py

def message_on_gui(m_code: str, m_type: NewsType, m_control: int, m_text: str) -> None:
    """ Manage sending messages on GUI """
    main_window: MainWindow = get_main_window_instance()
    if m_type.name.startswith("FILL_"):
        fill(main_window, m_code, m_type, m_control, m_text)
    if m_type.name.endswith("_WIN"):
        win(main_window, m_code, m_type, m_control, m_text)

def fill(mw: MainWindow, m_code: str, m_type: NewsType, _: int, m_text: str) -> None:
    """ Manage writing into fields on GUI """
    assert m_code
    if m_type == NewsType.FILL_NB_MACHINE:
        mw.form_frame.text_form.inputs[0].setText(m_text)
    elif m_type == NewsType.FILL_NB_OPER:
        mw.form_frame.text_form.inputs[1].setText(m_text)
    elif m_type == NewsType.FILL_MAX_DEPTH:
        mw.form_frame.text_form.inputs[2].setText(m_text)
    elif m_type == NewsType.FILL_TIMEOUT:
        mw.form_frame.text_form.inputs[3].setText(m_text)
    elif m_type == NewsType.FILL_LOG_DETAIL:
        mw.form_frame.text_form.inputs[4].setText(m_text)
    elif m_type == NewsType.FILL_GEN_FILE:
        # print(m_text)
        mw.form_frame.gen_form.file_input.setText(m_text)

def win(mw: MainWindow, m_code: str, m_type: NewsType, _: int, m_text: str) -> None:
    """ Manage open modal window for messages on GUI """
    if m_type.name.startswith("ERROR_"):
        # print(gui_control_dict["rec_state"],
        #         file= sys.stderr)
        # print(len(my_event_stack.my_stack),
        #         file= sys.stderr)
        # sys.stderr.flush()

        # QErrorMessage(mw).showMessage(m_text + "\n(" + m_code + ")") # "Something went wrong!"
        # QErrorMessage(mw).showMessage(...) does not(!) occur the problemm, below:
        #     RuntimeError: Cannot enter into task <Task pending name='Task-1' running at ...
        #        wait_for=<Future finished result=None>> while another task
        #        <Task pending name='Task-2' coro=<carry_out_processes() running at ...
        #       is being executed.

        # # This, below, does occur the problem (explained above):
        # reply = QMessageBox.warning(mw,
        #         "ddg Project - Error message",
        #         m_text + "\n(" + m_code + ")",  # "Something went wrong!"
        #         QMessageBox.StandardButton.Ok, # QMessageBox.StandardButton.Yes | ... .No,
        #         QMessageBox.StandardButton.Ok)
        #         # QMessageBox.Icon.Warning

        error_dialog = QMessageBox(mw)
        error_dialog.setWindowTitle("ddg Project - Error message")
        error_dialog.setIcon(QMessageBox.Icon.Warning)
        error_dialog.setText( m_text + "\n(" + m_code + ")")  # "Something went wrong!"
        error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)

        # error_dialog.exec() # Avoid(!) using exec() in asyncio applications because it's
        #                         a blocking call that can interfere with the asyncio event loop!
        # The conflict arises because exec() is a blocking call that starts a local event loop
        #   to wait for the dialog to close. It blocks the asyncio-driven PyQt loop mechanism.
        error_dialog.setModal(True)  # Make the dialog modal if needed
        error_dialog.show()

def confirmation_overwrite() -> None:
    """
        Confirmation of overwrite a file, if it is necessary,
        then emit signal to create the appropriate high level event.
        It runs under QMainWindow!
    """
    mw: MainWindow = get_main_window_instance()
    path: str = mw.form_frame.gen_form.file_input.text()
    path_abs = os.path.abspath(path)
    if os.path.isfile(path_abs):
        warning_dialog = QMessageBox(mw)
        warning_dialog.setWindowTitle("ddg Project - WARNING")
        warning_dialog.setIcon(QMessageBox.Icon.Warning)
        loc_message: str = "Please, confirm overwriting the file: \n" + path
        if not os.path.isabs(path):
            loc_message += "\n\n( Full path: \n" + path_abs + ")"
        warning_dialog.setText( loc_message )
        warning_dialog.setStandardButtons(QMessageBox.StandardButton.Ok |
                                          QMessageBox.StandardButton.Cancel)
        warning_dialog.setDefaultButton(QMessageBox.StandardButton.Cancel)
        # warning_dialog.exec() # Avoid(!) using exec() in asyncio applications because it's
        #                         a blocking call that can interfere with the asyncio event loop!
        # The conflict arises because exec() is a blocking call that starts a local event loop
        #   to wait for the dialog to close. It blocks the asyncio-driven PyQt loop mechanism.
        warning_dialog.setModal(True)  # Make the dialog modal if needed
        # warning_dialog.show()
        def button_clicked() -> None:
        # def button_clicked(button) -> None:
            wdc = warning_dialog.clickedButton()
            assert wdc
            if wdc.text().upper() == "OK":  # It worked fine...
            # if button.text().upper() == "OK":                It does not work in PyQt6
                my_event_stack.emit_initiate_generation_new_ddg()
            # else:
            #     print("Cancel clicked")
        warning_dialog.open(button_clicked)
    else:
        my_event_stack.emit_initiate_generation_new_ddg()
