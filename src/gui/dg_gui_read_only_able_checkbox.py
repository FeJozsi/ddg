"""
This modul serves a child class for QCheckBox.
It can be set as read-only.

Later, some smaller auxiliary classes were moved here from the dg_gui_window module for clarity.
"""
import os
import errno

# from abc import ABC, abstractmethod

from PyQt6.QtWidgets import QCheckBox, QWidget, QTextEdit, QFrame, QLineEdit
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
    It keeps the quasi abstract method requirements separate from the primary class hierarchy
    """
    # @abstractmethod
    def check_form_completion(self):
        """
        This method must be implemented in the child classes.
        """

# Base class for our Forms
class BaseForm(QWidget, AbstractFormMixin): # pylint: disable=R0903  # Too few public methods
    """
    Basically, the GUI's forms are built as objects of the BaseForm class's descendant.
    This class is a skeleton.
    This class using a Mixin for Abstract Method check_form_completion.
    """
    # Colours:  black, cyan, blue
    # background-color: #ADD8E6; /* Baby blue */
    # #87CEEB; /* Sky blue */
    # #00BFFF; /* Deep Sky blue */
    # #F4C2C2; /* Middle baby pink */
    def __init__(self):
        super().__init__()

        # Ensure the subclass has implemented the required method.
        if type(self).check_form_completion == AbstractFormMixin.check_form_completion:
            raise NotImplementedError("The subclass does not implement check_form_completion.")

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

        self.file_input = QLineEdit()
        self.file_input.setFont(font)

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
