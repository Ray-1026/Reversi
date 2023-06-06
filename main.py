import sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from gamelogic import GameLogic, pygame
from board import Board
from agent import Agent


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
    font = pygame.font.SysFont("Arial", 35)
    text_start = font.render("Start", True, (255, 255, 255))
    text_black = font.render("Black", True, (255, 255, 255))
    text_white = font.render("White", True, (255, 255, 255))
    button_start = text_start.get_rect(center=(350, 50))
    button_black = text_black.get_rect(center=(310, 100))
    button_white = text_white.get_rect(center=(390, 100))
    player_select = False

    # cop = pygame.image.load("img/white_cop_with_gun-removebg-preview.png")
    # nigga = pygame.image.load("img/nigga-removebg-preview.png")
    # nigga = pygame.transform.scale(nigga, (90, 94))
    # cop = pygame.transform.scale(cop, (90, 94))

    """
    視窗大小、名稱設定
    """
    screen = pygame.display.set_mode((board.boardRect.width, board.boardRect.height))
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
                        pygame.time.delay(1000)
                    if button_black.collidepoint(event.pos):
                        player_select = True
                        first = "player"

                    elif button_white.collidepoint(event.pos):
                        player_select = True
                        first = "computer"


            board.drawBoard(screen, game)
            pygame.draw.rect(screen, (255, 0, 0), (315, 25, 75, 50), 1)
            if first=="player": 
                pygame.draw.rect(screen, (0, 255, 0), (315-40, 25+50, 75, 50), 1)
                pygame.draw.rect(screen, (255, 0, 0), (315+40, 25+50, 75, 50), 1)
                # screen.blit(nigga, (270, 130))
            elif first=="computer": 
                pygame.draw.rect(screen, (255, 0, 0), (315-40, 25+50, 75, 50), 1)
                pygame.draw.rect(screen, (0, 255, 0), (315+40, 25+50, 75, 50), 1)
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
            board.drawBoard(screen, game)

        pygame.display.update()
        main_clock.tick(40)


if __name__ == "__main__":
    main()
