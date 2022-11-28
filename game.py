from PyQt5.QtWidgets import *
from login import LogIn
# 메인 인터페이스를 만든다
# 	시작화면에는 오프라인 온라인 버튼이 있고
# 		오프라인을 누르면 두명이서 한 컴퓨터로 할 수 있는 십이장기게임이 실행 		된다.
# 		온라인을 누르면 방 목록 및 방 생성 버튼이 만들어진다.
# 			새로고침 버튼이 있어 새로고침 할 수 있다.
# 			방은 비밀번호가 있을 수도 있고 없을 수도 있다.
# 			방에 들어가면 채팅창이 있으며, 대결을 시작한다.-소켓통신을 사용
# 			방 생성을 하면 비밀번호 입력란, 방 이름 입력 란이 있고 방을 생			성 할 수 있다.
# 			방 생성은 한 아이피 당 하나만 가능 하고 방을 삭제 할 수 있다.
# Hangman -> text 비효율적
# 6개보다 많은 알파벳을 사용하는 단어가 들어오면 맞출 수가 없음
from PyQt5.uic.properties import QtWidgets

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    log = LogIn()
    log.show()
    sys.exit(app.exec_())
