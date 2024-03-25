"""
This modul serves a child class for QCheckBox.
It can be set as read-only.

Later, some smaller auxiliary classes were moved here from the dg_gui_window module for clarity.
"""
import os
import errno

# from abc import ABC, abstractmethod

from PyQt6.QtWidgets import (QCheckBox, QWidget, QTextEdit, QFrame, QLineEdit,
                             QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout)
from PyQt6.QtGui import QTextCursor, QValidator
from PyQt6.QtCore import Qt, QTimer

class ReadOnlyAbleCheckBox(QCheckBox):
    """
    This class is a version of QCheckBox.
    It can be set as read-only
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_read_only = False

    def set_read_only(self, read_only):
        """Set the read-only state of the checkbox."""
        self._is_read_only = read_only

    def is_read_only(self):
        """Return the read-only state of the checkbox."""
        return self._is_read_only

    def mousePressEvent(self, e):# pylint: disable=C0103 #doesn't conform to snake_case naming st.
        """
        Handle for mouse press events.
        This method over-writes the QCheckBox's one.
        """
        if not self._is_read_only:
            super().mousePressEvent(e)
        # Else ignore the event

    def keyPressEvent(self, e):# pylint: disable=C0103 # doesn't conform to snake_case naming style
        """
        Handle for key press events.
        This method over-writes the QCheckBox's one.
        """
        if not self._is_read_only:
            super().keyPressEvent(e)
        # Else ignore the event, except allow focus navigation
        elif e.key() not in (Qt.Key.Key_Space, Qt.Key.Key_Select):
            super().keyPressEvent(e)

class QTextEditOutputStream:
    """
    This class produces the scrollable multiline LOG TEXT output screen part.
    """
    def __init__(self, text_edit: QTextEdit, max_char: int):
        self.text_edit: QTextEdit = text_edit
        self.text_edit.setStyleSheet("background-color: rgba(255, 255, 255, 200);")
        self.max_char: int = max_char # 160  # Maximum character limit

    def write(self, message: str):
        """
        Write to QTextEdit widget. Ensure the max_char not exceeded.
        """
        self.text_edit.moveCursor(QTextCursor.MoveOperation.End)
        self.text_edit.insertPlainText(message)
        # self.text_edit.moveCursor(QTextCursor.MoveOperation.End)
        # self.text_edit.ensureCursorVisible()

        # Check if the current text exceeds the maximum character limit
        current_text = self.text_edit.toPlainText()
        if len(current_text) > self.max_char:
            # Find the position to cut the text
            cut_position: int = len(current_text) - self.max_char
            new_text: str = current_text[cut_position:]
            if cut_position != -1:
                cut_position = new_text.find("\n")
                new_text = new_text[cut_position + 1:]  # len("\n") = always 1!

            # Update the QTextEdit (test_edit) with the trimmed text
            self.text_edit.setPlainText(new_text)
            self.text_edit.moveCursor(QTextCursor.MoveOperation.End)
            self.text_edit.ensureCursorVisible()

    def flush(self):
        """
        Flush the buffers.
        QTextEdit handles its updates and display internally.
        There's no need to manually manage a buffer
        that requires flushing to ensure data is written or displayed
        """
        # pass

# This led to typeError: metaclass conflict: the metaclass of a derived class must be
#   a (non-strict) subclass of the metaclasses of all its bases
# class AbstractFormMixin(ABC):
class AbstractFormMixin(): # pylint: disable=R0903  # Too few public methods
    """
    This class is for a Mixin.
    It keeps the quasi abstract method requirements separate from the primary class hierarchy.
    Also, it builds the set of layouts.
    """
    def __init__(self):
        # Main layout: self.main_form_layout = QHBoxLayout(self)
        # Left part - Radio Buttons
        self.left_layout = QVBoxLayout()
        # Right part
        self.right_layout = QVBoxLayout()
        # File input and Browse button
        self.file_layout = QHBoxLayout()
        # Short input fields
        self.input_fields_layout = QGridLayout()

    # @abstractmethod
    def check_form_completion(self):
        """
        This method must be implemented in the child classes of BaseForm.
        """

    # @abstractmethod
    def browse_file(self):
        """
        This method must be implemented in the child classes of BaseForm.
        """

# Base class for our Forms
class BaseForm(QWidget, AbstractFormMixin): # pylint: disable=R0903  # Too few public methods
    """
    Basically, the GUI's forms are built as objects of the BaseForm class's descendant.
    This class is a skeleton.
    This class using a Mixin for the quasi Abstract Methods (check_form_completion, browse_file).
    """
    # Colours:  black, cyan, blue
    # background-color: #ADD8E6; /* Baby blue */
    # #87CEEB; /* Sky blue */
    # #00BFFF; /* Deep Sky blue */
    # #F4C2C2; /* Middle baby pink */
    def __init__(self):
        super().__init__()

        # Ensure the subclass has implemented the required methods.
        if type(self).check_form_completion == AbstractFormMixin.check_form_completion:
            raise NotImplementedError("The subclass does not implement check_form_completion.")
        if type(self).browse_file == AbstractFormMixin.browse_file:
            raise NotImplementedError("The subclass does not implement browse_file.")

        # self.setObjectName("MyForm")
        # # self.setStyleSheet(
        # #             """
        # #             BaseForm {  /* QWidget#MyForm */
        # #                 border: 2px solid #E7A9C4; /* Light purple */
        # #                 border-radius: 5px;
        # #             }
        # #             """)
        # # Create and set font attributes
        # # font = QFont('Arial', 12, QFont.Weight.Bold)  # Font family, size, and weight
        font = self.font()
        # font.setItalic(True)  # Set font style to italic
        font.setPointSize(11)
        self.setFont(font)
        # self.setStyleSheet("QWidget#MyForm {  font-size: 11pt; }") # font-family: Arial;

        # font=self.font()
        # print(font.family(), font.pointSize(), font.weight())

        # font=super().font()
        # print(font.family(), font.pointSize(), font.weight())

        # self.setFont(super().font())
        # font=self.font()
        # print(font.family(), font.pointSize(), font.weight())

        self.init_ui_base()

    def init_ui_base(self):
        """
        It initializes the BaseForm
        """
        # Main layout: self.main_form_layout = QHBoxLayout(self)

        font=self.font()

        # Left part - Radio Buttons: self.left_layout = QVBoxLayout()
        self.random_gen_radio = ReadOnlyAbleCheckBox("Random Gen.")# QCheckBox (quasi QRadioButton)
        self.random_gen_radio.setFont(font)
        self.text_input_radio = ReadOnlyAbleCheckBox("Text Input") # QCheckBox (quasi QRadioButton)
        self.text_input_radio.setFont(font)
        self.left_layout.addWidget(self.random_gen_radio)
        self.left_layout.addWidget(self.text_input_radio)

        # Right part: self.right_layout = QVBoxLayout()
        # File input and Browse button: self.file_layout = QHBoxLayout()
        self.file_label = QLabel("*") # Save as path & name:
        self.file_label.setFont(font)

        self.file_input = QLineEdit()
        self.file_input.setFont(font)
        self.browse_button = QPushButton("Browse")
        # browse_button.setFixedSize(66, 30)
        self.browse_button.clicked.connect(self.browse_file)
        self.file_layout.addWidget(self.file_label)
        self.file_layout.addWidget(self.file_input)
        self.file_layout.addWidget(self.browse_button)

        # Short input fields: self.input_fields_layout = QGridLayout()
        labels = ["Nb. Machines", "Nb. Operations", "Max. Depth", "Timeout", "Log Detail"]
        self.inputs = [IntegerLineEdit() for _ in labels]
        self.inputs[0].setToolTip("Number of Machines. The operations set on "
                                  "one of the same machines can not be produced one a time.")
        self.inputs[1].setToolTip("Number of Operations. Each machine must have "
                                  "an operation connected at least.")
        self.inputs[2].setPlaceholderText("default 15 levels")
        self.inputs[2].setToolTip("Maximum Depth of the solution tree using the Branch "
                                  "and Bound method. Can be adjusted during making iterations.")
        self.inputs[3].setPlaceholderText("default 300 sec")
        self.inputs[3].setToolTip("Maximum  time searching of the optimum in seconds. "
                                  "Can be adjusted during making iterations.")
        self.inputs[4].setPlaceholderText("0 / 1 (or >0)")
        self.inputs[4].setToolTip("Log Detail. 0 = normal Log, > 0 = detailed Log. "
                                  "Can be adjusted during making iterations.")
        for i, label in enumerate(labels):
            loc_label = QLabel(label)
            loc_label.setFont(font)
            self.input_fields_layout.addWidget(loc_label, 0, i)
            self.inputs[i].setFont(font)
            self.input_fields_layout.addWidget(self.inputs[i], 1, i)

        self.debounce_timer = QTimer(self)
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self.check_form_completion)

    def start_debounce_timer(self):
        """
        Start debounce timer to foresee the inspection of the FORM (check_form_completion)
        after a 0.5 sec idle
        """
        if (not self.isHidden() and not self.file_input.isReadOnly()):
            self.debounce_timer.start(500)  # 500 ms delay

