"""
This modul is the main part of the project's GUI.
Its responsibilities are:
- 100% for View alon;
- with dg_gui_finite_state_machine.py together for Control.
"""

import sys
import asyncio

from PyQt6.QtWidgets import ( QApplication, QMainWindow, QFrame, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLineEdit, QWidget, QLabel, QFileDialog,
                              QStackedWidget, QTextEdit, QGraphicsView, QGraphicsScene, QStatusBar,
                              QSpacerItem, QSizePolicy, QRadioButton, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor, QPixmap, QPainter

import qasync

class QTextEditOutputStream:
    """
    This class produces the scrollable multiline LOG TEXT output screen part.
    """
    def __init__(self, text_edit: QTextEdit, max_char: int):
        self.text_edit: QTextEdit = text_edit
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

# Base class for our Forms
class BaseForm(QWidget): # pylint: disable=R0903  # Too few public methods
    """
    Basically, the GUI's forms are built as objects of the BaseForm class's descendant.
    This is a skeleton, a pseudo ABC.
    """
    # Colours:  black, cyan, blue
    # background-color: #ADD8E6; /* Baby blue */
    # #87CEEB; /* Sky blue */
    # #00BFFF; /* Deep Sky blue */
    # #F4C2C2; /* Middle baby pink */
    def __init__(self):
        super().__init__()
        self.setObjectName("MyForm")
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
class TextForm(BaseForm):
    """
    This is the GUI input FORM when the Application's input comes form TEXT file
    """
    def __init__(self):
        super().__init__()

        # font=self.font()
        # print(font.family(), font.pointSize(), font.weight())

        # font=super().font()
        # print(font.family(), font.pointSize(), font.weight())

        # self.setFont(super().font())
        # font=self.font()
        # print(font.family(), font.pointSize(), font.weight())

        self.init_ui()
    def init_ui(self):
        """
        It initializes the Form
        """
        # Main layout
        main_form_layout = QHBoxLayout(self)

        font=self.font()

        # Left part - Radio Buttons
        left_layout = QVBoxLayout()
        self.random_gen_radio = QRadioButton("Random Gen.")
        self.random_gen_radio.setFont(font)
        self.text_input_radio = QRadioButton("Text Input")
        self.text_input_radio.setFont(font)
        left_layout.addWidget(self.random_gen_radio)
        left_layout.addWidget(self.text_input_radio)

        # Right part
        right_layout = QVBoxLayout()

        # Top - File input and Browse button
        file_layout = QHBoxLayout()
        file_label = QLabel("Input path & name:")
        file_label.setFont(font)
        self.file_input = QLineEdit()
        self.file_input.setFont(font)
        self.browse_button = QPushButton("Browse")
        # browse_button.setFixedSize(66, 30)
        self.browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.browse_button)

        # Bottom - Short input fields
        input_fields_layout = QGridLayout()
        labels = ["Nb. Machines", "Nb. Operations", "Max. Depth", "Timeout", "Log Detail"]
        self.inputs = [QLineEdit() for _ in labels]

        for i, label in enumerate(labels):
            loc_label = QLabel(label)
            loc_label.setFont(font)
            input_fields_layout.addWidget(loc_label, 0, i)
            self.inputs[i].setFont(font)
            input_fields_layout.addWidget(self.inputs[i], 1, i)

        # Combine layouts
        right_layout.addLayout(file_layout)
        right_layout.addLayout(input_fields_layout)

        # Add to main layout
        main_form_layout.addLayout(left_layout)
        main_form_layout.addLayout(right_layout)

    def browse_file(self):
        """
        Explore the local computer files to choose one as the input of the process
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File...", "", "All Files (*)")
        if file_name:
            self.file_input.setText(file_name)

class GenForm(BaseForm):
    """
    This is the GUI input FORM when the Application's input is random generated
    """
    def __init__(self):
        super().__init__()

        self.init_ui()

        # font=self.font()
        # print(font.family(), font.pointSize(), font.weight())

        # font=super().font()
        # print(font.family(), font.pointSize(), font.weight())

        # self.setFont(super().font())
        # font=self.font()
        # print(font.family(), font.pointSize(), font.weight())

        # self.setFont(super().font()) # After each child exists.
        # self.setStyleSheet("GenForm {  font-size: 11pt; }") # font-family: Arial;

    def init_ui(self):
        """
        It initializes the Form
        """
        # Main layout
        main_form_layout = QHBoxLayout(self)

        font=self.font()

        # Left part - Radio Buttons
        left_layout = QVBoxLayout()
        self.random_gen_radio = QRadioButton("Random Gen.")
        self.random_gen_radio.setFont(font)
        self.text_input_radio = QRadioButton("Text Input")
        self.text_input_radio.setFont(font)
        left_layout.addWidget(self.random_gen_radio)
        left_layout.addWidget(self.text_input_radio)

        # Right part
        right_layout = QVBoxLayout()

        # Bottom - File input and Browse button
        file_layout = QHBoxLayout()
        file_label = QLabel("Save as path & name:")
        file_label.setFont(font)
        self.file_input = QLineEdit()
        self.file_input.setFont(font)
        self.browse_button = QPushButton("Browse")
        # browse_button.setFixedSize(66, 30)
        self.browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.browse_button)

        # Top - Short input fields
        input_fields_layout = QGridLayout()
        labels = ["Nb. Machines", "Nb. Operations", "Max. Depth", "Timeout", "Log Detail"]
        self.inputs = [QLineEdit() for _ in labels]

        for i, label in enumerate(labels):
            loc_label = QLabel(label)
            loc_label.setFont(font)
            input_fields_layout.addWidget(loc_label, 0, i)
            self.inputs[i].setFont(font)
            input_fields_layout.addWidget(self.inputs[i], 1, i)

        # Combine layouts (They are swapped in comparison with TextForm:)
        right_layout.addLayout(input_fields_layout)
        right_layout.addLayout(file_layout)

        # Add to main layout
        main_form_layout.addLayout(left_layout)
        main_form_layout.addLayout(right_layout)

    def browse_file(self):
        """
        Explore the local computer path+file names to choose one for the new generated input
        """
        file_name, _ = QFileDialog.getOpenFileName(self,
                                                   "Save generated file as...",
                                                   "",
                                                   "All Files (*)")
        if file_name:
            self.file_input.setText(file_name)


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
# 1. Top part. Title
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
        self.layout = QVBoxLayout()
        self.init_gui_t(title_text)
        self.setLayout(self.layout)
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
        # font.setBold(True)
        self.title_label.setFont(font)

        self.layout.addWidget(self.title_label)

# 2. Top part. Form
# class FormFrame(BaseFrame):
#     """
#     Frame for 2. Top part: Form.
#     """
#     def __init__(self):
#         super().__init__()
#         self.layout = QHBoxLayout()
#         self.init_gui_a()
#         self.setLayout(self.layout)
#     def __repr__(self) -> str:
#         return "Frame for Form"
#     def init_gui_a(self):
#         """
#         It initializes the GUI: Top 2. part
#         """
#         # 2. Form part
#         # form_layout = QHBoxLayout()
#         self.name_label = QLabel("Input path & name:")
#         self.name_line_edit = QLineEdit()
#         self.name_line_edit.setPlaceholderText("Select a file...")
#         font = self.name_label.font()
#         # print(font.family(), font.pointSize(), font.weight())
#         font.setPointSize(11)
#         # font.setBold(True)
#         self.name_label.setFont(font)
#         font = self.name_line_edit.font()
#         # print(font.family(), font.pointSize(), font.weight())
#         font.setPointSize(11)
#         # font.setBold(True)
#         self.name_line_edit.setFont(font)
#         self.layout.addWidget(self.name_label)
#         self.layout.addWidget(self.name_line_edit)
#         self.browse_button = QPushButton("Browse")
#         self.browse_button.setFixedSize(66, 30)
#         self.browse_button.clicked.connect(self.browse_file)
#         self.layout.addWidget(self.browse_button)
#     def browse_file(self):
#         """
#         Explore the local computer files to choose one as the input of the process
#         """
#         file_name, _ = QFileDialog.getOpenFileName(self, "Select File...") # open win's title
#         if file_name:  # If a file was selected (i.e., the user didn't cancel)
#             # self.lineEdit.setText(file_name)
#             self.name_line_edit.setText(file_name)

