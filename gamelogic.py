import pygame


class GameLogic:
    #宣告
    def __init__(self, player_first):
        ########################################################
        # - player_first: whether player move first
        #------------------------------------------------------
        # - playerSide: the side of the player's disk
        # - computerSide:  the side of the player's disk
        # - turn: who's turn to play
        # - last_move: the last move of the computer
        # - status: the status of the game
        # - direct: the 8 directions
        ########################################################
        if player_first:
            self.playerSide = "black"
            self.computerSide = "white"
            self.turn = "player"
        else:
            self.playerSide = "white"
            self.computerSide = "black"
            self.turn = "computer"
        self.last_move = []
        self.status = 0
        self.direct = [
            [0, 1],
            [1, 1],
            [1, 0],
            [1, -1],
            [0, -1],
            [-1, -1],
            [-1, 0],
            [-1, 1],
        ]

    def getFlipDisks(self, board, side, xstart, ystart):
        ########################################################
        # - board: the status of the tiles in the current board
        # - side: the side of the placed disk
        # - xstart: x location of the the placed disk
        # - ystart: y location of the the placed disk
        #------------------------------------------------------
        # - return the list of disks that should be flipped
        #######################################################
        board[xstart][ystart] = side
        otherside = "white"
        if side == "white":
            otherside = "black"
        flipped_disks = []
        for xdirect, ydirect in self.direct:
            x, y = xstart + xdirect, ystart + ydirect
            temp = []
            while self.isOnBoard(x, y) and board[x][y]!="none":
                if board[x][y] == otherside:
                    temp.append([x, y])
                    x += xdirect
                    y += ydirect
                if not self.isOnBoard(x, y):
                    break
                if board[x][y] == side:
                    flipped_disks+=temp
                    break
        board[xstart][ystart] = "none"
        return flipped_disks

    def isValidMove(self, board, side, xstart, ystart):
        #######################################################
        # - board: the status of the tiles in the current board
        # - side: the side of the placed disk
        # - xstart: x location of the placed disk
        # - ystart: y location of the placed disk
        #------------------------------------------------------
        # - return whether the move is valid
        #######################################################
        if (not self.isOnBoard(xstart, ystart) 
        or board[xstart][ystart] != "none" 
        or len(self.getFlipDisks(board, side, xstart, ystart))==0):
            return False
        return True 

    def isOnBoard(self, x, y):
        ########################################################
        # - x: x location of the tile
        # - y: y location of the tile
        #------------------------------------------------------
        # - return whether the tile is on board
        #######################################################
        return 7 >= x and x >= 0 and 7 >= y and y >= 0

    def getValidMoves(self, board, side):
        #######################################################
        # - board: the status of the tiles in the current board
        # - side: the side of the placed disk
        #------------------------------------------------------
        # - return the list of valid moves
        #######################################################
        valid = []
        for x in range(8):
            for y in range(8):
                if self.isValidMove(board, side, x, y):
                    valid.append([x, y])
        return valid

    def getScore(self, board):
        #######################################################
        # - board: the status of the tiles in the current board
        #------------------------------------------------------
        # - return the scores of two sides
        #######################################################
        bscore = 0
        wscore = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == "black":
                    bscore += 1
                elif board[x][y] == "white":
                    wscore += 1
        return {"black": bscore, "white": wscore}

    def flip(self, board, side, xstart, ystart):
        #######################################################
        # - board: the status of the tiles in the current board
        # - side: the side of the placed disk
        # - xstart: x location of the the placed disk
        # - ystart: y location of the the placed disk
        #------------------------------------------------------
        # - return nothing and flip the disks on move
        #######################################################
        disks = self.getFlipDisks(board, side, xstart, ystart)
        board[xstart][ystart] = side
        for x, y in disks:
            board[x][y] = side

    def noMoreMove(self, board):
        #######################################################
        # - board: the status of the tiles in the current board
        #------------------------------------------------------
        # - return whether there is no more move  
        #######################################################
        return (not self.getValidMoves(board, self.playerSide) 
            and not self.getValidMoves(board, self.computerSide))

    def PlayerTurn(self, board):
        #######################################################
        # - board: the status of the tiles in the current board
        #------------------------------------------------------
        # - player chooses the position with mouse
        #######################################################
        if self.noMoreMove(board):
            self.status = 2
        x, y = pygame.mouse.get_pos()
        col, row = int((x - 20) / 50), int((y - 20) / 50)
        if self.isValidMove(board, self.playerSide, col, row):
            self.flip(board, self.playerSide, col, row)
            if self.getValidMoves(board, self.computerSide):
                self.turn = "computer" 

    def ComputerTurn(self, board, agent):
        #######################################################
        # - board: the status of the tiles in the current board
        #------------------------------------------------------
        # - cmoputer chooses the position with algorithm
        #######################################################
        if self.noMoreMove(board):
            self.status = 2
        pos = agent.greedy_choose(board)
        if pos:
            self.flip(board, self.computerSide, pos[0], pos[1])
            self.last_move = [pos[0], pos[1]]
        if self.getValidMoves(board, self.playerSide):
            self.turn = "player"

