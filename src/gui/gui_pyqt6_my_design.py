"""
This modul demonstrates the GUI for the ddg project
and its asynchronous behaviors.
"""
# pylint: disable="R0801" # : Similar lines in 2 files
import sys
import asyncio

from PyQt6.QtWidgets import (QTextEdit, QWidget, QPushButton, QVBoxLayout, QLabel,
                             QHBoxLayout, QLineEdit, QStackedWidget, QGraphicsView, QGraphicsScene,
                             QStatusBar, QApplication, QFileDialog, QMainWindow)
from PyQt6.QtGui import QTextCursor, QPixmap, QPainter #, QColor, QFont
from PyQt6.QtCore import Qt #, QRectF

import qasync # type: ignore

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

class AsyncApp(QMainWindow):  # QWidget
    """
    This class represents the GUI interface
    and the asynchronous behaviors of the template program
    """
    def __init__(self, max_char: int):
        super().__init__()

        # self.setWindowTitle('Async PyQt Example')
        # self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle("ddg Project GUI") # "Complex Layout Example"
        self.setGeometry(100, 100, 800, 600) # , 600, 400

        # self.opacity = 0.7  # Set the desired opacity level (0.0 transparent through 1.0 opaque)

        # Set a central widget with transparent background
        l_cent_widget = QWidget(self) # self.centralWidget
        self.setCentralWidget(l_cent_widget) # self.centralWidget
        l_cent_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # self.centralWidget

        # self.main_layout = QVBoxLayout(self) # stands for self.setLayout(self.main_layout)
        self.main_layout = QVBoxLayout()
        self.init_gui_a()
        self.init_gui_b()
        self.init_gui_c()
        self.init_gui_d(max_char)

        l_cent_widget.setLayout(self.main_layout) # self.centralWidget

    def paintEvent(self, _): # event  # pylint: disable=C0103
        """
        This method draws the backgroud picture
        This method over-writes the QMainWindow's one.
        """
        painter = QPainter(self)
        # pixmap = QPixmap('src\\gui\\sandbox\\DALL·E 2024-03-11 16.28.47 -  3D __small.webp')
        pixmap = QPixmap('src\\gui\\DALL·E 2024-03-11 16.40.08 halvany__small.webp')

        painter.drawPixmap(self.rect(), pixmap)

        # Apply semi-transparent overlay
        # painter.setOpacity(self.opacity)  # Apply the opacity level
        # painter.setBrush(QColor(0, 0, 0, 127)) # A semi-transparent overlay: 27 light, 227 dark
        # painter.setPen(Qt.PenStyle.NoPen)  # No border
        painter.drawRect(self.rect())  # Draw the overlay


    def init_gui_a(self):
        """
        It initializes the GUI: Top (1.-2.) parts
        """
        # 1. Top part
        # "Title or Some Labels"
        title_label = QLabel("ddg Project – skeleton showing simulated actions")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = title_label.font()
        # print(font.family(), font.pointSize(), font.weight())
        font.setPointSize(14)
        # font.setBold(True)
        title_label.setFont(font)

        self.main_layout.addWidget(title_label)

        # 2. Form part
        form_layout = QHBoxLayout()
        name_label = QLabel("Input path & name:")
        self.name_line_edit = QLineEdit()
        self.name_line_edit.setPlaceholderText("Select a file...")
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_line_edit)

        browse_button = QPushButton("Browse")
        browse_button.setFixedSize(66, 30)
        browse_button.clicked.connect(self.browse_file)
        form_layout.addWidget(browse_button)

        self.main_layout.addLayout(form_layout)

    def init_gui_b(self):
        """
        It initializes the GUI: Central (3.) part
        """
        # Central part (QTextEdit or Image) using QStackedWidget
        self.central_widget = QStackedWidget()
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

        self.main_layout.addWidget(self.central_widget)

    def init_gui_c(self):
        """
        It initializes the GUI: Bottom (4., 5.) parts
        """
        # Buttons stripe
        buttons_layout = QHBoxLayout() # layout = QVBoxLayout(self)
        self.task_button = QPushButton('Run Async Search Optim') # here without parent= self param.
        self.task_button.setFixedSize(200, 30)
        self.task_button.clicked.connect(self.run_async_task)
        buttons_layout.addWidget(self.task_button)
        self.switch_button = QPushButton("Switch to Image (D. GRAPH)") # see it on another place
        self.switch_button.setFixedSize(200, 30)
        self.switch_button.clicked.connect(self.switch_central_widget)
        buttons_layout.addWidget(self.switch_button)
        self.main_layout.addLayout(buttons_layout) # stands for ...setLayout...

        # Status stripe
        status_bar = QStatusBar()
        font = status_bar.font()
        # print(font.family(), font.pointSize(), font.weight())
        font.setPointSize(11)
        # font.setBold(True)
        status_bar.setFont(font)
        # print(font.family(), font.pointSize(), font.weight())
        status_bar.showMessage("Status Info")
        self.main_layout.addWidget(status_bar)

    def init_gui_d(self, max_char: int):
        """
        Redirect print statements to QTextEdit
        """

        # Redirect print statements to QTextEdit
        sys.stdout = QTextEditOutputStream(self.text_edit, max_char) # type: ignore
        # sys.stderr = QTextEditOutputStream(self.text_edit)

    def browse_file(self):
        """
        Explore the local computer files to choose one as the input of the process
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File...") # open win's title
        if file_name:  # If a file was selected (i.e., the user didn't cancel)
            # self.lineEdit.setText(file_name)
            self.name_line_edit.setText(file_name)

    def switch_central_widget(self):
        """
        This method switches between Text and Image in the central widget
        """
        current_index = self.central_widget.currentIndex()
        if current_index == 0:
            self.central_widget.setCurrentIndex(1)
            self.switch_button.setText("Switch to TextEdit (STDOUT)")
            # # Load your image here, if necessary
            # pixmap = QPixmap("path/to/your/image.png")
            # self.scene.clear()
            # self.scene.addPixmap(pixmap)
            # # self.scene.setSceneRect(pixmap.rect())
        else:
            self.central_widget.setCurrentIndex(0)
            self.switch_button.setText("Switch to Image (D. GRAPH)")

    async def async_task(self):
        """
        It demonstrates the asynchronous tasks
        """
        print("Task solving Directed Disjunctive Graph started")
        await asyncio.sleep(5)
        print("Task completed")

    def run_async_task(self):
        """
        It demonstrates the starting asynchronous tasks
        """
        asyncio.create_task(self.async_task())


def main():
    """
    This function is the main runable one of the GUI controlled version of ddg project.
    """
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = AsyncApp(max_char= 1300)
    window.show()

    with loop:
        loop.run_forever()

if __name__ == '__main__':
    main()
