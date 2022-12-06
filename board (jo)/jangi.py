import pygame
from pygame.locals import *
import math
from jangi_const import *
import time

class Input:
    def __init__(self):
        self.mouse_pressed = False
        self.mouse_clicked = False
        self.mx = 0
        self.my = 0

        self.src_pos = ""
        self.src_piece_type = ""
        self.src_rect = (JANGI_BOARD_PADDING, JANGI_BOARD_PADDING, JANGI_BOARD_CELL_PIXELS, JANGI_BOARD_CELL_PIXELS)
        self.is_src_set = False

        self.target_pos = ""
        self.target_piece_type = ""
        self.target_rect = (JANGI_BOARD_PADDING, JANGI_BOARD_PADDING, JANGI_BOARD_CELL_PIXELS, JANGI_BOARD_CELL_PIXELS)
        self.is_target_set = False

class Display:
    def __init__(self):
        self.SURFACE = pygame.display.set_mode((JANGI_BOARD_SIZE_G, JANGI_BOARD_SIZE_S))

        self.img_piece_ja = pygame.image.load(JANGI_PIECE_IMAGE_JA)
        self.img_piece_wang = pygame.image.load(JANGI_PIECE_IMAGE_WANG)
        self.img_piece_sang = pygame.image.load(JANGI_PIECE_IMAGE_SANG)
        self.img_piece_jang = pygame.image.load(JANGI_PIECE_IMAGE_JANG)
        self.img_piece_hu = pygame.image.load(JANGI_PIECE_IMAGE_HU)

        self.img_item_time = pygame.image.load(JANGI_ITEM_IMAGE_TIME)
        self.img_item_mulligan = pygame.image.load(JANGI_ITEM_IMAGE_MULLIGAN)

        self.you_piece_list = []
        self.me_piece_list = []
        self.prep_piece_picture()
        self.SURFACE.fill((100,100,100))

    def prep_piece_picture(self):
        
        # 이미지 크기 조정
        self.img_piece_ja = pygame.transform.scale(self.img_piece_ja, (JANGI_PIECES_PIXELS,JANGI_PIECES_PIXELS))
        self.img_piece_wang = pygame.transform.scale(self.img_piece_wang, (JANGI_PIECES_PIXELS,JANGI_PIECES_PIXELS))
        self.img_piece_sang = pygame.transform.scale(self.img_piece_sang, (JANGI_PIECES_PIXELS,JANGI_PIECES_PIXELS))
        self.img_piece_jang = pygame.transform.scale(self.img_piece_jang, (JANGI_PIECES_PIXELS,JANGI_PIECES_PIXELS))
        self.img_piece_hu = pygame.transform.scale(self.img_piece_hu, (JANGI_PIECES_PIXELS,JANGI_PIECES_PIXELS))
        
        self.img_item_time = pygame.transform.scale(self.img_item_time, (JANGI_BOARD_CELL_PIXELS,JANGI_BOARD_CELL_PIXELS))
        self.img_item_mulligan = pygame.transform.scale(self.img_item_mulligan, (JANGI_BOARD_CELL_PIXELS,JANGI_BOARD_CELL_PIXELS))
        # 리스트에 이미지 보관 (+ 포로 기능을 추가하면 '후'도 추가해야함)
        # 내 리스트
        self.me_piece_list.append(self.img_piece_ja)
        self.me_piece_list.append(self.img_piece_sang)
        self.me_piece_list.append(self.img_piece_wang)
        self.me_piece_list.append(self.img_piece_jang)
        self.me_piece_list.append(self.img_piece_hu)
        # 상대 리스트 (추후 한자를 뒤집는다거나 색깔을 바꾸어 차이를 줄 예정)
        self.you_piece_list.append(pygame.transform.rotate(self.img_piece_ja, 180))
        self.you_piece_list.append(pygame.transform.rotate(self.img_piece_sang, 180))
        self.you_piece_list.append(pygame.transform.rotate(self.img_piece_wang, 180))
        self.you_piece_list.append(pygame.transform.rotate(self.img_piece_jang, 180))
        self.you_piece_list.append(pygame.transform.rotate(self.img_piece_hu, 180))
