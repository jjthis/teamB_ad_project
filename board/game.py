from PyQt5.QtWidgets import *
from login import LogIn
from makeRoom import MakeRoom
from selectRoom import RoomSelect

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    log = LogIn()
    log.show()
    app.exec_()
