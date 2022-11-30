class Piece:
    def __init__(self, isEnemy, x, y, isIn):
        self.isEnemy = isEnemy
        self.x = x
        self.y = y
        self.isIn = isIn


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
    def move(self, x, y, xx, yy, piece):
        if y == -1 and x == -1:
            # 처음위치 없음
            # 처리
            pass
