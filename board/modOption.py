from PyQt5.QtWidgets import *
from selectRoom import RoomSelect
from offlineGame import OfflineGame

class ModOption(QDialog, QWidget):

    def click(self):
        if self.sender().text() == "online":
            self.hide()
            room = RoomSelect()
            room.show()
            room.exec()
            self.show()
        else:
            self.hide()
            game = OfflineGame()
            game.show()
            game.exec()
            self.show()

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
