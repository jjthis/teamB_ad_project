코드 구조

## game.py 메인 인터페이스를 만든다<br>
	시작화면에는 오프라인 온라인 버튼이 있고<br>
		오프라인을 누르면 두명이서 한 컴퓨터로 할 수 있는 십이장기게임이 실행된다.<br>
		온라인을 누르면 방 목록 및 방 생성 버튼이 만들어진다.<br>
			새로고침 버튼이 있어 새로고침 할 수 있다. <br>
			방은 비밀번호가 있을 수도 있고 없을 수도 있다.<br>
			방에 들어가면 채팅창이 있으며, 대결을 시작한다.-소켓통신을 사용<br>
			방 생성을 하면 비밀번호 입력란, 방 이름 입력 란이 있고 방을 생성 할 수 있다.<br?
			방 생성은 한 아이피 당 하나만 가능 하고 방을 삭제 할 수 있다.<br?
## janggi.py  십이장기 게임 인터터페이스가 들어간다<br>
	누구 차례인지 표시 되고, 시간초가 표시된다.<br>
		시간초가 넘어가면 지게 된다<br>
		자신의 턴이 아니면 말을 움직일 수 없다.<br>
	장기말을 누르면 테두리 색이 바뀌고 선택이 된다.
		장기가 갈 수 있는 위치의 칸도 색이 바뀌며 표시된다.<br>
		장기가 갈 수 있는 칸을 누르게 되면 move.py에서 moveCheck를 실행 시켜 갈 수 있는지<br> 	판단하고 갈 수 있으면 턴을 넘기고 갈 수 없다면 선택이 		풀린다,
	포로로 잡은 말을 선택해 판에 놓을 수 있게 구현<br>
	아이템 버튼이 있어 누르면 아이템을 사용할 수 있다.<br>
	장기가 끝나게 되면 승리자가 출력되고<br>
		오프라인일때는 게임 시작화면으로 돌아가고<br>
		온라인이면 게임 판을 리셋한다.<br>
## 아이템 사용 함수<br>
	멀리건<br>
		십이장기 아이템 멀리건, 멀리건 상대방이 말을 내려놓기 전까지 사용 가능		하며 바로 전 턴에 자신이 했던 플레이를 다시 할 수 있다. 멀리건을 사용할 		경우, 사용한 순간부터 다시 90초가 카운팅된다.<br>
	90초<br>
		십이장기 아이템 90초, 자신의 턴 시간제한 90초에 90초를 더 늘려준다.<br>
## gound.py - Gound class<br>
	장기 판의 상태를 저장하는 클래스<br>
## move.py<br>
	janggiColoring
	장기칸을 색칠하여 선택됐는지 혹은 갈 수 있는 칸인지를 표시
	moveCheck
	이동 할 수 있는지 판별하는 메소드가 들어간다
		판의 상태가 주어지고,
		이동 할 수 있으면 이동시키고 True를 리턴 시킨다
		이동 할 수 없으면 False를 리턴시킨다.

## -서버<br>
php 서버 방 생성 할 때 ip와 방이름, 비밀번호를 post로 받아 서버에 저장시켜 온라인 대전을 가능하게 한다.