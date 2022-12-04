from PyQt5.QtWidgets import *
import util


class RoomSelect(QDialog, QWidget):

    def click(self):
        bt = QToolButton()
        bt.setText('asd')
        self.mainLayout.addWidget(bt)
        pass

    def __init__(self, parent=None):
        super().__init__(parent)

        self.mainLayout = QVBoxLayout()

        self.mainLayout.setContentsMargins(130, 0, 130, 0)
        self.setGeometry(300, 300, 500, 500)
        util.center(self)
        self.mainLayout.addStretch()
        # QVBoxLayout
        loginLabel = QLabel()
        loginLabel.setText("Room Select")
        button = QToolButton()
        button.setText("online")
        button.clicked.connect(self.click)
        button2 = QToolButton()
        button2.setText("offline")
        button2.clicked.connect(self.click)
        self.mainLayout.addWidget(loginLabel)
        self.mainLayout.addWidget(button)
        self.mainLayout.addWidget(button2)
        self.mainLayout.addStretch()

        self.setLayout(self.mainLayout)
        self.setWindowTitle('십이장기')
