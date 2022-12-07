import threading
from _thread import start_new_thread
from time import sleep
import socket
import Server
import asyncio
import requests
import json
from makeRoom import MakeRoom

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import util

from jangi_const import *
from jangi import *
import pygame

from userInfo import UserInfo


def executeOnMain(data):
    print(data)
    data = json.loads(data)
    if data['cmd'] == "start":
        UserInfo.sendTarget.send(json.dumps({"cmd": "start", "id": UserInfo.id}).encode())
        func()
        return
    elif data['cmd'] == 'move':
        UserInfo.move = True
        UserInfo.moveCmd = data
        pass
    elif data['cmd'] == 'chat':
        UserInfo.chat.addItem(data['id'] + ': ' + data['data'])
    elif data['cmd'] == 'poro':
        UserInfo.poro = True
        UserInfo.poroCmd = data

def func():
    jangi = Jangi()
    jangi.print_board()
    jangi.print_poro_board()

    # jangi.turn = YOU
    print('Turn:', jangi.turn)

    # 텍스트 디스플레이 함수
    def draw_text(txt, size, pos, color):
        font = pygame.font.Font('freesansbold.ttf', size)
        r = font.render(txt, True, color)
        jangi.display.SURFACE.blit(r, pos)

    isEnd = False
    pygame.init()
    pygame.display.set_caption("십이장기")
    clock = pygame.time.Clock()
    FPS = 60
    sound_move = pygame.mixer.Sound(JANGI_SOUND_MOVE)
    pygame.mixer.music.load(JANGI_SOUND_BGM)
    pygame.mixer.music.play(-1)
    #  게임 종료
    gameover = False
    porocheck = False
    porocheck2 = False
    defeated = ""
    # now_turn = -1

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
            # porocheck = False
            # porocheck2 = False
            print(jangi.input.mx, jangi.input.my)
            if (((JANGI_BOARD_PADDING - JANGI_BOARD_CELL_PIXELS <= jangi.input.mx  # 포로 보드 위치에 따라 수정필요
                  and
                  jangi.input.mx <= JANGI_BOARD_PADDING + 4 * JANGI_BOARD_CELL_PIXELS) and (
                         JANGI_BOARD_PADDING <= jangi.input.my
                         and
                         jangi.input.my <= JANGI_BOARD_PADDING + 4 * JANGI_BOARD_CELL_PIXELS))):
                # or
                # ((jangi.input.mx >= 10 and jangi.input.mx <= 150) or (jangi.input.my >= 110 and jangi.input.my <= 550))):

                isValid, mi, mj = jangi.posPixel2Num(JANGI_BOARD_PADDING, JANGI_BOARD_PADDING, jangi.input.mx,
                                                     jangi.input.my, JANGI_BOARD_CELL_PIXELS)
                print(isValid, mi, mj)
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
                        if (((JANGI_BOARD_PADDING <= jangi.input.mx  # 포로 보드 위치에 따라 수정필요
                              and
                              jangi.input.mx <= JANGI_BOARD_PADDING + 3 * JANGI_BOARD_CELL_PIXELS) and (
                                     JANGI_BOARD_PADDING <= jangi.input.my
                                     and
                                     jangi.input.my <= JANGI_BOARD_PADDING + 4 * JANGI_BOARD_CELL_PIXELS))):
                            jangi.input.src_piece_type = jangi.get_cell(mi, mj)
                            porocheck = False
                        # 결국에 겟셀이 문제(board에서 가져오기 때문, 근데 포로보드를 쓰기때문에 인덱스가 다름) 그럼 왼쪽은 왜 됨?
                        # -1 로 인식해서 뒤에서 첫번째src_piece_type 껄 가져오고 있음
                        # 결국에 되긴되지만 잘못된 값을 가져온다는 것, 즉 수정 필요.
                        # 이 부분은 이프문으로 따로 빼서 포로겟셀 함수 사용
                        else:
                            print("mi, mj: ", mi, mj)
                            print("src_i, src_j: ", src_i, src_j)
                            if mj == -1:
                                src_j = 0
                            elif mj == 3:
                                src_j = 1
                            print("src_i, src_j: ", src_i, src_j)
                            jangi.input.src_piece_type = jangi.poro_get_cell(src_i, src_j)
                            porocheck = True
                        jangi.input.is_src_set = True

                        # print(jangi.input.src_rect)
                        # print("src_piece_type: ",jangi.input.src_piece_type)
                    else:
                        target_i, target_j = (mi, mj)
                        jangi.input.target_rect = (mj * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING,
                                                   mi * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING,
                                                   JANGI_BOARD_CELL_PIXELS, JANGI_BOARD_CELL_PIXELS)
                        if (((JANGI_BOARD_PADDING <= jangi.input.mx  # 포로 보드 위치에 따라 수정필요
                              and
                              jangi.input.mx <= JANGI_BOARD_PADDING + 3 * JANGI_BOARD_CELL_PIXELS) and (
                                     JANGI_BOARD_PADDING <= jangi.input.my
                                     and
                                     jangi.input.my <= JANGI_BOARD_PADDING + 4 * JANGI_BOARD_CELL_PIXELS))):
                            jangi.input.target_piece_type = jangi.get_cell(mi, mj)
                            porocheck2 = True
                            # true false
                            # false false

                            # false false
                            # true true
                        else:
                            if mj == -1:
                                target_j = 0
                            elif mj == 3:
                                target_j = 1
                            jangi.input.src_piece_type = jangi.poro_get_cell(target_i, target_j)
                            porocheck2 = False
                        jangi.input.is_target_set = True
                        # porocheck = False
                        # porocheck2 = False
                # 조건을 만족했을 때 이동 # 이 아래에서 포로 오류, alreadyin이 또 겟셀을 이용하기 때문 포로는 얼레디인 필요없을듯
                # 얼레디인을 트루로 쓰기

                # 포로 #(포로보드->포로보드)만 실행됨 (포로보드->게임보드)만 실행되게 해야함
                # 포로체크 이용해서 조건 구현
                print("porocheck: ", porocheck)
                print("porocheck2: ", porocheck2)
                if jangi.turn == ME and jangi.input.is_src_set and jangi.input.is_target_set and porocheck and porocheck2:
                    print('poroin_pre')
                    jangi.poro_in(src_i, src_j, target_i, target_j)
                    UserInfo.sendTarget.send(json.dumps({"cmd": "poro",
                                                         "src_i": src_i,
                                                         "src_j": 1-src_j,
                                                         "target_i": 3 - target_i,
                                                         "target_j": 2 - target_j}).encode())
                    print('poroin_aft')
                    jangi.input.is_src_set = False
                    jangi.input.is_target_set = False
                    jangi.print_board()
                    jangi.print_poro_board()
                    sound_move.play()
                    print('Turn:', jangi.turn)
                    print(jangi.turn_count)
                    print(jangi.now_turn)
                    print('--------------------------------')
                elif jangi.input.is_src_set and jangi.input.is_target_set and porocheck and porocheck2 == False:
                    continue
                elif jangi.input.is_src_set and jangi.input.is_target_set and porocheck == False and porocheck2 == False:
                    continue
                # 말움직임
                elif jangi.turn == ME and jangi.input.is_src_set and jangi.input.is_target_set and jangi.is_alreadyIn(
                        src_i, src_j, target_i,
                        target_j):
                    print("From:", src_i, src_j, "/ To:", target_i, target_j)
                    jangi.move(src_i, src_j, target_i, target_j)
                    UserInfo.sendTarget.send(json.dumps({"cmd": "move",
                                                         "src_i": 3 - src_i,
                                                         "src_j": 2 - src_j,
                                                         "target_i": 3 - target_i,
                                                         "target_j": 2 - target_j}).encode())
                    jangi.input.is_src_set = False
                    jangi.input.is_target_set = False
                    jangi.print_board()
                    jangi.print_poro_board()
                    sound_move.play()
                    print('Turn:', jangi.turn)
                    print(jangi.turn_count)
                    print(jangi.now_turn)
                    print('--------------------------------')

                # porocheck = False
                # porocheck2 = False
        if jangi.turn == YOU and UserInfo.move:
            src_i = UserInfo.moveCmd['src_i']
            src_j = UserInfo.moveCmd['src_j']
            target_i = UserInfo.moveCmd['target_i']
            target_j = UserInfo.moveCmd['target_j']
            UserInfo.move = False
            print("dnhssssssssssssssssssssFrom:", src_i, src_j, "/ To:", target_i, target_j)
            jangi.move(src_i, src_j, target_i, target_j)
            jangi.input.is_src_set = False
            jangi.input.is_target_set = False
            jangi.print_board()
            jangi.print_poro_board()
            sound_move.play()
            print('Turn:', jangi.turn)
            print(jangi.turn_count)
            print(jangi.now_turn)
            print('--------------------------------')
        if jangi.turn == YOU and UserInfo.poro:
            src_i = UserInfo.poroCmd['src_i']
            src_j = UserInfo.poroCmd['src_j']
            target_i = UserInfo.poroCmd['target_i']
            target_j = UserInfo.poroCmd['target_j']
            UserInfo.poro = False
            print('poroin_pre')
            jangi.poro_in(src_i, src_j, target_i, target_j)
            print('poroin_aft')
            jangi.input.is_src_set = False
            jangi.input.is_target_set = False
            jangi.print_board()
            jangi.print_poro_board()
            sound_move.play()
            print('Turn:', jangi.turn)
            print(jangi.turn_count)
            print(jangi.now_turn)
            print('--------------------------------')

        # 턴 당 시간초 디스플레이
        remainingTime = 90 - (time.time() - jangi.start_time)
        txt = f"Time: {remainingTime:.1f}"
        # 텍스트 디스플레이
        if jangi.turn == "]":
            turn = "My turn"
            rgb = (129, 183, 71)
        else:
            turn = "Opponent turn"
            rgb = (230, 80, 80)
        txt2 = f"{turn}"
        txt3 = "My poro"
        txt4 = "Opponent poro"
        if defeated == ']':
            a = 'Green Team'
            b = 'Red Team'
        elif defeated == '[':
            a = 'Red Team'
            b = 'Green Team'
        else:
            a = ''
            b = ''
        txt5_pre = "Loser: "
        txt6_pre = "Winner: "
        txt5 = a
        txt6 = b

        jangi.display.SURFACE.fill((100, 100, 100))
        draw_text(txt, 32, (10, 10), (255, 255, 255))
        draw_text(txt2, 25, (10, 45), rgb)
        draw_text(txt3, 20, (60, 125), (200, 200, 200))
        draw_text(txt4, 20, (420, 125), (200, 200, 200))
        # 아이템 디스플레이
        # jangi.display.SURFACE.blit(jangi.display.img_item_time, (0*JANGI_BOARD_CELL_PIXELS+JANGI_BOARD_PADDING, 4*JANGI_BOARD_CELL_PIXELS+JANGI_BOARD_PADDING+25))
        # jangi.display.SURFACE.blit(jangi.display.img_item_mulligan, (2*JANGI_BOARD_CELL_PIXELS+JANGI_BOARD_PADDING, 4*JANGI_BOARD_CELL_PIXELS+JANGI_BOARD_PADDING+25))
        # drawing the poro board
        for i in range(4):  # me
            rect = (JANGI_BOARD_PADDING - JANGI_BOARD_CELL_PIXELS, i * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING,
                    JANGI_BOARD_CELL_PIXELS, JANGI_BOARD_CELL_PIXELS)
            pygame.draw.rect(jangi.display.SURFACE, (214, 198, 182), rect, 0)
            pygame.draw.rect(jangi.display.SURFACE, (71, 102, 50), rect, 7)
        for i in range(4):  # you
            rect = (
                JANGI_BOARD_PADDING + 3 * JANGI_BOARD_CELL_PIXELS, i * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING,
                JANGI_BOARD_CELL_PIXELS, JANGI_BOARD_CELL_PIXELS)
            pygame.draw.rect(jangi.display.SURFACE, (214, 198, 182), rect, 0)
            pygame.draw.rect(jangi.display.SURFACE, (152, 0, 50), rect, 7)
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
                cell_team = jangi.get_cell(N, M)[0]  # 차라리 piecenum 이용
                cell_type = jangi.get_cell(N, M)[1]  # 왕 죽은거 판단? 좌표를 알아야되므로 별로임
                sprite_num = -1
                if cell_type == JA:
                    sprite_num = 0
                elif cell_type == SANG:
                    sprite_num = 1
                elif cell_type == WANG:
                    sprite_num = 2
                elif cell_type == JANG:
                    sprite_num = 3
                elif cell_type == HU:
                    sprite_num = 4

                if cell_team == ME:
                    jangi.display.SURFACE.blit(jangi.display.me_piece_list[sprite_num],
                                               (M * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING + 10,
                                                N * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING + 10))
                elif cell_team == YOU:
                    jangi.display.SURFACE.blit(jangi.display.you_piece_list[sprite_num],
                                               (M * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING + 10,
                                                N * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING + 10))
        for N in range(4):
            for M in range(2):
                cell_team = jangi.poro_get_cell(N, M)[0]
                cell_type = jangi.poro_get_cell(N, M)[1]
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
                                               (10 + JANGI_BOARD_PADDING - JANGI_BOARD_CELL_PIXELS,
                                                N * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING + 10))
                elif cell_team == YOU:
                    jangi.display.SURFACE.blit(jangi.display.you_piece_list[sprite_num],
                                               (3 * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING + 10,
                                                N * JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING + 10))

        if jangi.now_turn + 2 == jangi.turn_count:  # 왕이 상대 진영에서 버티는 승리조건
            gameover = True
        if remainingTime <= 0.05:  # 시간초 오버 승리조건
            defeated = jangi.turn
            gameover = True

        if (gameover == True) or (jangi.gmaeover == True):
            if jangi.winner == YOU:
                defeated = ME
            elif jangi.winner:
                defeated = YOU
            if not isEnd:
                pygame.display.update()
                time.sleep(0.5)
            isEnd = True
            # 게임 오버 이후 디스플레이
            jangi.display.SURFACE.fill((100, 100, 100))
            draw_text("GAME OVER", 70, (JANGI_BOARD_SIZE_G / 2 - 210, JANGI_BOARD_SIZE_S / 2 - 245), (255, 255, 255))
            if defeated == ']':
                rgb2 = (129, 183, 71)
                rgb1 = (230, 80, 80)
            else:
                rgb1 = (129, 183, 71)
                rgb2 = (230, 80, 80)
            draw_text(txt6, 40, (JANGI_BOARD_SIZE_G / 2 - 62, JANGI_BOARD_SIZE_S / 2 - 103), rgb1)  # winner
            draw_text(txt5, 40, (JANGI_BOARD_SIZE_G / 2 - 92, JANGI_BOARD_SIZE_S / 2 - 13), rgb2)  # loser
            draw_text(txt6_pre, 40, (JANGI_BOARD_SIZE_G / 2 - 225, JANGI_BOARD_SIZE_S / 2 - 105), (255, 255, 255))
            draw_text(txt5_pre, 40, (JANGI_BOARD_SIZE_G / 2 - 225, JANGI_BOARD_SIZE_S / 2 - 15), (255, 255, 255))

        pygame.display.update()
        clock.tick(FPS)  # 초당 프레임 조정

    pygame.quit()
    UserInfo.sendTarget.close()


