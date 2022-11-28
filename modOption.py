from PyQt5.QtWidgets import *


class ModOption(QDialog, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        mainLayout = QVBoxLayout()
        # QVBoxLayout
        loginLabel = QLabel()
        loginLabel.setText("Option Select")
        id = QLineEdit()
        id.setPlaceholderText("id")
        pw = QLineEdit()
        pw.setPlaceholderText("pw")
        button = QToolButton()
        button.setText("Login")
        # button.clicked.c/onnect(self.click)
        button2 = QToolButton()
        button2.setText("Registration")
        # button2.clicked.connect(self.click)
        mainLayout.addWidget(loginLabel)
        mainLayout.addWidget(id)
        mainLayout.addWidget(pw)
        mainLayout.addWidget(button)
        mainLayout.addWidget(button2)

        self.setLayout(mainLayout)
        self.setWindowTitle('???')