# Base class for our frames
class BaseFrame(QFrame): # pylint: disable=R0903  # Too few public methods
    """
    Basically, the GUI is built from objects of the BaseFrame class.
    This is a skeleton, a pseudo ABC.
    """
    # Colours:  black, cyan, blue
    # background-color: #ADD8E6; /* Baby blue */
    # #87CEEB; /* Sky blue */
    # #00BFFF; /* Deep Sky blue */
    # #F4C2C2; /* Middle baby pink */
    def __init__(self):
        super().__init__()
        self.setObjectName("FrameWithBorder")
        self.setStyleSheet(
                    """
                    QFrame#FrameWithBorder {
                        border: 2px solid #E7A9C4; /* Light purple */
                        border-radius: 5px;
                        background-color: rgba(0, 0, 0, 20); /* #A0A0A0; gray */
                            /* Semi-transparent white (gray) */
                    }
                    """)

class StrictIntOrEmptyValidator(QValidator):
    """
    Strict Integer or Empty Validator for QLineEdit()
    """
    def __init__(self, parent=None): # pylint: disable=W0246 # Useless parent or super() delegation
        super().__init__(parent)     #         in method '__init__' (useless-parent-delegation)

    def validate(self, input_str, pos):
        """
        Validate during keyboard presses
        """
        if input_str == "":
            return QValidator.State.Acceptable, input_str, pos
        if input_str.isdigit():
            return QValidator.State.Acceptable, input_str, pos
        return QValidator.State.Invalid, input_str, pos

    def fixup(self, _): # input_str
        """
        Attempt to clean up the input; not needed for our current use case
        """
        # pass

