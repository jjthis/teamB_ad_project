# 상수 저장
JANGI_BOARD_CELL_PIXELS = 100 # 보드판 한 칸
JANGI_BOARD_PADDING = 150 # 보드판 밖 비어있는 공간
JANGI_PIECES_PIXELS = 80 # 말 크기
JANGI_BOARD_SIZE_S = JANGI_BOARD_CELL_PIXELS * 4 + JANGI_BOARD_PADDING*2 # 보드판 세로 사이즈
JANGI_BOARD_SIZE_G = JANGI_BOARD_CELL_PIXELS * 3 + JANGI_BOARD_PADDING*2 # 보드판 가로 사이즈
# 이미지 (경로가 바뀌면 수정 필요)
JANGI_PIECE_IMAGE_JA = "./pieceimg/JA.png"
JANGI_PIECE_IMAGE_SANG = "./pieceimg/SANG.png"
JANGI_PIECE_IMAGE_WANG = "./pieceimg/WANG.png"
JANGI_PIECE_IMAGE_JANG = "./pieceimg/JANG.png"

JANGI_ITEM_IMAGE_TIME = "./pieceimg/addTime.png"
JANGI_ITEM_IMAGE_MULLIGAN = "./pieceimg/Mulligan.png"
# 색상 저장
JANGI_PIECE_SRC_COLOR = (80, 80, 240)
JANGI_PIECE_TARGET_COLOR = (240, 80, 80)
# 말
EMPTY = '00'
JANG = 'j'
SANG = 's'
WANG = 'w'
JA = 'a'
# 진영
YOU = '['
ME = ']'

#   보드판 좌표
#     0 1 2
#    @ㅡㅡㅡ@
#  0 |      |
#  1 |      |
#  2 |  ]a  |
#  3 |]s]w]j|
#    @ㅡㅡㅡ@
#
# 보드판에 말이 놓여져 있는 말은 두글자로 표현
# ex) [a = 상대 자, [j = 상대 장, 00 = 비어있음, ]s = 나의 상