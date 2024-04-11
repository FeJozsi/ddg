"""
This module is responsible for creating the graphical user
interface (GUI) of the application.  
It initializes the main window and configures all the necessary UI controls,
including buttons, text fields, and layout managers.

The main classes/functions in this module include:
- MainWindow: a class that sets up the main application window and its layout.
- mw: a module-level instance of MainWindow that will be shared

Dependencies:
- PyQt6: This module relies on the PyQt6 framework for all UI-related functionality.

Example usage:
To create and show the main window, instantiate the MainWindow class and call its show method:

    from dg_gui_window import get_main_window_instance

    app = QApplication(sys.argv)
    main_window = get_main_window_instance()
    main_window.show()
    sys.exit(app.exec())
"""

import sys
import asyncio

import os
from collections.abc import Callable
from typing import Union

from PyQt6.QtWidgets import ( QMainWindow, QFrame, QVBoxLayout, QHBoxLayout, QApplication,
                              QPushButton, QWidget, QLabel, QFileDialog,
                              QStackedWidget, QTextEdit, QGraphicsView, QGraphicsScene, QStatusBar,
                              QSpacerItem, QSizePolicy, QMessageBox, QCheckBox)
                              # QErrorMessage, QLineEdit, QGridLayout
from PyQt6.QtCore import Qt #, QTimer
from PyQt6.QtGui import QPixmap, QPainter # QTextCursor,

# import qasync

from typing_extensions import deprecated

from dg_gui_finite_state_machine import DgState, InfluEventSet, NewsType, gui_control_dict, MyButton
from dg_gui_own_event_stack import my_event_stack
from dg_gui_prepare_window import (ReadOnlyAbleCheckBox, QTextEditOutputStream,
                                   BaseForm, BaseFrame, is_valid_write_path) # , IntegerLineEdit

# The slot will be "finished" in dg_gui_main because of module import issues
# i m port dg_gui_draw_on_state
# f r om dg_gui_draw_on_state i m port r e draw_my_app_window_on_state

class TextForm(BaseForm):
    """
    This is the GUI input FORM when the Application's input comes form TEXT file
    """
    def __init__(self):
        super().__init__()

        self.init_ui()
    def init_ui(self):
        """
        Finishing initializing the Form
        """
        # Main layout:
        main_form_layout = QHBoxLayout(self)

        # Right part
        # Top - File input and Browse button
        self.file_label.setText("Input path & name:")
        self.file_input.setPlaceholderText("Select a file...") # self.file_input inherited
        self.file_input.setToolTip("A path & file contains the description of Directed "
                                   "Disjunctive Graph to search optimum")

        # Bottom - Short input fields
        # Combine layouts
        self.right_layout.addLayout(self.file_layout)
        self.right_layout.addLayout(self.input_fields_layout)

        # Add to main layout
        main_form_layout.addLayout(self.left_layout)
        main_form_layout.addLayout(self.right_layout)

        self.file_input.textChanged.connect(self.start_debounce_timer)

    def browse_file(self):
        """
        Explore the local computer files to choose one as the input of the process
        """
        file_name = self.file_input.text()
        # Option Enum: pl. QFileDialog.Option.DontUseNativeDialog | QFileDialog.Option.ShowDirsOnly
        # options = QFileDialog.Option.DontUseNativeDialog
        # file_name, _ = QFileDialog.getOpenFileName(
        #                            self, "Select File...", "", "All Files (*)", options= options)
        file_name, _ = QFileDialog.getOpenFileName(self,
                                                   "Select File...",
                                                   file_name,
                                                   "All Files (*);;Text Files (*.txt)")
        if file_name:
            self.file_input.setText(file_name)

    def check_form_completion(self): # debounce_timer.timeout
        """
        Check the text entry form to make sure it's been completely filled out
        """
        if (not self.isHidden() and not self.file_input.isReadOnly() and
            gui_control_dict["rec_state"] in (
                    DgState.IDLE_INPUT_TEXT_DEF,
                    DgState.IDLE_INP_TEXT_SATISFIED
            )):
            file_path = self.file_input.text()
            if os.path.isfile(file_path):   # if os.path.exists(file_path):
                if gui_control_dict["rec_state"] == (DgState.IDLE_INPUT_TEXT_DEF):
                    my_event_stack.post_event(e= InfluEventSet(by_forms="Filled (T)"))
            else:
                if gui_control_dict["rec_state"] == (DgState.IDLE_INP_TEXT_SATISFIED):
                    my_event_stack.post_event(e= InfluEventSet(by_forms="Missing (T)"))

