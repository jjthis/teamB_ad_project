from PyQt5.QtWidgets import *
from login import LogIn
from selectRoom import RoomSelect
from PyQt5.uic.properties import QtWidgets

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    log = LogIn()
    log.show()
    app.exec_()
