import sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from gamelogic import GameLogic, pygame
from board import Board
from minimax_agent import Agent


def main():
    """
    初始化設定
    """
    pygame.init()
    main_clock = pygame.time.Clock()
    first = "player"
    game = GameLogic(first)
    board = Board(game)
    agent = Agent(first)

    """
    文字、按鈕設定
    """
    large_font = pygame.font.SysFont("Arial", 35)
    small_font = pygame.font.SysFont("Arial", 20)
    text_start = large_font.render("Start", True, (255, 255, 255))
    text_black = large_font.render("Black", True, (255, 255, 255))
    text_white = large_font.render("White", True, (255, 255, 255))
    text_restart = small_font.render("Restart", True, (255, 255, 255))
    text_quit = small_font.render("Quit", True, (255, 255, 255))
    button_start = text_start.get_rect(center=(350, 50))
    button_black = text_black.get_rect(center=(305, 100))
    button_white = text_white.get_rect(center=(390, 100))
    button_restart = text_restart.get_rect(center=(130, 300))
    button_quit = text_quit.get_rect(center=(310, 300))
    player_select = False
    at_start = False
    at_restart = False
    at_quit = False

    # cop = pygame.image.load("img/white_cop_with_gun-removebg-preview.png")
    # nigga = pygame.image.load("img/nigga-removebg-preview.png")
    # nigga = pygame.transform.scale(nigga, (90, 94))
    # cop = pygame.transform.scale(cop, (90, 94))

    """
    視窗大小、名稱設定
    """
    screen = pygame.display.set_mode((440, 440))
    pygame.display.set_caption("黑白棋 Reversi")

    """
    遊戲畫面更新和遊戲主要邏輯的運作
    """
    while True:
        if game.status == 0:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if player_select and button_start.collidepoint(event.pos):
                        game = GameLogic(first)
                        board = Board(game)
                        agent = Agent(first)
                        game.status = 1
                        pygame.time.delay(750)

                    if button_black.collidepoint(event.pos):
                        player_select = True
                        first = "player"
                    elif button_white.collidepoint(event.pos):
                        player_select = True
                        first = "computer"
                """
                取得滑鼠游標位置
                """
                x, y = pygame.mouse.get_pos()
                if 315 <= x and x <= 390 and 25 <= y and y <= 75:
                    at_start = True
                else:
                    at_start = False

            board.drawBoard(screen, game)
            if game.status == 0:
                if at_start:
                    pygame.draw.rect(screen, (255, 0, 0), (315, 25, 75, 50), 0)
                else:
                    pygame.draw.rect(screen, (255, 0, 0), (315, 25, 75, 50), 2)
                if first == "player":
                    pygame.draw.rect(screen, (0, 255, 0), (315 - 50, 30 + 50, 80, 50), 2)
                    pygame.draw.rect(screen, (255, 0, 0), (315 + 35, 30 + 50, 80, 50), 2)
                    # screen.blit(nigga, (270, 130))
                elif first == "computer":
                    pygame.draw.rect(screen, (255, 0, 0), (315 - 50, 30 + 50, 80, 50), 2)
                    pygame.draw.rect(screen, (0, 255, 0), (315 + 35, 30 + 50, 80, 50), 2)
                    # screen.blit(cop, (270, 130))
                screen.blit(text_start, button_start)
                screen.blit(text_black, button_black)
                screen.blit(text_white, button_white)

        elif game.status == 1:
            if game.turn == "computer":
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.time.delay(500)
                game.ComputerTurn(board.board, agent)
            else:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                        game.PlayerTurn(board.board)
            board.drawBoard(screen, game)

        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if button_restart.collidepoint(event.pos):
                        game.status = 0
                    elif button_quit.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                """
                取得滑鼠游標位置
                """
                x, y = pygame.mouse.get_pos()
                if 90 <= x and x <= 170 and 280 <= y and y <= 320:
                    at_restart = True
                else:
                    at_restart = False
                if 270 <= x and x <= 350 and 280 <= y and y <= 320:
                    at_quit = True
                else:
                    at_quit = False

            board.drawBoard(screen, game)
            if at_restart:
                pygame.draw.rect(screen, (255, 0, 0), (90, 280, 80, 40), 0)
            else:
                pygame.draw.rect(screen, (255, 255, 255), (90, 280, 80, 40), 2)
            if at_quit:
                pygame.draw.rect(screen, (255, 0, 0), (270, 280, 80, 40), 0)
            else:
                pygame.draw.rect(screen, (255, 255, 255), (270, 280, 80, 40), 2)
            screen.blit(text_restart, button_restart)
            screen.blit(text_quit, button_quit)

        pygame.display.update()
        main_clock.tick(40)


if __name__ == "__main__":
    main()
