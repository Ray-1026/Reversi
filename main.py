import sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from gamelogic import GameLogic, pygame
from board import Board
from agent import Agent
from player import PlayerAgent


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
    chooseSide = "black"
    status = "start"

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

    # 按鈕位置設定
    button_start = text_start.get_rect(center=(105, 250))
    button_PVC = text_PVC.get_rect(center=(55, 160))
    button_CVC = text_CVC.get_rect(center=(155, 160))
    button_black = text_black.get_rect(center=(25, 200))
    button_white = text_white.get_rect(center=(85, 200))
    button_restart = text_restart.get_rect(center=(130, 300))
    button_quit = text_quit.get_rect(center=(310, 300))

    # 按鈕狀態設定
    at_start = False
    at_restart = False
    at_quit = False

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
                if 70 <= x and x <= 145 and 230 <= y and y <= 270:
                    at_start = True
                else:
                    at_start = False

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if 70 <= x and x <= 145 and 230 <= y and y <= 270:  # 按下start鍵
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
                    elif 15 <= x and x <= 95 and 140 <= y and y <= 180:  # 按下PVC模式
                        pvc = True
                    elif 115 <= x and x <= 195 and 140 <= y and y <= 180:  # 按下CVC模式
                        pvc = False
                    elif pvc and 0 <= x and x <= 50 and 185 <= y and y <= 215:  # 在PVC模式下選擇黑棋
                        chooseSide = "black"
                    elif pvc and 60 <= x and x <= 110 and 185 <= y and y <= 215:  # 在PVC模式下選擇白棋
                        chooseSide = "white"

            board.draw(screen, status)
            if status == "start":
                if at_start:
                    pygame.draw.rect(screen, red, (70, 230, 75, 40), 0)
                else:
                    pygame.draw.rect(screen, red, (70, 230, 75, 40), 3)

                if pvc:
                    pygame.draw.rect(screen, green, (15, 140, 80, 40), 3)
                    pygame.draw.rect(screen, red, (115, 140, 80, 40), 3)
                    if chooseSide == "black":
                        pygame.draw.rect(screen, green, (0, 185, 50, 30), 2)
                        pygame.draw.rect(screen, red, (60, 185, 50, 30), 2)
                    else:
                        pygame.draw.rect(screen, red, (0, 185, 50, 30), 2)
                        pygame.draw.rect(screen, green, (60, 185, 50, 30), 2)
                    screen.blit(text_black, button_black)
                    screen.blit(text_white, button_white)

                else:
                    pygame.draw.rect(screen, red, (15, 140, 80, 40), 3)
                    pygame.draw.rect(screen, green, (115, 140, 80, 40), 3)

                screen.blit(text_start, button_start)
                screen.blit(text_PVC, button_PVC)
                screen.blit(text_CVC, button_CVC)

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

        pygame.display.update()
        main_clock.tick(60)


if __name__ == "__main__":
    main()
