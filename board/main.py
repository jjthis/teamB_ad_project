from jangi_const import *
from jangi import *

jangi = Jangi()
jangi.print_board()
print('Turn:', jangi.turn)


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
        isValid, mi, mj = jangi.posPixel2Num(JANGI_BOARD_PADDING, JANGI_BOARD_PADDING, jangi.input.mx, jangi.input.my, JANGI_BOARD_CELL_PIXELS) 
        #print(isValid, mi, mj)
        if not isValid:
            jangi.input.mouse_pressed = False
            is_src_set = False
            is_target_set = False
            continue
        else:
            #print(isValid, mi, mj)
            if not jangi.input.is_src_set:
                src_i, src_j = (mi, mj)
                jangi.input.src_rect = (mj*JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING, mi*JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING, JANGI_BOARD_CELL_PIXELS, JANGI_BOARD_CELL_PIXELS)
                jangi.input.src_piece_type = jangi.get_cell(mi, mj)
                jangi.input.is_src_set = True
            else:
                target_i, target_j = (mi, mj)
                jangi.input.target_rect = (mj*JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING, mi*JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING, JANGI_BOARD_CELL_PIXELS, JANGI_BOARD_CELL_PIXELS)
                jangi.input.target_piece_type = jangi.get_cell(mi, mj)
                jangi.input.is_target_set = True
        # 조건을 만족했을 때 이동
        if jangi.input.is_src_set and jangi.input.is_target_set:
            print("From:",src_i,src_j,"/ To:",target_i,target_j)
            jangi.move(src_i, src_j, target_i, target_j)
            jangi.input.is_src_set = False
            jangi.input.is_target_set = False
            jangi.print_board()
            print('Turn:', jangi.turn)
            print('--------------------------------')
            


    #drawing the board
    for i in range(4):
        for j in range(3):
            rect = (j*JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING,i*JANGI_BOARD_CELL_PIXELS + JANGI_BOARD_PADDING, JANGI_BOARD_CELL_PIXELS, JANGI_BOARD_CELL_PIXELS)
            pygame.draw.rect(jangi.display.SURFACE, (240,217,183), rect, 0)
            if i == 0:
                pygame.draw.rect(jangi.display.SURFACE, (230,80,80), rect, 0)
            elif i == 3:
                pygame.draw.rect(jangi.display.SURFACE, (129,183,71), rect, 0)
            pygame.draw.rect(jangi.display.SURFACE, (50,50,50), rect, 1)
    if jangi.input.is_src_set:
        pygame.draw.rect(jangi.display.SURFACE, JANGI_PIECE_SRC_COLOR, jangi.input.src_rect, 5)
    elif jangi.input.is_target_set: # 옮길 위치에 색깔 표시, 기능 안함, 원인 찾아야함
        pygame.draw.rect(jangi.display.SURFACE, JANGI_PIECE_TARGET_COLOR, jangi.input.target_rect, 5)

    #drawing the pieces
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
                (M*JANGI_BOARD_CELL_PIXELS+JANGI_BOARD_PADDING+10, N*JANGI_BOARD_CELL_PIXELS+JANGI_BOARD_PADDING+10))
            elif cell_team == YOU:
                jangi.display.SURFACE.blit(jangi.display.you_piece_list[sprite_num], 
                (M*JANGI_BOARD_CELL_PIXELS+JANGI_BOARD_PADDING+10, N*JANGI_BOARD_CELL_PIXELS+JANGI_BOARD_PADDING+10))            
        

    pygame.display.update()

pygame.quit()