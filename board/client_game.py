from _thread import start_new_thread
from time import sleep
import socket
import Server

import requests
import json
from makeRoom import MakeRoom

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import util

from jangi_const import *
from jangi import *
import pygame


class UserInfo:
    sendTarget = None
    move = False
    moveCmd = {}


def executeOnMain(data):
    if data == "start":
        func()
        return
    data = json.loads(data)
    if data['cmd'] == 'move':
        UserInfo.move = True
        UserInfo.moveCmd = data
        pass


def func():
    jangi = Jangi()
    jangi.print_board()
    print('Turn:', jangi.turn)
    jangi.turn = YOU


    # 텍스트 디스플레이 함수
    def draw_text(txt, size, pos, color):
        font = pygame.font.Font('freesansbold.ttf', size)
        r = font.render(txt, True, color)
        jangi.display.SURFACE.blit(r, pos)

    pygame.init()
    pygame.display.set_caption("십이장기")
    clock = pygame.time.Clock()
    FPS = 60
    sound_move = pygame.mixer.Sound(JANGI_SOUND_MOVE)
    pygame.mixer.music.load(JANGI_SOUND_BGM)
    pygame.mixer.music.play(-1)
    #  게임 종료
    gameover = False
    gamewin = False
    gamedefeated = False
    while jangi.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jangi.running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    jangi.input.mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if jangi.input.mouse_pressed:
                    jangi.input.mouse_clicked = True
                    jangi.input.mouse_pressed = False
                    jangi.input.mx, jangi.input.my = pygame.mouse.get_pos()
                else:
                    jangi.input.mouse_clicked = False
        if jangi.input.mouse_clicked:
            jangi.input.mouse_clicked = False
            print(jangi.input.mx, jangi.input.my)
            if (
                    JANGI_BOARD_PADDING <= jangi.input.mx and jangi.input.mx <= JANGI_BOARD_PADDING + 3 * JANGI_BOARD_CELL_PIXELS) and (
                    JANGI_BOARD_PADDING <= jangi.input.my and jangi.input.my <= JANGI_BOARD_PADDING + 4 * JANGI_BOARD_CELL_PIXELS):
                isValid, mi, mj = jangi.posPixel2Num(JANGI_BOARD_PADDING, JANGI_BOARD_PADDING, jangi.input.mx,
                                                     jangi.input.my, JANGI_BOARD_CELL_PIXELS)
                # print(isValid, mi, mj)
                if not isValid:
                    jangi.input.mouse_pressed = False
                    is_src_set = False
                    is_target_set = False
                    continue
                else:
                    # print(isValid, mi, mj)
                    if not jangi.input.is_src_set:
                        src_i, src_j = (mi, mj)
                        jangi.input.src_rect = (mj * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING,
                                                mi * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING,
                                                JANGI_BOARD_CELL_PIXELS,
                                                JANGI_BOARD_CELL_PIXELS)
                        jangi.input.src_piece_type = jangi.get_cell(mi, mj)
                        jangi.input.is_src_set = True
                    else:
                        target_i, target_j = (mi, mj)
                        jangi.input.target_rect = (mj * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING,
                                                   mi * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING,
                                                   JANGI_BOARD_CELL_PIXELS, JANGI_BOARD_CELL_PIXELS)
                        jangi.input.target_piece_type = jangi.get_cell(mi, mj)
                        jangi.input.is_target_set = True
                # 조건을 만족했을 때 이동
                if jangi.turn == '[' and jangi.input.is_src_set and jangi.input.is_target_set and jangi.is_alreadyIn(
                        src_i, src_j, target_i,
                        target_j):
                    print("From:", src_i, src_j, "/ To:", target_i, target_j)
                    jangi.move(src_i, src_j, target_i, target_j)  # 3,2

                    UserInfo.sendTarget.send(json.dumps({"cmd": "move",
                                                         "scr_i": 3 - src_i,
                                                         "scr_j": 2 - src_j,
                                                         "target_i": 3 - target_i,
                                                         "target_j": 2 - target_j}))
                    jangi.input.is_src_set = False
                    jangi.input.is_target_set = False
                    jangi.print_board()
                    sound_move.play()
                    print('Turn:', jangi.turn)
                    print('--------------------------------')
        if jangi.turn == ']' and UserInfo.move:
            src_i = UserInfo.moveCmd['src_i']
            src_j = UserInfo.moveCmd['src_j']
            target_i = UserInfo.moveCmd['target_i']
            target_j = UserInfo.moveCmd['target_j']
            UserInfo.move = False
            print("From:", src_i, src_j, "/ To:", target_i, target_j)
            jangi.move(src_i, src_j, target_i, target_j)  # 3,2
            UserInfo.sendTarget.send(json.dumps({"cmd": "move",
                                                 "scr_i": 3 - src_i,
                                                 "scr_j": 2 - src_j,
                                                 "target_i": 3 - target_i,
                                                 "target_j": 2 - target_j}))
            jangi.input.is_src_set = False
            jangi.input.is_target_set = False
            jangi.print_board()
            sound_move.play()
            print('Turn:', jangi.turn)
            print('--------------------------------')

        # 턴 당 시간초 디스플레이
        remainingTime = 100 - (time.time() - jangi.start_time)
        txt = f"Time: {remainingTime:.1f}"
        jangi.display.SURFACE.fill((100, 100, 100))
        draw_text(txt, 32, (10, 10), (255, 255, 255))
        # 아이템 디스플레이
        jangi.display.SURFACE.blit(jangi.display.img_item_time, (
            0 * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING, 4 * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING + 25))
        jangi.display.SURFACE.blit(jangi.display.img_item_mulligan, (
            2 * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING, 4 * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING + 25))
        # drawing the board
        for i in range(4):
            for j in range(3):
                rect = (
                    j * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING,
                    i * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING,
                    JANGI_BOARD_CELL_PIXELS, JANGI_BOARD_CELL_PIXELS)
                pygame.draw.rect(jangi.display.SURFACE, (240, 217, 183), rect, 0)
                if i == 0:
                    pygame.draw.rect(jangi.display.SURFACE, (230, 80, 80), rect, 0)
                elif i == 3:
                    pygame.draw.rect(jangi.display.SURFACE, (129, 183, 71), rect, 0)
                pygame.draw.rect(jangi.display.SURFACE, (50, 50, 50), rect, 1)
        if jangi.input.is_src_set:
            pygame.draw.rect(jangi.display.SURFACE, JANGI_PIECE_SRC_COLOR, jangi.input.src_rect, 5)
        elif jangi.input.is_target_set:  # 옮길 위치에 색깔 표시, 기능 안함, 원인 찾아야함
            pygame.draw.rect(jangi.display.SURFACE, JANGI_PIECE_TARGET_COLOR, jangi.input.target_rect, 5)

        # drawing the pieces
        for N in range(4):
            for M in range(3):
                cell_team = jangi.get_cell(N, M)[0]
                cell_type = jangi.get_cell(N, M)[1]
                sprite_num = -1
                if cell_type == JA:
                    sprite_num = 0
                elif cell_type == SANG:
                    sprite_num = 1
                elif cell_type == WANG:
                    sprite_num = 2
                elif cell_type == JANG:
                    sprite_num = 3

                if cell_team == ME:
                    jangi.display.SURFACE.blit(jangi.display.me_piece_list[sprite_num],
                                               (M * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING + 10,
                                                N * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING + 10))
                elif cell_team == YOU:
                    jangi.display.SURFACE.blit(jangi.display.you_piece_list[sprite_num],
                                               (M * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING + 10,
                                                N * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING + 10))

        if remainingTime <= 0:
            gameover = True
        if gameover:
            jangi.display.SURFACE.fill((100, 100, 100))
            draw_text("GAME OVER", 50, (JANGI_BOARD_SIZE_G / 2 - 150, JANGI_BOARD_SIZE_S / 2 - 275), (255, 255, 255))
            # remainingTime

        pygame.display.update()
        clock.tick(FPS)  # 초당 프레임 조정
    # sleep(2000)
    pygame.quit()


