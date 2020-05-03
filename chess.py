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

    def preMove(self, piece, destination):
        Temp = self.board.matrix
        Temp[piece.position.getX()][piece.position.getY()] = 0
        Temp[destination.getX()][destination.getY()] = piece
        return Temp

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
                Legal = legal(self.board.matrix, self.selected, x, y)
                if Legal:
                    TM = self.preMove(self.selected, Point(x,y))
                    Check = check(TM, self.Players[0].side, self.Players[0].King.position)
                    if not Check:
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

class Player:
    def __init__(self, game, side, K = True, Q = True, R = True, B = True, N = True, P = 8):
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

        if K:
            self.King = king(self.game.board, Point(4, y), self)
            self.pieces.append(self.King)

        if P:
            for p in range(P):
                self.pieces.append(pawn(self.game.board, Point(p, yp), self))
        if Q:
            self.pieces.append(queen(self.game.board, Point(3, y), self))
        if N:
            self.pieces.append(knight(self.game.board, Point(1, y), self))
            self.pieces.append(knight(self.game.board, Point(6, y), self))
        if B:
            self.pieces.append(bishop(self.game.board, Point(2, y), self))
            self.pieces.append(bishop(self.game.board, Point(5, y), self))
        if R:
            self.pieces.append(rook(self.game.board, Point(0, y), self))
            self.pieces.append(rook(self.game.board, Point(7, y), self))

        for p in self.pieces:
            p.place()

# ===== DEFINE LEGALITY FUNCTIONS =====

def legal(matrix, piece, dx, dy):
# function to check whether a move to square (dx,dy)
# by <piece> is a legal chess move

    x,y = piece.getLocation()
    xChange, yChange = dx-x, dy-y

    if type(piece) == knight:
        if not kLegal(xChange, yChange): return False
        O = occupied(matrix, Point(dx,dy))
    else:
        if not straight(xChange, yChange): return False
        Path = path(xChange, yChange)

        if not Path: return False
        if distance(xChange, yChange) > piece.footprint[Path]:
            return False

        # O is the variable for storing path obstruction.
        O = obs(matrix, Point(x,y), Point(dx,dy))
        if O == True: return False

    if type(piece) == king and xChange > 1:
        if castleLegal(matrix, piece, dx): return True
        else: return False

    # Check capture legality and return the piece if captured
    if O:
        # pawn can't capture forward
        if type(piece) == pawn and Path == 'f': return False
        # Check opposition of the piece in the destination square
        if O.side is not piece.side: return O
        else: return False
    else:
        # pawn can only move fr or fl to capture
        if type(piece) == pawn and (Path =='fr' or Path == 'fl'):
            enPass = occupied(Point(dx, dy -1))
            if type(enPass) == pawn and enPass.EP:
                return enPass
            else: return False
        return True

def occupied(matrix, point):
    if point:
        x, y = int(point.getX()), int(point.getY())
        return matrix[x][y]
    else: return False

def obs(matrix, start, end):
    ''' obs checks the path of the move for obstructing pieces.
        If there is a piece then True is returned, if not than False.
        Finally if there is a piece on the destination square than
        the piece is returned. '''

    sx, sy = int(start.getX()), int(start.getY())
    ex, ey = int(end.getX()), int(end.getY())

    if sx > ex: sx = sx - 1
    elif sx < ex: sx = sx + 1
    if sy > ey: sy = sy - 1
    elif sy < ey: sy = sy + 1

    square = occupied(matrix, Point(sx, sy))

    if sx == ex and sy == ey: return square
    if square: return True;
    else: return obs(matrix, Point(sx, sy), end)

def findRook(matrix, king, x):
    ox = king.position.getX()
    if ox < x: return matrix[7][0]
    else: return matrix[0][0]

def castleLegal(matrix, king, dx):
    rook = findRook(matrix, king, dx)
    kx = king.position.getX()

    if obs(matrix, king.position, rook.position) == True: return False
    elif king.moved or rook.moved: return False
    elif king.inCheck: return False
    else: return True

def check(matrix, side, square):
    x, y = square.getX(), square.getY()

    for col in matrix:
        for piece in col:
            if piece and piece.side != side:
                xChange = piece.position.getX() - x
                yChange = piece.position.getY() - y
##                Path = path(xChange, yChange)
##                dist = distance(xChange, yChange)

                if straight(xChange, yChange):
                    if not obs(matrix, piece.position, square):
                        if distance(xChange, yChange) < piece.footprint[path(xChange, yChange)]:
                            return True
    return False
# =======================================================================

# Function to check legality of knight moves
def kLegal(x, y):
    return (abs(x) == 1 and abs(y) == 2) or (abs(x) == 2 and abs(y) == 1)

def distance(xChange, yChange):
    return max(abs(xChange), abs(yChange))

def path(x,y):
    p = ""
    if y > 0: p = "f"       # Forward
    elif y < 0: p = "b"     # Back
    if x > 0: p = p + "r"   # Right
    elif x < 0: p = p + "l" # Left
    return p

def straight(xChange, yChange):
    # Test for straight lines on path
    return ((abs(xChange) == abs(yChange)) \
       or (yChange and not xChange) \
       or (xChange and not yChange))