class IntegerLineEdit(QLineEdit): # pylint: disable=R0903  # Too few public methods
    """
    This class a version of QLineEdit using
    strict Integer or Empty validation
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set the custom validator right when the widget is initialized
        self.setValidator(StrictIntOrEmptyValidator(self))

def is_valid_write_path(path) -> int:
    """
    Check if a path is a valid write path (folder path) or a writable file URL

    Return: 0 - path is wrong
            1 - path is a writable file URL
            2 - path is a writable file URL
    """
    # Check if the directory exists
    ret_val: int = 1
    try:
        directory = os.path.dirname(path)
        if not os.path.isdir(directory):
            # print(f"Directory does not exist: {directory}")
            ret_val = 0 # return False

        # Check if the file exists and is writable
        elif os.path.exists(path) and not os.path.isfile(path):
            # print(f"Path exists but is not a file: {path}")
            # return False
            ret_val = 2 # only a path without file name

        if (ret_val > 0 and
            os.path.exists(path) and not os.access(path, os.W_OK)):
            # print(f"File exists but is not writable: {path}")
            ret_val = 0 # return False
    except Exception as _: # pylint: disable=W0718 # Catching too general
                           #  ... exception Exception (broad-exception-caught)
        # print(f"An unexpected error occurred: {e}")
        ret_val = 0 # return False

    if not ret_val == 1:
        return ret_val

    # Try to open the file in append mode to check write permission without altering the file
    my_length:int = -1
    try:
        # Get the size of the file
        my_length = max(os.stat(path).st_size, 1)
    except FileNotFoundError:
        my_length = 0
    try:
        with open(path, 'a'): # pylint: disable=W1514 # Using open without explicitly
            pass              # specifying an encoding (unspecified-encoding)
    except IOError as e:      # This is only a test.
        if e.errno == errno.EACCES:
            # print(f"No write permission for the file: {path}")
            ret_val = 0 # return False
        # Directory does not exist or no permission to create file
        elif e.errno in [errno.ENOENT, errno.EPERM, errno.EACCES]:
            # print(f"Directory '{directory}' does not exist or no permission to write: {path}")
            ret_val = 0 # return False
        else:
            # Other IO errors
            # print(f"Unable to write to file due to an IOError: {path}")
            ret_val = 0 # return False
    except Exception as _: # pylint: disable=W0718 # Catching too general
                           #  ... exception Exception (broad-exception-caught)
        # print(f"An unexpected error occurred: {e}")
        ret_val = 0 # return False

    if ret_val == 1 and my_length == 0:
        os.remove(path) # Erasing the trace of the experiment

    return ret_val # True