class GenForm(BaseForm):
    """
    This is the GUI input FORM when the Application's input is random generated
    """
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self) -> None:
        """
        Finishing initializing the Form
        """
        # Main layout:
        main_form_layout = QHBoxLayout(self)

        # Right part
        # Bottom - File input and Browse button
        self.file_label.setText("Save as path & name:")
        self.file_input.setPlaceholderText("Select a file or a folder to save into...")
        self.file_input.setToolTip("A path & file for saving the description of the Random "
                                   "Generated Directed Disjunctive Graph to search optimum")

        # Top - Short input fields
        # Combine layouts (They are swapped in comparison with TextForm:)
        self.right_layout.addLayout(self.input_fields_layout)
        self.right_layout.addLayout(self.file_layout)

        # Add to main layout
        main_form_layout.addLayout(self.left_layout)
        main_form_layout.addLayout(self.right_layout)

        self.file_input.textChanged.connect(self.start_debounce_timer)
        for inp in self.inputs:
            inp.textChanged.connect(self.start_debounce_timer)

    def browse_file(self) -> None:
        """
        Explore the local computer path or path+file names to choose one for the new generated input
        """
        file_name: str = self.file_input.text()
        path_abs: str = os.path.abspath(file_name)
        init_path: str = ""
        dir_name: str
        # Option Enum: pl. QFileDialog.Option.DontUseNativeDialog | QFileDialog.Option.ShowDirsOnly
        # file_dialog = QFileDialog(self)
        # options = file_dialog.options() # | QFileDialog.Option.ShowDirsOnly
        # # options = QFileDialog.Option.ShowDirsOnly
        # file_name, _ = QFileDialog.getSaveFileName(self,
        #                                            "Save generated file as...",    # Dialog Title
        #                                            file_name,            # Initial Directory/Path
        #                                            "All Files (*);;Text Files (*.txt)", # Filters
        #                                            options= options)
        browser_folder: bool = ( not bool(file_name) or os.path.isdir(path_abs) or
                                 not os.path.isdir(os.path.dirname(path_abs)) or
                                 not bool(os.path.basename(file_name)) )
        return_absolute: bool = (not bool(file_name) or os.path.isabs(file_name))
        if browser_folder:
            if bool(file_name) and os.path.isdir(path_abs):
                init_path = file_name
            elif bool(file_name):
                dir_name = os.path.dirname(path_abs)
                while bool(dir_name):
                    if os.path.isdir(dir_name):
                        init_path = dir_name
                        break
                    dir_name = os.path.dirname(dir_name)
            if init_path:
                file_name = QFileDialog.getExistingDirectory(self,
                                                        "Save generated file in... (initialized)",
                                                        init_path)          # Initial Directory/Path
            else:
                file_name = QFileDialog.getExistingDirectory(self,
                                                        "Save generated file in...")  # Dialog Title
        else:
            file_name, _ = QFileDialog.getSaveFileName(self,
                                                    "Save generated file as...",    # Dialog Title
                                                    file_name,            # Initial Directory/Path
                                                    "All Files (*);;Text Files (*.txt)") # Filters
        if file_name:
            if return_absolute:
                self.file_input.setText(file_name)
            else:
                self.file_input.setText(os.path.relpath(file_name))

    def check_form_completion(self) -> None: # debounce_timer.timeout
        """
        Check the Generate form to make sure it's been completely filled out
        """
        loc_result: bool = True
        if (not self.isHidden() and not self.file_input.isReadOnly() and
            gui_control_dict["rec_state"] in (
                    DgState.IDLE_RANDOM_GEN,
                    DgState.IDLE_RAND_GEN_SATISFIED
            )):
            if (not self.inputs[0].text() or
                not self.inputs[1].text()):
                loc_result = False
            file_path = self.file_input.text()
            if loc_result and not is_valid_write_path(file_path) > 0:
                loc_result = False
            if loc_result:
                if gui_control_dict["rec_state"] == (DgState.IDLE_RANDOM_GEN):
                    my_event_stack.post_event(e= InfluEventSet(by_forms="Filled (R)"))
            else:
                if gui_control_dict["rec_state"] == (DgState.IDLE_RAND_GEN_SATISFIED):
                    my_event_stack.post_event(e= InfluEventSet(by_forms="Missing (R)"))

