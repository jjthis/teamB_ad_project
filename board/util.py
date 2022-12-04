import hashlib

from PyQt5.QtWidgets import QDesktopWidget


def getHash(strs):
    return hashlib.md5(("adProject&@*^%*!($" + strs + "aja&5^4$&2&!abhk").encode('utf-8')).hexdigest()

def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())