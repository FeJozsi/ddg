"""
This modul demonstrates the GUI for the dgg project.
"""
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTextEdit, QStatusBar, QGraphicsView,
                             QGraphicsScene, QStackedWidget)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt #, QRectF

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("dgg Project GUI") # "Complex Layout Example"
        self.setGeometry(100, 100, 800, 600) # , 600, 400

        self.main_layout = QVBoxLayout(self)

        # Top part
        titleLabel = QLabel("dgg Project") # "Title or Some Labels"
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(titleLabel)

        # Form part
        form_layout = QHBoxLayout()
        nameLabel = QLabel("Name:")
        nameLineEdit = QLineEdit()
        form_layout.addWidget(nameLabel)
        form_layout.addWidget(nameLineEdit)
        self.main_layout.addLayout(form_layout)

        # Central part (QTextEdit or Image) using QStackedWidget
        self.centralWidget = QStackedWidget()
        self.textEdit = QTextEdit()
        self.graphicsView = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        # Load your image (ensure the path is correct)
        pixmap = QPixmap(".\\src\\gui\\Picture 1.png")  # ".\\src\\gui\\sandbox\\Picture 1.png"
        self.scene.clear()  # Clear previous content
        self.scene.addPixmap(pixmap)
        # self.scene.setSceneRect(pixmap.rect())
        # self.scene.setSceneRect(QRectF(pixmap.rect()))
        self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())

        self.centralWidget.addWidget(self.textEdit)
        self.centralWidget.addWidget(self.graphicsView)

        self.main_layout.addWidget(self.centralWidget)

        # Buttons stripe
        buttons_layout = QHBoxLayout()
        self.switchButton = QPushButton("Switch to Image")
        self.switchButton.clicked.connect(self.switch_central_widget)
        buttons_layout.addWidget(self.switchButton)
        self.main_layout.addLayout(buttons_layout)

        # Status stripe
        statusBar = QStatusBar()
        statusBar.showMessage("Status Info")
        self.main_layout.addWidget(statusBar)

    def switch_central_widget(self):
        currentIndex = self.centralWidget.currentIndex()
        if currentIndex == 0:
            self.centralWidget.setCurrentIndex(1)
            self.switchButton.setText("Switch to TextEdit")
            # # Load your image here, if necessary
            # pixmap = QPixmap("path/to/your/image.png")
            # self.scene.clear()
            # self.scene.addPixmap(pixmap)
            # # self.scene.setSceneRect(pixmap.rect())
        else:
            self.centralWidget.setCurrentIndex(0)
            self.switchButton.setText("Switch to Image")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