# 1. Top part, I. Title
class TitleFrame(BaseFrame):
    """
    Frame for 1. Top part: Title.
    """
    def __init__(self, title_text: str):
        super().__init__()
        self.setStyleSheet(
                    """
                    TitleFrame {
                        border: 2px solid #00BFFF; /* Deep Sky blue */
                        border-radius: 5px;
                        /* background-color: #ADD8E6;Baby blue */
                        /* border: 1px solid rgba(0, 0, 0, 0.15);  / *  a subtle border * /
                            / * Subtle, semi-transparent black border */
                        background-color: rgba(0, 0, 0, 30); /* #A0A0A0; */
                            /* Semi-transparent white (gray) */
                    }
                    """)
        self.loc_layout = QVBoxLayout()
        self.init_gui_t(title_text)
        self.setLayout(self.loc_layout)
    def __repr__(self) -> str:
        return "Frame for Title: " + self.title_label.text()
    def init_gui_t(self, title_text: str):
        """
        It initializes the GUI: Top 1. part
        """
        # "Title and/or Some Labels"
        self.title_label = QLabel(title_text) # "ddg Project – skeleton showing simulated actions"
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = self.title_label.font()
        # print(font.family(), font.pointSize(), font.weight())
        font.setPointSize(14)
        font.setBold(True)
        self.title_label.setFont(font)

        self.loc_layout.addWidget(self.title_label)

# 2. Top part, II. Forms (Interchanging forms)
class FormFrame(BaseFrame):
    """
    Frame for 2. Top part: Forms (Interchanging forms).
    """
    def __init__(self):
        super().__init__()

        # Adjust the size policy
        size_policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.form_stack_widget.sizePolicy().hasHeightForWidth())
        # sizePolicy.setHeightForWidth(False)
        self.setSizePolicy(size_policy)

        self.loc_layout = QVBoxLayout()
        self.init_gui_a()
        self.setLayout(self.loc_layout)
    def __repr__(self) -> str:
        return "Frame for Interchanging Forms"
    def init_gui_a(self):
        """
        It initializes the GUI: Top 2. part with two Interchanging Forms
        """
        # 2. Form part
        self.form_stack_widget = QStackedWidget() # central_widget

        # # Adjust the size policy
        # sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        # # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # # sizePolicy.setHeightForWidth(self.form_stack_widget.sizePolicy().hasHeightForWidth())
        # # sizePolicy.setHeightForWidth(False)
        # self.form_stack_widget.setSizePolicy(sizePolicy)

        self.text_form = TextForm()
        self.form_stack_widget.addWidget(self.text_form)
        self.gen_form = GenForm()
        self.form_stack_widget.addWidget(self.gen_form)

        self.loc_layout.addWidget(self.form_stack_widget)

        self.text_form.text_input_radio.stateChanged.connect(self.check_state_change)
        self.text_form.random_gen_radio.stateChanged.connect(self.check_state_change)
        self.gen_form.text_input_radio.stateChanged.connect(self.check_state_change)
        self.gen_form.random_gen_radio.stateChanged.connect(self.check_state_change)


    def check_state_change(self) -> None:
        """
        Keep the quasi Radio Buttons of the two forms synchronized and
        replace the Forms according to them.
        """
        current_index = self.form_stack_widget.currentIndex()

        # Check which quasi radio button sent the signal
        # radio_button: QRadioButton = self.sender()
        # radio_button: QCheckBox = self.sender()
        s = self.sender()
        if s is None or not isinstance(s, ReadOnlyAbleCheckBox):
            return
        assert isinstance(s, ReadOnlyAbleCheckBox)  # These informs MyPy about the type of 's'
        radio_button: ReadOnlyAbleCheckBox = s      #  in prev. line or cast(ReadOnlyAbleCheckBox,s)

        # Check if the quasi radio button is checked # and print its label
        if radio_button.isChecked():
            # print(f"{radio_button.text()} is selected")
            # QRadioButton, QCheckBox (or any checkable button in PyQt) will trigger
            #   the toggled signal if the action changes the checked state of the button.
            if radio_button.text() == "Text Input":
                self.text_form.text_input_radio.setChecked(True)
                self.gen_form.text_input_radio.setChecked(True)
                self.text_form.random_gen_radio.setChecked(False)
                self.gen_form.random_gen_radio.setChecked(False)
                if current_index == 1:
                    self.form_stack_widget.setCurrentIndex(0)
                my_event_stack.post_event(e= InfluEventSet(by_forms="Radio Text"))
            else:
                self.text_form.random_gen_radio.setChecked(True)
                self.gen_form.random_gen_radio.setChecked(True)
                self.text_form.text_input_radio.setChecked(False)
                self.gen_form.text_input_radio.setChecked(False)
                if current_index == 0:
                    self.form_stack_widget.setCurrentIndex(1)
                my_event_stack.post_event(e= InfluEventSet(by_forms="Radio Random"))

    @deprecated("Just for an early demonstration.")
    def switch_form_stack_widget(self, switch_button: QPushButton) -> None: # switch_central_widget
        """
        Deprecated: This method switches between Text Input Form and Random Generated Input Form
        It is deprecated. Its purpose was only an early demonstration.
        """
        current_index = self.form_stack_widget.currentIndex()
        if current_index == 0:
            self.form_stack_widget.setCurrentIndex(1)
            # self.switch_button.setText("Switch to TextEdit (STDOUT)")
            switch_button.setText("Switch Text Input")
            # # # Load your image here, if necessary
            # # pixmap = QPixmap("path/to/your/image.png")
            # # self.scene.clear()
            # # self.scene.addPixmap(pixmap)
            # # # self.scene.setSceneRect(pixmap.rect())
        else:
            self.form_stack_widget.setCurrentIndex(0)
            # self.switch_button.setText("Switch to Image (D. GRAPH)")
            switch_button.setText("Switch Random Gen Input")

