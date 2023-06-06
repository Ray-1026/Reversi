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
    game = GameLogic("player")
    board = Board(game)
    agent = Agent("player")
    font = pygame.font.SysFont("Arial", 35)
    text = font.render("Start", True, (255, 255, 255))
    text_rect = text.get_rect(center=(350, 50))

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
                    if text_rect.collidepoint(event.pos):
                        game.status = 1
                        pygame.time.delay(1000)
            board.drawBoard(screen, game)
            pygame.draw.rect(screen, (255, 0, 0), (315, 25, 75, 50), 1)
            screen.blit(text, text_rect)

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