# 2. Top part. Forms (Interchanging forms)
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

        self.layout = QVBoxLayout()
        self.init_gui_a()
        self.setLayout(self.layout)
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

        self.form_stack_widget.addWidget(TextForm())
        self.form_stack_widget.addWidget(GenForm())

        self.layout.addWidget(self.form_stack_widget)

    def switch_form_stack_widget(self, switch_button: QPushButton) -> None: # switch_central_widget
        """
        This method switches between Text Input Form and Random Generated Input Form
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

        self.layout = QHBoxLayout()
        # # self.central_widget = QStackedWidget()
        self.init_gui_b()
        # self.switch_central_widget()
        # # self.addWidget(self.central_widget)
        self.setLayout(self.layout)
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

        self.layout.addWidget(self.central_widget)
    def switch_central_widget(self, switch_button: QPushButton) -> None:
        """
        This method switches between Text and Image in the central widget
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

# 4. Bottom part (Buttons)
class ButtonsFrame(BaseFrame):
    """
    Frame for 4. bottom part: Buttons.
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window: MainWindow = main_window
        self.layout = QHBoxLayout()
        # Set the layout margins to 0
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.init_gui_c()
        self.setLayout(self.layout)
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
        # self.layout.addWidget(self.task_button)
        # self.switch_button = QPushButton("Switch to Image (D. GRAPH)") # see it on another place
        # self.switch_button.setFixedSize(200, 30)
        # self.switch_button.clicked.connect(self.main_window.central_frame.switch_central_widget)
        # self.layout.addWidget(self.switch_button)

        # Button placeholders
        self.button_placeholders = [QFrame(self) for _ in range(4)]
        # for placeholder in self.button_placeholders:
        #     placeholder.setFixedHeight(50) # setMaximumHeight
        #     # Optionally set a fixed width or maximum width for the placeholders if needed
        #     # placeholder.setMaximumWidth(100)
        #     # painter = QPainter(placeholder)
        #     # painter.drawRect(placeholder.rect())
        #     # placeholder.drawFrame(painter)

        # Create buttons
        self.button1 = QPushButton("Run Async Search Optim") # "Button 1", self
        self.button2 = QPushButton("Change visibility") # "Button 2"
        self.button3 = QPushButton("Switch Random Gen Input") # "Button 3"
        self.button4 = QPushButton("Switch to Image (D. GRAPH)") # "Button 4"

        # Set a maximum width for buttons
        max_width = 220
        for btn in [self.button1, self.button2, self.button3, self.button4]:
            btn.setMaximumWidth(max_width)
            btn.setFixedHeight(30) # setMaximumHeight

        # # Add buttons to the layout
        # self.mainLayout.addWidget(self.button1)
        # self.mainLayout.addWidget(self.button2)
        # self.mainLayout.addWidget(self.button3)
        # self.mainLayout.addWidget(self.button4)

        # Add buttons to their respective placeholders
        for i, btn in enumerate([self.button1, self.button2, self.button3, self.button4]):
            layout = QHBoxLayout(self.button_placeholders[i])
            # Set the layout margins to 0
            if i == 0:
                layout.setContentsMargins(5, 0, 0, 0)
            elif i == 3:
                layout.setContentsMargins(0, 0, 5, 0)
            layout.addWidget(btn)
            self.layout.addWidget(self.button_placeholders[i])

        # Example event handle I.: Start async task
        self.button1.clicked.connect(self.run_async_task) # task_button

        # Example event handle II.: Hide the second button
        # self.toggleButtonVisibility(self.button3)   # It has no effect here.
        self.button2.clicked.connect(self.toggle_button3_visibility)

        # Example event handle III.: Swich GUI Input FORM
        self.button3.clicked.connect(
            lambda: self.main_window.form_frame.switch_form_stack_widget(self.button3)
        )

        # Example event handle IV.: Swich central part
        self.button4.clicked.connect(
            lambda: self.main_window.central_frame.switch_central_widget(self.button4)
        )

    async def async_task(self):
        """
        It demonstrates the asynchronous tasks
        """
        print("Task solving Directed Disjunctive Graph started")
        self.main_window.print_status("Task solving Directed Disjunctive Graph started")

        await asyncio.sleep(5)
        print("Task completed")
        self.main_window.print_status("...COMPLETED...", -3)

    def run_async_task(self):
        """
        It demonstrates the starting asynchronous tasks
        """
        asyncio.create_task(self.async_task())

    # Example method to toggle button visibility
    def toggle_button3_visibility(self):  # , button
        """
        This method toggle the visibility of button3 for demonstration
        """
        self.button3.setVisible(not self.button3.isVisible())
        # self.button3.hide()
        if self.button3.isVisible():
            self.main_window.print_status("The Button3 is visible...")
            self.main_window.print_status("", 2)
        else:
            self.main_window.print_status("The Button3 disappeared...", -2)
            self.main_window.print_status("...REALLY...", 3)

# 5. Bottom part (Status Info)
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
                        background-color: rgba(0, 0, 0, 30); /* #A0A0A0; gray */
                            /* Semi-transparent white (gray) */
                    }
                    """)
        # self.setMaximumHeight(35) # setFixedHeight
        self.layout = QHBoxLayout()
        # Set the layout margins to 0
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.init_gui_d()
        self.setLayout(self.layout)
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
        self.layout.addWidget(status_bar)