# 3. Central part (QTextEdit or Image)
class CentralFrame(BaseFrame):
    """
    Frame for 3. central part: QTextEdit or Image.
    """
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
                    """
                    CentralFrame {
                        border: 2px solid #00BFFF; /* Deep Sky blue */
                        border-radius: 5px;
                    }
                    """)

        # Adjust the size policy
        size_policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(999999)
        # sizePolicy.setHeightForWidth(self.form_stack_widget.sizePolicy().hasHeightForWidth())
        # sizePolicy.setHeightForWidth(False)
        self.setSizePolicy(size_policy)

        self.loc_layout = QHBoxLayout()
        # # self.central_widget = QStackedWidget()
        self.init_gui_b()
        # self.switch_central_widget()
        # # self.addWidget(self.central_widget)
        self.setLayout(self.loc_layout)
    def __repr__(self) -> str:
        return "Frame for Central part"
    def init_gui_b(self):
        """
        It initializes the GUI: Central (3.) part
        """
        # Central part (QTextEdit or Image) using QStackedWidget
        self.central_widget = QStackedWidget()

        # # Adjust the size policy
        # sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        # # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(999999)
        # # sizePolicy.setHeightForWidth(self.form_stack_widget.sizePolicy().hasHeightForWidth())
        # # sizePolicy.setHeightForWidth(False)
        # self.central_widget.setSizePolicy(sizePolicy)

        self.text_edit = QTextEdit()  # self.text_edit = QTextEdit(self) parent?!?!
        self.text_edit.setReadOnly(True)
        graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        graphics_view.setScene(self.scene)
        # Load your image (ensure the path is correct)
        pixmap = QPixmap(".\\src\\gui\\Picture 1.png")  # ".\\src\\gui\\sandbox\\Picture 1.png"
        self.scene.clear()  # Clear previous content
        self.scene.addPixmap(pixmap)
        # self.scene.setSceneRect(pixmap.rect())
        # self.scene.setSceneRect(QRectF(pixmap.rect()))
        self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())

        self.central_widget.addWidget(self.text_edit)
        self.central_widget.addWidget(graphics_view)

        self.loc_layout.addWidget(self.central_widget)
    def switch_central_widget(self, switch_button: QPushButton) -> None:
        """
        This method switches between Text and Image in the central widget.
        """
        current_index = self.central_widget.currentIndex()
        if current_index == 0:
            self.central_widget.setCurrentIndex(1)
            # self.switch_button.setText("Switch to TextEdit (STDOUT)")
            switch_button.setText("Switch to TextEdit (STDOUT)")
            # # # Load your image here, if necessary
            # # pixmap = QPixmap("path/to/your/image.png")
            # # self.scene.clear()
            # # self.scene.addPixmap(pixmap)
            # # # self.scene.setSceneRect(pixmap.rect())
        else:
            self.central_widget.setCurrentIndex(0)
            # self.switch_button.setText("Switch to Image (D. GRAPH)")
            switch_button.setText("Switch to Image (D. GRAPH)")