#############################################################################################################
class Piece:
    def __init__(self, camp, type, pos, num):
        self.__type = type
        self.__team = camp
        self.__pos = pos
        self.__num = num
        self.__alive = True
    def getType(self):
        return self.__type
    def setType(self, type):
        self.__type = type
    def get_team(self):
        return self.__team
    def get_pos(self):
        return self.__pos
    def setPos(self, pos):
        self.__pos = pos
    def setPos(self, i ,j):
        self.__pos = [i,j]
    def get_num(self):
        return self.__num
    def setNum(self, num):
        self.__num = num
# 팀 만들기
class Team:
    def __init__(self, camp):
        self.__team = camp
        self.__pieces = []
        self.set_init_pos()
    
    # 초기 말의 위치를 정함
    def set_init_pos(self):
        self.__pieces = []
         # 상대 팀일 경우
        if self.__team == YOU:
            self.__pieces.append(Piece(self.__team, JA, [1, 1], 1))
            self.__pieces.append(Piece(self.__team, SANG, [0, 2], 2))
            self.__pieces.append(Piece(self.__team, WANG, [0, 1], 3))
            self.__pieces.append(Piece(self.__team, JANG, [0, 0], 4))
        # 나의 팀일 경우
        else:
            self.__pieces.append(Piece(self.__team, JA, [2, 1], 5))
            self.__pieces.append(Piece(self.__team, SANG, [3, 0], 6))
            self.__pieces.append(Piece(self.__team, WANG, [3, 1], 7))
            self.__pieces.append(Piece(self.__team, JANG, [3, 2], 8))
    
    def get_pieces(self):
        return self.__pieces
#########################################################################################################

