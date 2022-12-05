import subprocess

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import util
import socket
import requests
import user


class MakeRoom(QDialog, QWidget):
    par = None

    def insertRoom(self):
        # $gid =$_GET["id"];
        # $gnm =$_GET["name"];
        # $sip =$_GET['sip']; // / Socket
        # $gip =$_GET['gip']; // / Group
        return requests.get('http://adteamb.dothome.co.kr/roomInsert.php?'
                            + 'id=' + user.User.id + '&'
                            + 'name=' + self.rname.text() + '&'
                            + 'gip=' + requests.get("http://ip.jsontest.com").json()['ip'] + '&'
                            + 'sid=' + socket.gethostbyname(socket.gethostname())
                            ).text

    def click(self):
        self.close()
        self.insertRoom()
        subprocess.call("py main.py", shell=True)
        pass

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(130, 0, 130, 0)
        self.setGeometry(300, 300, 500, 500)
        util.center(self)
        mainLayout.addStretch()
        # QVBoxLayout
        loginLabel = QLabel()
        loginLabel.setText("MakeRoom")
        self.rname = QLineEdit()
        self.rname.setPlaceholderText("room name")
        button2 = QToolButton()
        button2.setText("create")
        button2.clicked.connect(self.click)
        mainLayout.addWidget(loginLabel)
        mainLayout.addWidget(self.rname)
        mainLayout.addWidget(button2)
        mainLayout.addStretch()

        self.setLayout(mainLayout)
        self.setWindowTitle('십이장기')
