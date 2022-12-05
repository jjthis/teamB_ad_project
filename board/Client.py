import socket
from _thread import *


# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리
from PyQt5.QtWidgets import QToolButton


def recv_data(client_socket, ui):
    while True:
        data = client_socket.recv(1024)

        print("recive : ", repr(data.decode()))
        ui.emit(data.decode())
