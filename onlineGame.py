from PyQt5.QtWidgets import *


class OnlineGame(QDialog, QWidget):

    def click(self):
        pass

    def __init__(self, parent=None):
        super().__init__(parent)

        mainLayout = QVBoxLayout()
        # QVBoxLayout
        loginLabel = QLabel()
        loginLabel.setText("Mod Option Select")
        button = QToolButton()
        button.setText("online")
        button.clicked.connect(self.click)
        button2 = QToolButton()
        button2.setText("offline")
        button2.clicked.connect(self.click)
        mainLayout.addWidget(loginLabel)
        mainLayout.addWidget(button)
        mainLayout.addWidget(button2)

        self.setLayout(mainLayout)
        self.setWindowTitle('???')