class Chatting(QDialog):
    socketSignal = pyqtSignal(object)  # must be defined in class level

    def click(self):
        self.lis.addItem(UserInfo.id + ": " + self.edit.text())
        UserInfo.sendTarget.send(json.dumps({"cmd": "chat", "id": UserInfo.id, "data": self.edit.text()}).encode())
        self.edit.setText("")

    def socket_start(self):

        # 소켓을 만든다.
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 소켓 레벨과 데이터 형태를 설정한다.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 서버는 복수 ip를 사용하는 pc의 경우는 ip를 지정하고 그렇지 않으면 None이 아닌 ''로 설정한다.
        # 포트는 pc내에서 비어있는 포트를 사용한다. cmd에서 netstat -an | find "LISTEN"으로 확인할 수 있다.
        print("bind")
        server_socket.bind(('', 9999))
        # server 설정이 완료되면 listen를 시작한다.
        print("listen")
        server_socket.listen(1)
        try:
            client_socket, addr = server_socket.accept()
            print("받음")
            UserInfo.sendTarget = client_socket
            # 쓰레드를 이용해서 client 접속 대기를 만들고 다시 accept로 넘어가서 다른 client를 대기한다.
            th = threading.Thread(target=Server.threaded, args=(client_socket, addr, UserInfo.socketSignal))
            th.start()
        except:
            print("server")
        finally:
            # 에러가 발생하면 서버 소켓을 닫는다.
            server_socket.close()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.socketSignal.connect(executeOnMain)
        UserInfo.socketSignal = self.socketSignal
        # asyncio.run(self.socket_start())
        threading.Thread(target=self.socket_start).start()
        self.setWindowModality(Qt.ApplicationModal)
        self.mainLayout = QVBoxLayout()

        # self.mainLayout.setContentsMargins(130, 0, 130, 0)
        self.setGeometry(300, 300, 300, 500)
        util.center(self)
        # QVBoxLayout
        self.lis = QListWidget()
        UserInfo.chat = self.lis
        # self.makeList()
        blay = QHBoxLayout()
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Message")
        button = QToolButton()
        button.setText("push")
        button.setFixedHeight(50)
        button.setSizePolicy(QSizePolicy.Expanding, 0)
        button.clicked.connect(self.click)
        self.mainLayout.addWidget(self.lis)
        blay.addWidget(self.edit)
        blay.addWidget(button)
        self.mainLayout.addLayout(blay)

        self.setLayout(self.mainLayout)
        self.setWindowTitle('십이장기')


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    log = Chatting()
    log.show()
    app.exec_()
