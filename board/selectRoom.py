import subprocess

import requests
import json

import user
from makeRoom import MakeRoom

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import util


class RoomSelect(QDialog):
    roomList = []

    def click(self):
        if self.sender().text() == "refresh":
            self.makeList()
        elif self.sender().text() == "select":
            pos = self.lis.currentRow()
            if pos == -1:
                return
            import client_game
            import userInfo
            userInfo.UserInfo.socketIP = self.roomList[pos]['SocketIP']
            room = client_game.Chatting(self)
            room.show()
            room.exec_()

        else:
            # self.hide()
            room = MakeRoom(self.par)
            room.show()
            room.exec()
            self.makeList()
        pass

    def getRoomList(self):
        return json.loads(str(requests.get('http://adteamb.dothome.co.kr/roomList.php').text))

    def makeList(self):
        self.lis.clear()
        self.roomList = self.getRoomList()[1:]
        # print(self.roomList)
        for i in self.roomList:
            self.lis.addItem(i['name'] + "\nOwner: " + i['userID'])

    def __init__(self, parent=None):
        super().__init__(parent)
        self.par = parent
        self.setWindowModality(Qt.ApplicationModal)
        self.mainLayout = QVBoxLayout()

        self.mainLayout.setContentsMargins(130, 0, 130, 0)
        self.setGeometry(300, 300, 500, 500)
        util.center(self)
        self.mainLayout.addStretch()
        # QVBoxLayout
        self.lis = QListWidget()
        self.makeList()
        loginLabel = QLabel()
        loginLabel.setText("Room Select")
        blay = QHBoxLayout()
        button = QToolButton()
        button.setText("refresh")
        button.setFixedHeight(50)
        button.setSizePolicy(QSizePolicy.Expanding, 0)
        button.clicked.connect(self.click)
        button2 = QToolButton()
        button2.setText("select")
        button2.setFixedHeight(50)
        button2.clicked.connect(self.click)
        button2.setSizePolicy(QSizePolicy.Expanding, 0)
        button3 = QToolButton()
        button3.setText("makeRoom")
        button3.setFixedHeight(50)
        button3.clicked.connect(self.click)
        button3.setSizePolicy(QSizePolicy.Expanding, 0)
        self.mainLayout.addWidget(loginLabel)
        self.mainLayout.addWidget(self.lis)
        blay.addWidget(button)
        blay.addWidget(button2)
        self.mainLayout.addLayout(blay)
        self.mainLayout.addWidget(button3)
        self.mainLayout.addStretch()

        self.setLayout(self.mainLayout)
        self.setWindowTitle('십이장기')