class Jangi:
    now_turn = 999
    teams = {}
    poro_you = []
    poro_me = []
    turn_count = 1
    gmaeover = False
    winner = ''
    def __init__(self):
        self.board = []
        self.poro_board = []
        self.turn = ME
        self.team = {}
        self.team['me'] = Team(ME)
        self.team['you'] = Team(YOU)
        self.clear_board()
        self.clear_poro_board()
        self.fill_board()
        self.display = Display()
        self.input = Input()
        self.running = True
        self.start_time = time.time()
    def poro_get_pieces_me(self):
        return self.poro_me
    def poro_get_pieces_you(self):
        return self.poro_you
    def get_team(self, campStr):
        return self.team[campStr]
    # 보드판 생성
    def clear_board(self):
        self.board = []
        for N in range(4):
            row = []
            for M in range(3):
                row.append(EMPTY)
            self.board.append(row)
    def clear_board(self):
        self.board = []
        for N in range(4):
            row = []
            for M in range(3):
                row.append(EMPTY)
            self.board.append(row)
    def clear_poro_board(self):
        self.poro_board = []
        for N in range(4):
            row = []
            for M in range(2):
                row.append(EMPTY)
            self.poro_board.append(row)
    # 터미널에 보드판 출력
    def print_poro_board(self):
        for N in range(4):
            for M in range(2):
                print(self.poro_board[N][M][:2], end=' ')
            print()
        print()
    def print_board(self):
        for N in range(4):
            for M in range(3):
                print(self.board[N][M][:2], end=' ')
            print()
        print()    

    def is_Valid_pos_num(self, i, j):
        if (i >= 0 and i <= 3)and (j >= 0 and j <= 2):
            return True
        return False    
    def poro_is_Valid_pos_num(self, i, j):
        if (i >= 0 and i <= 4)and (j == 0 or j == 1):
            return True
        return False    


    # 픽셀 위치를 i,j로 변환하는 함수 (마우스 클릭 위치를 판별하는데 사용)
    def posPixel2Num(self, sx,sy, px, py, stride):
        pad = 0.1
        i = (py - sy) / stride
        j = (px - sx) / stride
        # i < 4.802 -> i = 4 /// 4.1~4.9
        # j < 2.09 -> X /// 2.1 ~ 2.9 패딩때문
        i_upper = math.floor(i)
        i_lower = math.ceil(i)
        j_left = math.floor(j)
        j_right = math.ceil(j)

        if i >= i_upper + pad and i <= i_lower - pad:
            if j >= j_left + pad and j <= j_right - pad:
                return True, i_upper, j_left
        return False, i_upper, j_left

 #########################################################################################
    def get_piece_team(self, i, j):
        return self.board[i][j][0]
    
    def get_piece_type(self, i,j):
        return self.board[i][j][1]

    def get_piece_num(self, camp, i,j):
        if camp == YOU:
            pieces = self.get_team("you").get_pieces()
        else:
            pieces = self.get_team("me").get_pieces()
        for piece in pieces:
            pos_i, pos_j = piece.get_pos()
            if pos_i == i and pos_j == j:
                return piece.get_num()
        return -1
    def poro_get_piece_num(self,camp,i,j):
        if camp == ME:
            for piece in self.poro_get_pieces_me():
                pos_i, pos_j = piece.get_pos()
                if pos_i == i and pos_j == j:
                    return piece.get_num()
        else:
            for piece in self.poro_get_pieces_you():
                pos_i, pos_j = piece.get_pos()
                if pos_i == i and pos_j == j:
                    return piece.get_num()
        
        return -1
    def get_cell(self, pos):
        return self.board[pos[0]][pos[1]]
    def get_cell(self, i, j):
        return self.board[i][j]
    def poro_get_cell(self, i, j):
        return self.poro_board[i][j]
    def set_cell(self, campStr, typeStr, i, j, num):
        self.board[i][j] =  campStr + typeStr + "{:02d}".format(num) 
    def set_cell(self, campStr, typeStr, pos, num):
        self.board[pos[0]][pos[1]] =  campStr + typeStr + "{:02d}".format(num) 
    def poro_set_cell(self, campStr, typeStr, pos, num):
        self.poro_board[pos[0]][pos[1]] =  campStr + typeStr + "{:02d}".format(num) 

    # 초기 보드판 세팅 수정필요
    def fill_board(self):
        pieces = self.get_team("you").get_pieces()
        for piece in pieces:
            self.set_cell(piece.get_team(), piece.getType(), piece.get_pos(), piece.get_num())
        pieces = self.get_team("me").get_pieces()
        for piece in pieces:
            self.set_cell(piece.get_team(), piece.getType(), piece.get_pos(), piece.get_num())  
        

    ################################
    def update_board(self):
        self.clear_board()
        self.fill_board()
    def currentTurn(self):
        return self.turn
    def nextTurn(self):
        if self.currentTurn() == ME:
            return YOU 
        else:
            return ME
    def changeTurn(self):
        self.turn = self.nextTurn()
        self.turn_count += 1
    def resetTime(self):
        self.start_time = time.time()
    def checkPieceType(self, i, j, PIECETYPE):
        return PIECETYPE == self.get_piece_type(i,j)
#################################################################
    def ja_move(self, src_i, src_j, target_i, target_j):
        if self.get_cell(src_i, src_j)[0] == "]" :
            if target_i - src_i == -1 and target_j - src_j == 0:
                return True
            else: return False
        else: 
            if target_i - src_i == 1 and target_j - src_j == 0:
                return True
            else: return False
    def sang_move(self, src_i, src_j, target_i, target_j):
        if abs((target_i - src_i)*(target_j - src_j)) == 1 :
            return True
        else: return False
    def wang_move(self, src_i, src_j, target_i, target_j):
        if abs(target_i - src_i) <= 1 and abs(target_j - src_j) <= 1 :
                return True
        else: return False
    def jang_move(self, src_i, src_j, target_i, target_j):
        if abs((target_i - src_i)*(target_j - src_j)) == 1:
            return False
        elif (abs(target_i - src_i) == 1 and target_j - src_j == 0 ) or (abs(target_i - src_i) == 0 and abs(target_j - src_j) == 1):
            return True
        else: return False
    def hu_move(self, src_i, src_j, target_i, target_j):
        if target_i - src_i == 1 and abs(target_j - src_j) == 1 : #뒤대각선 불가능
            return False
        elif abs(target_i - src_i) <= 1 and abs(target_j - src_j) <= 1 : #제외 6방향 가능
            return True
        else: return False

    def attack(self, i, j):
        if self.get_cell(i, j)[0] == '[':
            x = self.get_cell(i, j)[1]
            camp = ME
        elif self.get_cell(i, j)[0] == ']':
            x = self.get_cell(i, j)[1]
            camp = YOU
        self.poro_set(x, camp)
    def poro_set(self, x, camp):
        if x == 'h':
                x = 'a'
        if camp == ME:
            n = len(self.poro_me)
            self.poro_me.append(Piece(camp, x, [n, 0], 10+n))
        elif camp == YOU:
            n = len(self.poro_you)
            self.poro_you.append(Piece(camp, x, [n, 1], 20+n))
            
        for poro in self.poro_me:
            self.poro_set_cell(poro.get_team(), poro.getType(), poro.get_pos(), poro.get_num())
        for poro in self.poro_you:
            self.poro_set_cell(poro.get_team(), poro.getType(), poro.get_pos(), poro.get_num())
        
    def is_alreadyIn(self, src_i, src_j, target_i, target_j):
        if self.board[target_i][target_j] == EMPTY :
            return True
        elif self.get_cell(target_i,target_j)[0] == self.get_cell(src_i, src_j)[0] :
            return False
        else: 
            
            return True
