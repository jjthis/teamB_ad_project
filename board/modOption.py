import subprocess

from PyQt5.QtWidgets import *
from selectRoom import RoomSelect
import util


class ModOption(QDialog, QWidget):
    def click(self):
        if self.sender().text() == "online":
            room = RoomSelect(self)
            room.show()
            room.exec_()
        else:
            import main
            main.func()

    def __init__(self, parent=None):
        super().__init__(parent)
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(130, 0, 130, 0)
        self.setGeometry(300, 300, 500, 500)
        util.center(self)
        mainLayout.addStretch()
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
        mainLayout.addStretch()

        self.setLayout(mainLayout)
        self.setWindowTitle('십이장기')