import Client


class Chatting(QWidget):
    socketSignal = pyqtSignal(object)  # must be defined in class level

    def click(self):
        if self.sender().text() == "open":
            # func()
            # 서버 IP 및 열어줄 포트
            HOST = '127.0.0.1'
            PORT = 9999

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))

            start_new_thread(Client.recv_data, (client_socket, self.socketSignal))
            print('>> Connect Server')
            UserInfo.sendTarget = client_socket
            UserInfo.sendTarget.send(str("start").encode())


    def __init__(self, parent=None):
        super().__init__(parent)

        self.socketSignal.connect(executeOnMain)
        self.setWindowModality(Qt.ApplicationModal)
        self.mainLayout = QVBoxLayout()

        self.mainLayout.setContentsMargins(130, 0, 130, 0)
        self.setGeometry(300, 300, 500, 500)
        util.center(self)
        self.mainLayout.addStretch()
        # QVBoxLayout
        self.lis = QListWidget()
        # self.makeList()
        blay = QHBoxLayout()
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Message")
        button = QToolButton()
        button.setText("push")
        button.setFixedHeight(50)
        button.setSizePolicy(QSizePolicy.Expanding, 0)
        button.clicked.connect(self.click)
        button2 = QToolButton()
        button2.setText("open")
        button2.setFixedHeight(50)
        button2.setSizePolicy(QSizePolicy.Expanding, 0)
        button2.clicked.connect(self.click)
        self.mainLayout.addWidget(button2)
        self.mainLayout.addWidget(self.lis)
        blay.addWidget(self.edit)
        blay.addWidget(button)
        self.mainLayout.addLayout(blay)
        self.mainLayout.addStretch()

        self.setLayout(self.mainLayout)
        self.setWindowTitle('십이장기')


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    log = Chatting()
    log.show()
    app.exec_()
