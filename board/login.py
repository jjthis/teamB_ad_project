from PyQt5.QtWidgets import *
from registration import Registration
from modOption import ModOption
import util
import requests


class LogIn(QDialog, QWidget):

    def login(self, id, pw):
        hashedPW = util.getHash(pw)
        return requests.get('http://adteamb.dothome.co.kr/login.php?id='
                            + id + '&pw=' + hashedPW)

    def click(self):
        if self.sender().text() == "Registration":
            self.hide()
            reg = Registration()
            reg.show()
            reg.exec_()
            self.show()
        else:
            for i in self.id.text():
                if 'a' <= i <= 'z' or 'A' <= i <= 'Z' or '0' <= i <= '9':
                    pass
                else:
                    self.message.setText("아이디로는 숫자와 알파벳만 가능합니다")
                    return
            r = self.login(self.id.text(), self.pw.text())
            if r.content == b'101':
                self.message.setText("존재하지 않는 아이디 입니다.")
            elif r.content == b'102':
                self.message.setText("잘못된 비밀번호 입니다.")
            else:
                self.hide()
                options = ModOption()
                options.show()
                options.exec_()
                # self.show()

    def __init__(self, parent=None):
        super().__init__(parent)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(130, 0, 130, 0)
        self.setGeometry(300, 300, 500, 500)
        util.center(self)
        mainLayout.addStretch()
        # QVBoxLayout
        loginLabel = QLabel()
        loginLabel.setText("Login")
        self.id = QLineEdit()
        self.id.setPlaceholderText("id")
        self.pw = QLineEdit()
        self.pw.setPlaceholderText("pw")
        self.message = QLineEdit()
        self.message.setPlaceholderText("Error Message")
        self.message.setReadOnly(True)
        button = QToolButton()
        button.setText("Login")
        button.clicked.connect(self.click)
        button2 = QToolButton()
        button2.setText("Registration")
        button2.clicked.connect(self.click)
        mainLayout.addWidget(loginLabel)
        mainLayout.addWidget(self.id)
        mainLayout.addWidget(self.pw)
        mainLayout.addWidget(self.message)
        mainLayout.addWidget(button)
        mainLayout.addWidget(button2)
        mainLayout.addStretch()

        self.setLayout(mainLayout)
        self.setWindowTitle('십이장기')
