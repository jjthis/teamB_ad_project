class Piece:

    #

    def __init__(self, isEnemy, x, y, isIn, piece, color):
        self.isEnemy = isEnemy
        self.x = x
        self.y = y
        self.isIn = isIn
        self.piece = piece
        self.color = color 


class Ground:
    stat = []
    myPrisoner = []
    enemyPrisoner = []

    def __init__(self):
        for i in range(4):
            for j in range(3):
                self.stat[i][j] = Piece(True, i, j, True)

    # 말이 이동 가능 장소인지
    # 가려는 장소에 말이 있는지
    def move(self, x, y, xx, yy, piece, color):
        if y == -1 and x == -1:
            # 처음위치 없음
            # 처리
            pass

        if piece == 1 :
            # 말 형태: 장
            if abs((xx-x)*(yy-y)) == 1: # 좌우위아래 가능 대각선 불가능
                return False
            elif abs(xx-x) == 1 or abs(yy-y) == 1:
                return True
            else: return False
        elif piece == 2 :
            # 말 형태: 상
            if abs((xx-x)*(yy-y)) == 1 : # 대각선만 가능 좌표차:(1,-1)(1,1)(1,-1)(-1,-1)로 곱 1 or -1
                return True
            else: return False
        elif piece == 3 :
            # 말 형태: 왕
            if abs(xx-x)==1 or abs(yy-y)==1 : # 좌우위아래대각선 다 가능 = 좌표차:1 가능
                return True
            else: False
        elif piece == 4 :
            # 말 형태: 자
            if color == 1 : # 한(빨강)
                if xx - x == 1 : # 앞만
                    return True
                else: return False
            else: # 초(초록)
                if xx - x == -1 :
                    return True
                else: return False
        elif piece == 5 :
            # 말 형태: 후
            if color == 1 : #한(빨강)
                if xx - x == -1 and abs(yy-y) == 1 : #뒤대각선 불가능
                    return False
                elif abs(xx-x) == 1 or abs(yy-y) == 1 : #제외 6방향 가능
                    return True
                else: return False    
            else: #초(초록)
                if xx - x == 1 and abs(yy-y) == 1 :
                    return False
                elif abs(xx-x) == 1 or abs(yy-y) == 1 :
                    return True
                else: return False   

        if color == Piece.color and Piece.x == xx and Piece.y == yy and Piece.isIn == True : 
            # 가려는 장소에 같은 팀 말이 있으면 불가능
            return False
