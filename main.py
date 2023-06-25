import sys
import utils
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from gamelogic import GameLogic, pygame
from board import Board
from agent import Agent
from player import PlayerAgent
from remote_agent import RemoteAgent
# from player import PlayerAgent
from client import *

def main():
    """
    # Pygame 啟動 !!!
    """
    # 初始化
    pygame.init()
    main_clock = pygame.time.Clock()
    board = Board()

    # 模式設定
    pvc = True
    passive = True
    user_name = ''
    at_input = True
    
    color = (255, 255, 255)
    chooseSide = "black"
    status = "start"
    sub_status = "choose online mode"

    # 顏色設定
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)

    # 按鈕文字設定
    large_font = pygame.font.SysFont("Arial", 35)
    small_font = pygame.font.SysFont("Arial", 20)
    text_start = large_font.render("Start", True, white)
    text_PVC = large_font.render("PVC", True, white)
    text_CVC = large_font.render("CVC", True, white)
    text_black = small_font.render("Black", True, white)
    text_white = small_font.render("White", True, white)
    text_restart = small_font.render("Restart", True, white)
    text_quit = small_font.render("Quit", True, white)
    text_PVP = large_font.render("PVP", True, white)
    text_passive = large_font.render('Connect by others', True, white)
    text_active= large_font.render('Connect others', True, white)

    # 按鈕位置設定
    button_start = text_start.get_rect(center=(335, 150))
    button_PVC = text_PVC.get_rect(center=(280, 60))
    button_CVC = text_CVC.get_rect(center=(390, 60))
    button_black = text_black.get_rect(center=(250, 100))
    button_white = text_white.get_rect(center=(310, 100))
    button_restart = text_restart.get_rect(center=(130, 300))
    button_quit = text_quit.get_rect(center=(310, 300))
    button_PVP = text_PVP.get_rect(center=(335, 210))
    button_passive = text_passive.get_rect(center=(220, 180))
    button_active = text_active.get_rect(center=(220, 260))
    name_input_box = pygame.Rect(150, 204, 140, 40)

    
    # 按鈕狀態設定
    at_start = False
    at_restart = False
    at_quit = False
    at_PVP = False
    
    # 視窗大小、名稱設定
    screen = pygame.display.set_mode((440, 440))
    pygame.display.set_caption("黑白棋 Reversi")

    # 遊戲畫面更新和遊戲主要邏輯的運作
    while True:
        # 遊戲開始
        if status == "start":
            for event in pygame.event.get():
                # 取得滑鼠游標位置
                x, y = pygame.mouse.get_pos()

                # 判斷滑鼠是否移動到按鈕上
                if 300 <= x and x <= 375 and 125 <= y and y <= 175:
                    at_start = True
                else:
                    at_start = False

                if 300 <= x and x <= 375 and 185 <= y and y <= 235:
                    at_PVP = True
                else:
                    at_PVP = False


                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if 300 <= x and x <= 375 and 125 <= y and y <= 175:  # 按下start鍵
                        at_start = False
                        status = "run"
                        if pvc:  # 選擇PVC模式
                            agent1 = PlayerAgent(chooseSide)  # 玩家
                            agent2 = Agent("white" if chooseSide == "black" else "black")  # 電腦
                        else:  # 選擇CVC模式
                            agent1 = Agent("white")  # 1號電腦
                            agent2 = Agent("black")  # 2號電腦
                        game = GameLogic(agent1, agent2, screen)
                        pygame.time.delay(750)
                    elif 240 <= x and x <= 320 and 40 <= y and y <= 80:  # 按下PVC模式
                        pvc = True
                    elif 350 <= x and x <= 430 and 40 <= y and y <= 80:  # 按下CVC模式
                        pvc = False
                    elif pvc and 225 <= x and x <= 275 and 85 <= y and y <= 115:  # 在PVC模式下選擇黑棋
                        chooseSide = "black"
                    elif pvc and 285 <= x and x <= 335 and 85 <= y and y <= 115:  # 在PVC模式下選擇白棋
                        chooseSide = "white"
                    elif 300 <= x and x <= 375 and 185 <= y and y <= 235:
                        at_PVP = False
                        status = 'PVP'

            board.draw(screen, status)
            if status == "start":
                if at_start:
                    pygame.draw.rect(screen, red, (300, 125, 75, 50), 0)
                else:
                    pygame.draw.rect(screen, red, (300, 125, 75, 50), 2)

                if at_PVP:
                    pygame.draw.rect(screen, red, (300, 185, 75, 50), 0)
                else:
                    pygame.draw.rect(screen, red, (300, 185, 75, 50), 2)
                
                if pvc:
                    pygame.draw.rect(screen, green, (240, 40, 80, 40), 2)
                    pygame.draw.rect(screen, red, (350, 40, 80, 40), 2)
                    if chooseSide == "black":
                        pygame.draw.rect(screen, green, (225, 85, 50, 30), 2)
                        pygame.draw.rect(screen, red, (285, 85, 50, 30), 2)
                    else:
                        pygame.draw.rect(screen, red, (225, 85, 50, 30), 2)
                        pygame.draw.rect(screen, green, (285, 85, 50, 30), 2)
                    screen.blit(text_black, button_black)
                    screen.blit(text_white, button_white)

                else:
                    pygame.draw.rect(screen, red, (240, 40, 80, 40), 2)
                    pygame.draw.rect(screen, green, (350, 40, 80, 40), 2)

                screen.blit(text_start, button_start)
                screen.blit(text_PVC, button_PVC)
                screen.blit(text_CVC, button_CVC)
                screen.blit(text_PVP, button_PVP)

        # 遊戲進行
        elif status == "run":
            game.run(screen, main_clock)
            status = "end"  # 遊戲結束後變換狀態

        # 遊戲結束
        elif status == "end":
            for event in pygame.event.get():
                # 取得滑鼠游標位置
                x, y = pygame.mouse.get_pos()

                # 判斷滑鼠是否移動到restart按鈕上
                if 90 <= x and x <= 170 and 280 <= y and y <= 320:
                    at_restart = True
                else:
                    at_restart = False

                # 判斷滑鼠是否移動到restart按鈕上
                if 270 <= x and x <= 350 and 280 <= y and y <= 320:
                    at_quit = True
                else:
                    at_quit = False

                # 判斷按下Restart、Quit或關閉視窗
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if 90 <= x and x <= 170 and 280 <= y and y <= 320:  # 按下restart
                        status = "start"
                        at_quit = False
                        at_restart = False
                    elif 270 <= x and x <= 350 and 280 <= y and y <= 320:  # 按下Quit
                        pygame.quit()
                        sys.exit()

            board.draw(screen, status, game)
            if at_restart:
                pygame.draw.rect(screen, red, (90, 280, 80, 40), 0)
            else:
                pygame.draw.rect(screen, white, (90, 280, 80, 40), 2)

            if at_quit:
                pygame.draw.rect(screen, red, (270, 280, 80, 40), 0)
            else:
                pygame.draw.rect(screen, white, (270, 280, 80, 40), 2)

            screen.blit(text_restart, button_restart)
            screen.blit(text_quit, button_quit)
            
        
        elif status == 'PVP':
            # 選擇passive還是active畫面
            if sub_status == 'choose online mode':
                for event in pygame.event.get():
                    x, y = pygame.mouse.get_pos()
                    # 判斷滑鼠是否移動到restart按鈕上
                    if button_passive.collidepoint((x, y)):
                        pygame.draw.rect(screen, red, (button_passive.left, button_passive.top, button_passive.width, button_passive.height), 0)
                    else:
                        pygame.draw.rect(screen, black, (button_passive.left, button_passive.top, button_passive.width, button_passive.height), 0)
                        
                    if button_active.collidepoint((x, y)):
                        pygame.draw.rect(screen, red, (button_active.left, button_active.top, button_active.width, button_active.height), 0)
                    else:
                        pygame.draw.rect(screen, black, (button_active.left, button_active.top, button_active.width, button_active.height), 0)
                        
                    screen.blit(text_passive, button_passive)
                    screen.blit(text_active, button_active)
                    
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == MOUSEBUTTONDOWN:
                        if button_passive.collidepoint((x, y)):
                            sub_status = 'input name'
                            passive = True
                            screen.fill(black)
                        if button_active.collidepoint((x, y)):
                            sub_status = 'input name'
                            passive = False
                            screen.fill(black)
                            
                            
            elif sub_status == 'input name':
                
                for event in pygame.event.get():
                    x, y = pygame.mouse.get_pos()
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        
                        # 判斷滑鼠是否移動到restart按鈕上
                    elif at_input and event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            user_name = user_name[:-1]
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                            mode = 'passive' if passive else 'active'
                            s = connect_server()
                            if register_name(user_name, mode, s):
                                sub_status = 'online list'
                                if mode == 'passive':
                                    start_sending_trash(s)
                                screen.fill(black)
                                break
                            else:
                                print('Internal Server Error')
                                disconnect(s)
                                pygame.quit()
                                sys.exit()
                        else:
                            user_name += event.unicode
                                
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if name_input_box.collidepoint((x, y)):
                            at_input = True
                            color = white
                        else:
                            at_input = False
                            color = (100, 100, 100)
                    title_text = large_font.render('Please input your name', True, white)
                    remind_text = small_font.render('Press Enter to continue', True, white)
                    name = large_font.render(user_name, True, black)
                    
                    title_rect = title_text.get_rect(center=(name_input_box.centerx, name_input_box.centery-50))
                    remind_rect = remind_text.get_rect(center=(name_input_box.centerx, name_input_box.centery+50))
                    pygame.draw.rect(screen, color, name_input_box)
                    
                    
                    screen.blit(remind_text, remind_rect)
                    screen.blit(title_text, title_rect)
                    screen.blit(name, (name_input_box.x+5, name_input_box.y+5))
                    
            elif sub_status == 'online list':
                
                    if passive:
                        # render waiting
                        waiting_text = large_font.render('Waiting for opponent...', True, white)
                        waiting_rect = waiting_text.get_rect(center=(220, 220))
                        screen.blit(waiting_text, waiting_rect)
                        opponent = passive_recv_req(s)
                        
                        # receive match request
                        if opponent != -1:
                            stop_sending_trash()
                            req_text = small_font.render(f'{opponent} want to play with you!', True, white)
                            req_rect = req_text.get_rect(center=(220, 50))
                            screen.blit(req_text, req_rect)
                            sub_status = 'passive confirm'
                        
                        # 讓pygame不要死機  
                        for event in pygame.event.get():                    
                            if event.type == QUIT:
                                disconnect(s)
                                pygame.quit()
                                sys.exit()
                    else: 
                        # render online list
                        for event in pygame.event.get():
                            x, y = pygame.mouse.get_pos()
                            screen.fill(black)
                            if event.type == QUIT:
                                disconnect(s)
                                pygame.quit()
                                sys.exit()
                                
                            # get online list
                            online_list = request_online_list(s)
                            if online_list != -1:
                                for idx, name in enumerate(online_list):
                                    user_text = small_font.render(name, True, white)
                                    user_rect = user_text.get_rect(center=(220, 50*(idx+1)))
                                    
                                    if user_rect.collidepoint((x, y)):
                                        pygame.draw.rect(screen, green, (user_rect.left, user_rect.top, user_rect.width, user_rect.height), 2)
                                    else:
                                        pygame.draw.rect(screen, black, (user_rect.left, user_rect.top, user_rect.width, user_rect.height), 0)
                                        
                                    # send match request to choosen opponent
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        if user_rect.collidepoint((x, y)) :
                                            sub_status = 'active waiting'
                                            send_opponent(s, name)
                                            start_sending_trash(s)
                                            screen.fill(black)
                                            break
                                        
                                    screen.blit(user_text, user_rect)
                            else:
                                print('Internal server error')
                                disconnect(s)
                                pygame.quit()
                                sys.exit()
                            
            elif sub_status == 'active waiting':
                
                waiting_text = large_font.render('Waiting for opponent...', True, white)
                waiting_rect = waiting_text.get_rect(center=(220, 220))
                screen.blit(waiting_text, waiting_rect)
                    
                if active_req_ok(s):
                    sub_status = 'setup pvp game'
                    stop_sending_trash()
                    screen.fill(black)
                    
                for event in pygame.event.get():
                    if event.type == QUIT:
                        disconnect(s)
                        pygame.quit()
                        sys.exit()
                    
            
            elif sub_status == 'passive confirm':
                for event in pygame.event.get():
                    x, y = pygame.mouse.get_pos()
                    if event.type == QUIT:
                        disconnect(s)
                        pygame.quit()
                        sys.exit()
                        
                    ok_text = small_font.render("Ready", True, white)
                    ok_rect = ok_text.get_rect(center=(220, 100))   
                    if ok_rect.collidepoint((x, y)):
                        pygame.draw.rect(screen, green, (ok_rect.left, ok_rect.top, ok_rect.width, ok_rect.height), 2)
                    else:
                        pygame.draw.rect(screen, red, (ok_rect.left, ok_rect.top, ok_rect.width, ok_rect.height), 0)
                    
                    # send ok request
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if ok_rect.collidepoint((x, y)):
                            passive_send_ok(s, user_name, opponent)
                            screen.fill(black)
                            sub_status = 'setup pvp game'
                            break
                    screen.blit(ok_text, ok_rect)
                    
            elif sub_status =='setup pvp game':
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    game_order = get_game_order(s, True, passive)
                    setup_text = large_font.render('Loading...', True, white)
                    setup_rect = setup_text.get_rect(center=(220, 220))
                    
                    screen.blit(setup_text, setup_rect)
                    if game_order != -1:
                        status = 'PVP run 1'
                        screen.fill(black)
                        break
                    
        elif status == 'PVP run 1':
            for event in pygame.event.get():
                if event.type == QUIT:
                    disconnect(s)
                    pygame.quit()
                    sys.exit()
            agent1 = PlayerAgent(game_order)
            agent2 = RemoteAgent("white" if game_order == "black" else "black")
            game = GameLogic(agent1, agent2, screen, s, user_name)
            game.run(screen, main_clock)
            status = "PVP end run 1"
        elif status == "PVP end run 1":
            print("end pvp run 1")
            score = utils.getScore(game.board.board)
            s.sendall(packing(["END1", user_name, str(score[game_order]), str(score["white" if game_order == "black" else "black"])]))
            time.sleep(1)
            game_order = get_game_order(s, False, passive)
            print(game_order, "game_order")
            time.sleep(0.5)
            s.sendall(packing(["OK", user_name]))
            data = s.recv(1024).decode('utf-8')
            print("start game 2", data)
            if data == "OK":
                status = "PVP run 2"
                screen.fill(black)
        elif status == "PVP run 2":
            agent1 = PlayerAgent(game_order)
            agent2 = RemoteAgent("white" if game_order == "black" else "black")
            game = GameLogic(agent1, agent2, screen, s, user_name)
            game.run(screen, main_clock)
            status = "PVP end run 2"
            score = utils.getScore(game.board.board)
            s.sendall(packing(["END2", user_name, str(score[game_order]), str(score["white" if game_order == "black" else "black"])]))
            data = s.recv(2048)
            results = pickle.loads(data)
        elif status == "PVP end run 2":
            for event in pygame.event.get():
                # 取得滑鼠游標位置
                x, y = pygame.mouse.get_pos()

                # 判斷滑鼠是否移動到restart按鈕上
                if 90 <= x and x <= 170 and 280 <= y and y <= 320:
                    at_restart = True
                else:
                    at_restart = False

                # 判斷滑鼠是否移動到restart按鈕上
                if 270 <= x and x <= 350 and 280 <= y and y <= 320:
                    at_quit = True
                else:
                    at_quit = False

                # 判斷按下Restart、Quit或關閉視窗
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if 90 <= x and x <= 170 and 280 <= y and y <= 320:  # 按下restart
                        status = "start"
                        at_quit = False
                        at_restart = False
                    elif 270 <= x and x <= 350 and 280 <= y and y <= 320:  # 按下Quit
                        pygame.quit()
                        sys.exit()
            board.draw(screen, "end pvp", game, user_name, results)
            if at_restart:
                pygame.draw.rect(screen, red, (90, 280, 80, 40), 0)
            else:
                pygame.draw.rect(screen, white, (90, 280, 80, 40), 2)

            if at_quit:
                pygame.draw.rect(screen, red, (270, 280, 80, 40), 0)
            else:
                pygame.draw.rect(screen, white, (270, 280, 80, 40), 2)

            screen.blit(text_restart, button_restart)
            screen.blit(text_quit, button_quit)

                
        pygame.display.update()
        main_clock.tick(60)
    


if __name__ == "__main__":
    main()