# 4. Bottom part I. (Buttons)
class ButtonsFrame(BaseFrame):
    """
    Frame for 4. bottom part: Buttons.
    """
    def __init__(self, main_window) -> None:
        super().__init__()
        self.main_window: MainWindow = main_window
        self.loc_layout = QHBoxLayout()
        # Set the layout margins to 0
        self.loc_layout.setContentsMargins(0, 0, 0, 0)
        self.init_gui_c()
        self.setLayout(self.loc_layout)
    def __repr__(self) -> str:
        return "Frame for Buttons"
    def init_gui_c(self):
        """
        It initializes the GUI: Bottom (4.) parts for buttons
        """
        # Buttons stripe

        # self.task_button = QPushButton(
        #                   'Run Async Search Optim') # here without , parent= self param.
        # self.task_button.setFixedSize(200, 30)
        # self.task_button.clicked.connect(self.run_async_task)
        # self.loc_layout.addWidget(self.task_button)
        # self.switch_button = QPushButton("Switch to Image (D. GRAPH)") # see it on another place
        # self.switch_button.setFixedSize(200, 30)
        # self.switch_button.clicked.connect(self.main_window.central_frame.switch_central_widget)
        # self.loc_layout.addWidget(self.switch_button)

        # Button placeholders
        self.button_placeholders = [QFrame(self) for _ in range(4)]
        # for placeholder in self.button_placeholders:
        #     placeholder.setFixedHeight(50) # setMaximumHeight
        #     # Optionally set a fixed width or maximum width for the placeholders if needed
        #     # placeholder.setMaximumWidth(100)
        #     # painter = QPainter(placeholder)
        #     # painter.drawRect(placeholder.rect())
        #     # placeholder.drawFrame(painter)

        # Create buttons and a quasi button (CheckBox)
        self.button1 = QPushButton("Run Async Search Optim") # "Button 1", self

        # self.button2 = QPushButton("Change visibility") # "Button 2"
        self.checkbox2 = QCheckBox("Step by step process")
        font = self.checkbox2.font()
        # print(font.family(), font.pointSize(), font.weight())
        font.setPointSize(11)
        # font.setBold(True)
        self.checkbox2.setFont(font)

        self.button3 = QPushButton("Switch Random Gen Input") # "Button 3"
        self.button4 = QPushButton("Switch to Image (D. GRAPH)") # "Button 4"

        # Set a maximum width for buttons
        max_width = 220
        for btn in [self.button1, self.checkbox2, self.button3, self.button4]:
            btn.setMaximumWidth(max_width)
            btn.setFixedHeight(30) # setMaximumHeight

        # # Add buttons to the layout
        # self.mainLayout.addWidget(self.button1)
        # self.mainLayout.addWidget(self.button2)
        # self.mainLayout.addWidget(self.button3)
        # self.mainLayout.addWidget(self.button4)

        # Add buttons to their respective placeholders
        for i, btn in enumerate([self.button1, self.checkbox2, self.button3, self.button4]):
            layout = QHBoxLayout(self.button_placeholders[i])
            # Set the layout margins to 0
            if i == 0:
                layout.setContentsMargins(5, 0, 0, 0)
            elif i == 3:
                layout.setContentsMargins(0, 0, 5, 0)
            layout.addWidget(btn)
            self.loc_layout.addWidget(self.button_placeholders[i])

        # Example event handle I.: Start async task
        # self.button1.clicked.connect(self.run_async_task) # task_button
        self.button1.clicked.connect(
            lambda: self.propagate_button_click(MyButton.BACK, self.button1) # 0
        )

        # Example event handle II.: Hide the second button
        # self.toggleButtonVisibility(self.button3)   # It has no effect here.
        # self.checkbox2.clicked.connect(self.toggle_button3_visibility)

        # Example event handle III.: Swich GUI Input FORM
        self.button3.clicked.connect(
            # lambda: self.main_window.form_frame.switch_form_stack_widget(self.button3)
            lambda: self.propagate_button_click(MyButton.ACTION, self.button3) # 1

        )

        # Example event handle IV.: Swich central part
        self.button4.clicked.connect(
            # lambda: self.main_window.central_frame.switch_central_widget(self.button4)
            lambda: self.propagate_button_click(MyButton.NEXT, self.button4) # 2
        )

    def propagate_button_click(self, my_button: MyButton, button: QPushButton) -> None:
        """
        This method propagates the button clicks through the high level event stack
        """
        loc_event_text: str = button.text()
        if my_button == MyButton.NEXT and loc_event_text == "Generate":
            # if not confirmation_overwrite(mw= get_main_window_instance()):
            pw = self.parentWidget() #.parentWidget()
            assert pw
            pw = pw.parentWidget()
            assert isinstance(pw, MainWindow)
            lct = pw.loc_callable_tuple
            if bool(lct):
                assert isinstance(lct, tuple)
                if len(lct) >= 3:
                    lct[2]() # confirmation_overwrite(). See loc_initiate_generation_new_ddg() also
            return
        loc_by_buttons: list[str] = ["", "", ""]
        loc_by_buttons[my_button.value] = loc_event_text
        my_event_stack.post_event(InfluEventSet(by_buttons= loc_by_buttons))

    def loc_initiate_generation_new_ddg(self) -> None:
        """
        After confirmation, this method sends the appropriate high level event
        for generation new DDG description file
        """
        loc_by_buttons: list[str] = ["", "", ""]
        loc_by_buttons[MyButton.NEXT.value] = "Generate"
        my_event_stack.post_event(InfluEventSet(by_buttons= loc_by_buttons))

    @deprecated("Just for an early demonstration.")
    async def async_task(self):
        """
        Deprecated: It demonstrates the asynchronous tasks
        """
        print("Task solving Directed Disjunctive Graph started")
        self.main_window.print_status("Task solving Directed Disjunctive Graph started")

        await asyncio.sleep(5)
        print("Task completed")
        self.main_window.print_status("...COMPLETED...", -3)

    @deprecated("Just for an early demonstration.")
    def run_async_task(self):
        """
        Deprecated: It demonstrates the starting asynchronous tasks
        """
        asyncio.create_task(self.async_task())

    # Example method to toggle button visibility
    @deprecated("Just for an early demonstration.")
    def toggle_button3_visibility(self):  # , button
        """
        Deprecated: This method toggle the visibility of button3 for demonstration
        """
        self.button3.setVisible(not self.button3.isVisible())
        # self.button3.hide()
        if self.button3.isVisible():
            self.main_window.print_status("The Button3 is visible...")
            self.main_window.print_status("", 2)
        else:
            self.main_window.print_status("The Button3 disappeared...", -2)
            self.main_window.print_status("...REALLY...", 3)