#################################################################
    def move(self, i_from, j_from, i_to, j_to):
        end = False
        if i_from == i_to and j_from == j_to:
            return False
        
        print(i_from, j_from, i_to, j_to)
        src_piece = self.get_cell(i_from, j_from)
        print("src_piece:", src_piece)
        src_piece_team = src_piece[0]
        src_piece_num = self.get_piece_num(src_piece_team,i_from, j_from)
        target_piece = self.get_cell(i_to, j_to)
        target_piece_team = target_piece[0]
        target_piece_num = self.get_piece_num(target_piece_team,i_to, j_to)
        campStr = ""
        if src_piece_team == YOU:
            campStr = "you"
        else:
            campStr = "me"
        print(campStr)
        isSrcTurn = (self.turn == src_piece_team)
        isValid_from = self.is_Valid_pos_num(i_from, j_from)
        isValid_to = self.is_Valid_pos_num(i_to, j_to)

        if not isSrcTurn or not isValid_from or not isValid_to:
            return False
        moveSuccess = False
        #moved = self.is_piece_moved(src_piece_num)
        print('PieceNumber:', src_piece_num)

        if self.checkPieceType(i_from, j_from, JA):
            if self.ja_move(i_from, j_from, i_to, j_to):
                print(campStr+": 자 이동")
                moveSuccess = True
                if self.get_cell(i_to, j_to) != "00":
                    self.attack(i_to, j_to)
                    if self.board[i_to][j_to][1] == "w":
                        self.winner = src_piece_team
                        end = True
                # 말을 이동시키는 코드
                self.board[i_from][j_from] = EMPTY
                self.board[i_to][j_to] = src_piece_team + JA
                if i_to == 0 and src_piece_team == ME:
                        self.board[i_to][j_to] = src_piece_team + HU
                if i_to == 3 and src_piece_team == YOU:
                        self.board[i_to][j_to] = src_piece_team + HU
                if end:
                    self.gmaeover = True
                else:
                    self.gmaeover = False
                
        elif self.checkPieceType(i_from, j_from, SANG):
            if self.sang_move(i_from, j_from, i_to, j_to):
                print(campStr+": 상 이동")
                moveSuccess = True
                if self.get_cell(i_to, j_to) != "00":
                    self.attack(i_to, j_to)
                    if self.board[i_to][j_to][1] == "w":
                        self.winner = src_piece_team
                        end = True
                self.board[i_from][j_from] = EMPTY
                self.board[i_to][j_to] = src_piece_team + SANG
                if end:
                    self.gmaeover = True
                else:
                    self.gmaeover = False

        elif self.checkPieceType(i_from, j_from, WANG):
            if self.wang_move(i_from, j_from, i_to, j_to):
                print(campStr+": 왕 이동")
                moveSuccess = True
                if self.get_cell(i_to, j_to) != "00":
                    self.attack(i_to, j_to)
                    if self.board[i_to][j_to][1] == "w":
                        self.winner = src_piece_team
                        end = True
                self.board[i_from][j_from] = EMPTY
                self.board[i_to][j_to] = src_piece_team + WANG
                if i_to == 0 and src_piece_team == ME:
                        self.wangStand(src_piece_team)
                if i_to == 3 and src_piece_team == YOU:
                        self.wangStand(src_piece_team)
                if end:
                    self.gmaeover = True
                else:
                    self.gmaeover = False

        elif self.checkPieceType(i_from, j_from, JANG):
            if self.jang_move(i_from, j_from, i_to, j_to):
                print(campStr+": 장 이동")
                moveSuccess = True
                if self.get_cell(i_to, j_to) != "00":
                    self.attack(i_to, j_to)
                    if self.board[i_to][j_to][1] == "w":
                        self.winner = src_piece_team
                        end = True
                self.board[i_from][j_from] = EMPTY
                self.board[i_to][j_to] = src_piece_team + JANG
                if end:
                    self.gmaeover = True
                else:
                    self.gmaeover = False

        elif self.checkPieceType(i_from, j_from, HU):
            if self.hu_move(i_from, j_from, i_to, j_to):
                print(campStr+": 후 이동")
                moveSuccess = True
                if self.get_cell(i_to, j_to) != "00":
                    self.attack(i_to, j_to)
                    if self.board[i_to][j_to][1] == "w":
                        self.winner = src_piece_team
                        end = True
                self.board[i_from][j_from] = EMPTY
                self.board[i_to][j_to] = src_piece_team + HU
                if end:
                    self.gmaeover = True
                else:
                    self.gmaeover = False
           
        # 말이 성공적으로 움직였다면
        if moveSuccess: 
            # 보드 업데이트
            #self.update_board() 
            self.changeTurn()
            self.resetTime()
            # 말이 움직이면 시간초 리셋하는 알고리즘이기 때문에 포로 배치 같은 경우 따로 설정해줘야함
            # -> move함수 안에서 한다면 단순히 moveSuccess만 주면 됨
    def poro_in(self, i_from, j_from, i_to, j_to):
        print("poroin 함수 진입")
        src_piece = self.poro_get_cell(i_from, j_from)
        src_piece_team = src_piece[0]
        src_piece_num = self.poro_get_piece_num(src_piece_team,i_from, j_from)
        target_piece = self.get_cell(i_to, j_to)
        #target_piece_team = target_piece[0]
        print(src_piece)
        print(target_piece)

        campStr = ""
        if src_piece_team == YOU:
            campStr = "you"
        else:
            campStr = "me"
        #print(campStr+": 포로 배치")
        
        isSrcTurn = (self.turn == src_piece_team)
        poro_isValid_from = self.poro_is_Valid_pos_num(i_from, j_from)
        isValid_to = self.is_Valid_pos_num(i_to, j_to)

        if not isSrcTurn or not poro_isValid_from or not isValid_to:
            return False
        # 상대 진영에 포로 배치 불가 구현
        if i_to == 0 and src_piece_team == ME:
            return False
        if i_to == 3 and src_piece_team == YOU:
            return False

        moveSuccess = False
        if target_piece[:2] == "00":
            self.poro_board[i_from][j_from] = EMPTY
            self.board[i_to][j_to] = src_piece_team + src_piece[1]
            moveSuccess = True
        
        if moveSuccess:
            print(self.poro_me)
            print(self.poro_you)
            print(src_piece_num)
            #20 21 22 ... src_piece_num-20 \\ 0 1 2  ...
            if src_piece_team == ME:
                del self.poro_me[src_piece_num-10]
            elif src_piece_team == YOU:
                del self.poro_you[src_piece_num-20]
            self.changeTurn()
            self.resetTime()
    def wangStand(self, team): # 왕이 상대 진영에서 턴이 돌아올때까지 버티면 게임 오버
        self.now_turn = self.turn_count
        self.winner = team

    
               


        
#jangi = Jangi()
#jangi.make_init_board()
#jangi.print_board()