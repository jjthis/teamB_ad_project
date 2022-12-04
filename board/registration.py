from PyQt5.QtWidgets import *
import util
import requests


class Registration(QDialog, QWidget):
    def regi(self, id, pw):
        hashedPW = util.getHash(pw)
        return requests.get('http://adteamb.dothome.co.kr/registration.php?id='
                            + id + '&pw=' + hashedPW)

    def click(self):
        for i in self.id.text():
            if 'a' <= i <= 'z' or 'A' <= i <= 'Z' or '0' <= i <= '9':
                pass
            else:
                self.message.setText("아이디로는 숫자와 알파벳만 가능합니다")
                return
        r = self.regi(self.id.text(), self.pw.text())
        if r.content == b'100':
            self.message.setText("이미 있는 아이디 입니다.")
        else:
            self.message.setText("회원가입이 완료되었습니다.")

    def __init__(self, parent=None):
        super().__init__(parent)

        mainLayout = QVBoxLayout()
        # QVBoxLayout
        loginLabel = QLabel()
        loginLabel.setText("Registration")
        self.id = QLineEdit()
        self.id.setPlaceholderText("id")
        self.pw = QLineEdit()
        self.pw.setPlaceholderText("pw")
        self.message = QLineEdit()
        self.message.setPlaceholderText("Error Message")
        self.message.setReadOnly(True)
        button = QToolButton()
        button.setText("register")
        button.clicked.connect(self.click)
        mainLayout.addWidget(loginLabel)
        mainLayout.addWidget(self.id)
        mainLayout.addWidget(self.pw)
        mainLayout.addWidget(self.message)
        mainLayout.addWidget(button)

        self.setLayout(mainLayout)
        self.setWindowTitle('???')