# 5. Bottom part II. (Status Info)
class StatusFrame(BaseFrame):
    """
    Frame for 5. bottom part: Status Info.
    """
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
                    """
                    StatusFrame {
                        border: 2px solid #00BFFF; /* Deep Sky blue */
                        border-radius: 5px;
                        background-color: rgba(255, 255, 255, 200); /* #A0A0A0; gray */
                            /* Semi-transparent white (gray) rgba(0, 0, 0, 30) */
                    }
                    """)
        # self.setMaximumHeight(35) # setFixedHeight
        self.loc_layout = QHBoxLayout()
        # Set the layout margins to 0
        self.loc_layout.setContentsMargins(0, 0, 0, 0)
        self.init_gui_d()
        self.setLayout(self.loc_layout)
    def __repr__(self) -> str:
        return "Frame for Status"
    def init_gui_d(self):
        """
        It initializes the GUI: Bottom 5. parts: Status Info
        """
        # Status stripe
        status_bar = QStatusBar()
        font = status_bar.font()
        # print(font.family(), font.pointSize(), font.weight())
        font.setPointSize(11)
        # # font.setBold(True)
        # status_bar.setFont(font)
        # # print(font.family(), font.pointSize(), font.weight())

        # Create layout to hold items
        loc_layout = QHBoxLayout()

        # Set the layout margins to 0
        loc_layout.setContentsMargins(0, 0, 0, 0)

        # Left-aligned information
        self.left_label = QLabel("Left Info")
        # Set the minimum width
        self.left_label.setMinimumWidth(200)
        self.left_label.setFont(font)
        loc_layout.addWidget(self.left_label)

        # Spacer to push center and right apart
        loc_layout.addItem(QSpacerItem(40, 20,
                                       QSizePolicy.Policy.Expanding,
                                       QSizePolicy.Policy.Minimum))

        # Center-aligned information
        self.center_label = QLabel("Center Info")
        self.center_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.center_label.setFont(font)
        loc_layout.addWidget(self.center_label)

        # Another spacer for symmetry
        loc_layout.addItem(QSpacerItem(40, 20,
                                       QSizePolicy.Policy.Expanding,
                                       QSizePolicy.Policy.Minimum))

        # Right-aligned information
        self.right_label = QLabel("Right Info")
        self.right_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        # Set the minimum width
        self.right_label.setMinimumWidth(200)
        self.right_label.setFont(font)
        loc_layout.addWidget(self.right_label)

        # Create a QWidget to set the layout
        container = QWidget()
        container.setLayout(loc_layout)

        # Add the container widget to the status bar
        status_bar.addPermanentWidget(container, 1)

        #status_bar.showMessage("Status Info")
        self.loc_layout.addWidget(status_bar)

