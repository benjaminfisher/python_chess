''' Version 2 - Added Game Class.  Added flip to pieces and turnChange to Game
Added standard piece configuration to the Player class init.
'''

from graphics import *
from Board import *
from Pieces import *
from time import sleep

class Game:
    ''' Class to control the interaction of game play between the players
        and the board.
        '''
    def __init__(self, window):
        self.window = window
        self.board = board(window)

        self.Players = []
        self.over = False
        self.moveList = []
        self.selected = False # Holds coord for move in progress

    def deselect(self):
        if self.selected:
            for o in self.selected.obj:
                o.setWidth(1)
                o.setOutline(self.selected.outline)
            self.selected = False

    def inter(self, point):
        # is mouse click inside the board?
        if point.getX() >= 0 and point.getX() < 8\
           and point.getY() >= 0 and point.getY() < 8:
            # board coord of mouse click
            x, y = int(point.getX()), int(point.getY())
            # contents of clicked square
            get = self.board.occupied(point)

            # if a piece is selected (selected != False)
            # and the destination square is a legal move
            # (deselect selected piece if illegal) then move the piece
            # else store the piece in selected
            if self.selected:
                Legal = self.board.legal(self.selected, x, y)
                if Legal:
                    if type(Legal) != bool: Legal.capture()
                    self.selected._move(x, y)
                    self.deselect()
                    self.turnChange()
                else: self.deselect()
            else:
                if get and get.side == self.Players[0].side:
                    get.select()
                    self.selected = get

    def turnChange(self):
        sleep(0.5)

        for L in self.Players[0].labels:
            L.undraw()

        self.Players.reverse()

        for L in self.Players[0].labels:
            L.draw(self.window)

        cPlay = str.upper(self.Players[0].side)
        self.board.ticker.setFill(cPlay)
        self.board.feedback("Player: " + cPlay)

        ' Check EnPassant switches for current player '
        for p in self.Players[0].pieces:
            if type(p) == pawn:
                p.EP = False

        ''' Before flipping the board flashconfig refreshes
            all of the pieces current positions so they can
            be moved from the current positions to the new
            positions '''
        self.board.flashConfig()
        self.board.flipMatrix()
        self.board.printMatrix()

        for column in self.board.matrix:
            for piece in column:
                if piece: piece.flip()

        ' Store the pieces new positions '
        self.board.flashConfig()

    def Check(self, square):
        x, y = square.getX(), square.getY()
        
        for piece in self.Players[1].pieces:
            xChange = piece.position.getX() - x
            yChange = piece.position.getY() - y
            Path = self.board.path(xChange, yChange)
            dist = self.board.distance(xChange, yChange)
            
            if self.board.straight(xChange, yChange):
                if not self.board.obs(piece.position, square):
                    if dist < piece.footprint[path]:
                        return True
        return False

class Player:
    def __init__(self, game, side):
        self.game = game
        self.side = side
        self.pieces = []

        self.game.Players.append(self)

        if side == 'white':
            y, yp = 0, 1
            self.labels = game.board.Labels[0]
        else:
            y, yp = 7, 6
            self.labels = game.board.Labels[1]

        self.King = king(self.game.board, Point(4, y), self)
        self.pieces.append(self.King)

        for p in range(8):
            self.pieces.append(pawn(self.game.board, Point(p, yp), self))

        self.pieces.append(queen(self.game.board, Point(3, y), self))
        self.pieces.append(knight(self.game.board, Point(1, y), self))
        self.pieces.append(knight(self.game.board, Point(6, y), self))
        self.pieces.append(bishop(self.game.board, Point(2, y), self))
        self.pieces.append(bishop(self.game.board, Point(5, y), self))
        self.pieces.append(rook(self.game.board, Point(0, y), self))
        self.pieces.append(rook(self.game.board, Point(7, y), self))

        for p in self.pieces:
            p.place()