# Main Application Window
class MainWindow(QMainWindow):
    """
    This class represents the GUI interface's view
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ddg Project")
        self.setGeometry(100, 100, 800, 600)

        # Set a central widget with transparent background

        cent_widget = QWidget(self) # stands for l_cent... = QWidget(); self.setLayout(l_cent...)
        self.setCentralWidget(cent_widget)
        cent_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # self.centralWidget

        main_layout = QVBoxLayout()

        # Initialize frames
        self.title_frame = TitleFrame("ddg Project")
        # print(self.title_frame)
        self.form_frame = FormFrame()
        self.central_frame = CentralFrame()
        self.buttons_frame = ButtonsFrame(self)
        self.status_frame = StatusFrame()

        # Add frames to the main_layout
        main_layout.addWidget(self.title_frame)
        main_layout.addWidget(self.form_frame)
        main_layout.addWidget(self.central_frame)
        main_layout.addWidget(self.buttons_frame)
        main_layout.addWidget(self.status_frame)

        cent_widget.setLayout(main_layout)

        # pixmap = QPixmap('src\\gui\\sandbox\\DALL·E 2024-03-11 16.28.47 -  3D __small.webp')
        self.pixmap = QPixmap('src\\gui\\DALL·E 2024-03-11 16.40.08 halvany__small.webp')
        self.redirect_print()

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

    def redirect_print(self) -> None:
        """
        Redirect print statements to QTextEdit
        """
        sys.stdout = QTextEditOutputStream(self.central_frame.text_edit, 1300) # max_char
        # sys.stderr = QTextEditOutputStream(self.text_edit)

    def print_status(self, message: str = "", alaign_nb: int = 0) -> None:
        """
        Print a message into the bottom Status line

        Attributes:
            message   - the text being printed

            aliagn_nb - 0 - Erease any message in the Status line if not message.
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

def dg_gui_main():
    """
    This function is the main runable one of the GUI controlled version of ddg project.
    """
    app = QApplication(sys.argv)
    # mainWindow = MainWindow() // AsyncApp(max_char= 1300)
    # mainWindow.show()
    # sys.exit(app.exec())

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    with loop:
        loop.run_forever()

if __name__ == "__main__":
    dg_gui_main()