# Main Application Window
class MainWindow(QMainWindow):
    """
    This class represents the GUI interface's view
    """
    def __init__(self) -> None:
        super().__init__()

        # self.redraw_my_app_window_on_state_callable = None  It will be loc_callable_tuple[0]
        # self.message_on_gui_callable = None                 It will be loc_callable_tuple[1]
        self.loc_callable_tuple: Union[tuple[Callable, Callable, Callable], None] = None

        self.setWindowTitle("ddg Project")
        self.setGeometry(100, 100, 800, 600)

        # Set a central widget with transparent background

        cent_widget = QWidget(self) # stands for l_cent... = QWidget(); self.setLayout(l_cent...)
        self.setCentralWidget(cent_widget)
        cent_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # self.centralWidget

        main_layout = QVBoxLayout()

        # Initialize frames
        title_frame = TitleFrame("ddg Project")
        # print(self.title_frame)
        self.form_frame = FormFrame()
        self.central_frame = CentralFrame()
        self.buttons_frame = ButtonsFrame(self)
        self.status_frame = StatusFrame()

        # Add frames to the main_layout
        main_layout.addWidget(title_frame)
        main_layout.addWidget(self.form_frame)
        main_layout.addWidget(self.central_frame)
        main_layout.addWidget(self.buttons_frame)
        main_layout.addWidget(self.status_frame)

        cent_widget.setLayout(main_layout)

        # pixmap = QPixmap('src\\gui\\sandbox\\DALL·E 2024-03-11 16.28.47 -  3D __small.webp')
        self.pixmap = QPixmap('src\\gui\\DALL·E 2024-03-11 16.40.08 halvany__small.webp')
        self.redirect_print()

        my_event_stack.redraw_my_app_window_on_state.connect(self.loc_redraw_my_app_window_on_state)
        my_event_stack.message_on_gui.connect(self.loc_message_on_gui)
        my_event_stack.my_application_quit.connect(self.loc_my_application_quit)
        my_event_stack.initiate_generation_new_ddg.connect(self.loc_initiate_generation_new_ddg)

    def __repr__(self) -> str:
        return "Main window of the Application"

    def paintEvent(self, _): # pylint: disable=C0103 # doesn't conform to snake_case naming style
        """
        This method draws the backgroud picture
        This method over-writes the QMainWindow's one.
        """
        painter = QPainter(self)

        painter.drawPixmap(self.rect(), self.pixmap)

        # Apply semi-transparent overlay
        # painter.setOpacity(self.opacity)  # Apply the opacity level
        # painter.setBrush(QColor(0, 0, 0, 127)) # A semi-transparent overlay: 27 light, 227 dark
        # painter.setPen(Qt.PenStyle.NoPen)  # No border
        painter.drawRect(self.rect())  # Draw the overlay

        painter.end()  # Properly end the painting session

    def redirect_print(self) -> None:
        """
        Redirect print statements to QTextEdit
        Please, consider  max_char == 1300
        """
        sys.stdout = QTextEditOutputStream(self.central_frame.text_edit, 1300) # type: ignore
        # sys.stderr = QTextEditOutputStream(self.text_edit)

    def print_status(self, message: str = "", alaign_nb: int = 0) -> None:
        """
        Print a message into the bottom Status line

        Attributes:
            message   - the text being printed

            aliagn_nb - 0 - Erease any message in the Status line if not bool(message).
                            Otherwise as aliagn_nb = 1
                        1 - Write the message into the left label
                        2 - Write the message into the center label
                        3 - Write the message into the right label
                        -1 - Write the message into the left label and erase others
                        -2 - Write the message into the center label and erase others
                        -3 - Write the message into the right label and erase others
        """
        if alaign_nb < 0:
            self.print_status()
            alaign_nb = - alaign_nb
        if alaign_nb == 0 and not bool(message):
            self.status_frame.left_label.setText("")
            self.status_frame.center_label.setText("")
            self.status_frame.right_label.setText("")
        elif alaign_nb in [0, 1]:
            self.status_frame.left_label.setText(message)
        elif alaign_nb == 2:
            self.status_frame.center_label.setText(message)
        elif alaign_nb == 3:
            self.status_frame.right_label.setText(message)

    def closeEvent(self, event): # pylint: disable=C0103 # doesn't conform to snake_case naming style
        """
        This method confims the System Close Event.
        This method over-writes the QMainWindow's one.
        """
        if gui_control_dict["rec_state"] in (DgState.INIT, DgState.STOP):
            event.accept()  # Accept the close event, allowing the window to close
            return
        if gui_control_dict["rec_state"] == DgState.IDLE_INIT:
            # event.accept()
            my_event_stack.post_event(e= InfluEventSet(by_process="Close Win"))
            event.ignore()  # Ignore the close event, preventing the window from closing yet
            return

        # # Create a confirmation dialog
        # reply = QMessageBox.question(self,
        #         'Window Close',
        #         'Are you sure you want to close the ddg Project window?',
        #         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        #         QMessageBox.StandardButton.No)
        # Create a warning dialog
        reply = QMessageBox.warning(self,
                'Window Close - Attention Required',
                'This action will close the ddg Project application. Do you want to proceed?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No)
                # QMessageBox.Icon.Warning
        if reply == QMessageBox.StandardButton.Yes:
            my_event_stack.post_event(e= InfluEventSet(by_process="Confirmed Close Win"))
            # if my_event_stack.my_stack.count(Influ...(by_process="Confirmed Close Win")) >= 3:
            if sum(1 for elem in
                     my_event_stack.my_stack
                     if elem.is_watching(InfluEventSet(by_process="Confirmed Close Win"))) >= 3:
                event.accept()
                return
        event.ignore()  # Ignore the close event, preventing the window from closing (yet)

    def set_loc_callable_tuple(self, callable_tuple: tuple[Callable, Callable, Callable]) -> None:
        """
        This method "fills" the functionality used for
         - handle of redraw_my_app_window_on_state signal
         - handel of message_on_gui signal
         - confirm overwrite file when generate DDG
        """
        self.loc_callable_tuple = callable_tuple

    # def set_redraw_my_app_window_on_state(self, update_callable) -> None:
    #     """
    #     This method "fills" the functionality used for handle of
    #     redraw_my_app_window_on_state signal
    #     """
    #     # Assign the passed callable to be used for UI updates
    #     self.redraw_my_app_window_on_state_callable = update_callable

    def loc_redraw_my_app_window_on_state(self) -> None:
        """
        This method call the redrawing of the main window.
        The slot will be "filled" using self.set_loc_callable_tuple
        [[[instead of self.set_redraw_my_app_window_on_state()]]]
        in dg_gui_main because of module import issues:
        """
        # dg_gui_draw_on_state.r e draw_my_app_window_on_state()
        # r e draw_my_app_window_on_state()

        # If an update callable is set, use it; otherwise, use default logic
        # if self.redraw_my_app_window_on_state_callable:
            # self.redraw_my_app_window_on_state_callable()
        if bool(self.loc_callable_tuple):
            assert isinstance(self.loc_callable_tuple, tuple)
            if len(self.loc_callable_tuple) >= 1:
                self.loc_callable_tuple[0]()
        else:
            # Default logic to update or redraw the main window
            pass

    # def set_message_on_gui(self, update_callable) -> None:
    #     """
    #     This method "fills" the functionality used for handle of
    #     message_on_gui signal
    #     """
    #     # Assign the passed callable to be used for messages
    #     self.message_on_gui_callable = update_callable

    def loc_message_on_gui(self, m_code: str, m_type: NewsType, m_control: int, m_text: str) ->None:
        """
        This method call the message manager on the main window.
        The slot will be "filled" using self.set_loc_callable_tuple
        [[[ instead of self.set_message_on_gui() ]]]
        in dg_gui_main because of module import issues:
        """
        # If a message callable is set, use it; otherwise, use default logic
        # if self.message_on_gui_callable:
        #     self.message_on_gui_callable(m_code, m_type, m_control, m_text)
        if bool(self.loc_callable_tuple):
            assert isinstance(self.loc_callable_tuple, tuple)
            if len(self.loc_callable_tuple) >= 2:
                self.loc_callable_tuple[1](m_code, m_type, m_control, m_text)
        else:
            # Default logic to update or redraw the main window
            pass

    def loc_my_application_quit(self) -> None:
        """
        This method stops the application
        """
        i = QApplication.instance()
        assert i # This informs MyPy about the type of i of "QCoreApplication | None"
        i.quit()

    def loc_initiate_generation_new_ddg(self) -> None:
        """
        This method connect listening of the initiate_generation_new_ddg signal
        and implementing it
        """
        self.buttons_frame.loc_initiate_generation_new_ddg()

# # Create a module-level instance that will be shared
# mw: MainWindow = MainWindow() # main_window
# This does not work, because the instantiation of QApplication must precede
#   the instantiation of MainWindow or any other widgets.
_instance: MainWindow | None = None

def get_main_window_instance() -> MainWindow:
    """
    This function instantiates the main window, if it is necessary.
    """
    global _instance  # pylint: disable=W0603 # Using the global statement (global-statement)
    if _instance is None:
        _instance = MainWindow()
    return _instance
