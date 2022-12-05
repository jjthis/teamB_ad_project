import threading
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
    print(data)
    if data == "start":
        func()
        UserInfo.sendTarget.send("start".encode())
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
        if jangi.turn == ME and UserInfo.move:
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


class Chatting(QWidget):
    socketSignal = pyqtSignal(object)  # must be defined in class level

    def click(self):
        if self.sender().text() == "open":
            #     def binder(client_socket, addr):
            #         # 커넥션이 되면 접속 주소가 나온다.
            #         print('Connected by', addr);
            #         try:
            #             # 접속 상태에서는 클라이언트로 부터 받을 데이터를 무한 대기한다.
            #             # 만약 접속이 끊기게 된다면 except가 발생해서 접속이 끊기게 된다.
            #             while True:
            #                 # socket의 recv함수는 연결된 소켓으로부터 데이터를 받을 대기하는 함수입니다. 최초 4바이트를 대기합니다.
            #                 data = client_socket.recv(4);
            #                 # 최초 4바이트는 전송할 데이터의 크기이다. 그 크기는 little 엔디언으로 byte에서 int형식으로 변환한다.
            #                 length = int.from_bytes(data, "little");
            #                 # 다시 데이터를 수신한다.
            #                 data = client_socket.recv(length);
            #                 # 수신된 데이터를 str형식으로 decode한다.
            #                 msg = data.decode();
            #                 # 수신된 메시지를 콘솔에 출력한다.
            #                 print('Received from', addr, msg);
            #
            #                 # 수신된 메시지 앞에 「echo:」 라는 메시지를 붙힌다.
            #                 msg = "echo : " + msg;
            #                 # 바이너리(byte)형식으로 변환한다.
            #                 data = msg.encode();
            #                 # 바이너리의 데이터 사이즈를 구한다.
            #                 length = len(data);
            #                 # 데이터 사이즈를 little 엔디언 형식으로 byte로 변환한 다음 전송한다.
            #                 client_socket.sendall(length.to_bytes(4, byteorder="little"));
            #                 # 데이터를 클라이언트로 전송한다.
            #                 client_socket.sendall(data);
            #         except:
            #             # 접속이 끊기면 except가 발생한다.
            #             print("except : ", addr);
            #         finally:
            #             # 접속이 끊기면 socket 리소스를 닫는다.
            #             client_socket.close();

            # 소켓을 만든다.
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            # 소켓 레벨과 데이터 형태를 설정한다.
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
            # 서버는 복수 ip를 사용하는 pc의 경우는 ip를 지정하고 그렇지 않으면 None이 아닌 ''로 설정한다.
            # 포트는 pc내에서 비어있는 포트를 사용한다. cmd에서 netstat -an | find "LISTEN"으로 확인할 수 있다.
            print("bind")
            server_socket.bind(('', 9999));
            # server 설정이 완료되면 listen를 시작한다.

            print("listen")
            server_socket.listen();

            try:
                # 서버는 여러 클라이언트를 상대하기 때문에 무한 루프를 사용한다.

                # client로 접속이 발생하면 accept가 발생한다.
                # 그럼 client 소켓과 addr(주소)를 튜플로 받는다.
                client_socket, addr = server_socket.accept();
                print("받음")
                UserInfo.sendTarget = client_socket
                # 쓰레드를 이용해서 client 접속 대기를 만들고 다시 accept로 넘어가서 다른 client를 대기한다.
                th = threading.Thread(target=Server.threaded, args=(client_socket, addr, self.socketSignal))
                th.start()
            except:
                print("server")
            finally:
                # 에러가 발생하면 서버 소켓을 닫는다.
                server_socket.close();
            # func()
            # 서버 IP 및 열어줄 포트
            # HOST = ''
            # PORT = 9991
            #
            # # 서버 소켓 생성
            # print('>> Server Start')
            # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # server_socket.bind((HOST, PORT))
            # server_socket.listen()
            # try:
            #     print('>> Wait')
            #     client_socket, addr = server_socket.accept()
            #     UserInfo.sendTarget = client_socket
            #     start_new_thread(Server.threaded, (client_socket, addr, self.socketSignal))
            #     print("참가자 수 : ", 1)
            # except Exception as e:
            #     print('에러는? : ', e)
            # finally:
            #     server_socket.close()

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
