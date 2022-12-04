from PyQt5.QtWidgets import *


class RoomSelect(QDialog, QWidget):

    def click(self):
        bt = QToolButton()
        bt.setText('asd')
        self.mainLayout.addWidget(bt)
        pass

    def __init__(self, parent=None):
        super().__init__(parent)

        self.mainLayout = QVBoxLayout()
        # QVBoxLayout
        loginLabel = QLabel()
        loginLabel.setText("Mod Option Select")
        button = QToolButton()
        button.setText("online")
        button.clicked.connect(self.click)
        button2 = QToolButton()
        button2.setText("offline")
        button2.clicked.connect(self.click)
        self.mainLayout.addWidget(loginLabel)
        self.mainLayout.addWidget(button)
        self.mainLayout.addWidget(button2)

        self.setLayout(self.mainLayout)
        self.setWindowTitle('???')
