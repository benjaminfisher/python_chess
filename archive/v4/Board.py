'''
Created on Jun 13, 2009

@author: Benjamin Fisher
'''

from graphics import *
from button import Button
from Pieces import *

class board:
    ''' Class to define the parameters of the chess board.
        The matrix is a nested set of lists storing the current
        configuration of the board.
        '''

    def __init__(self, window):
        self.window = window
        self.window.setCoords(0, -1, 8, 9)
        self.matrix = [] # storage list for the current state of the board
        self.Labels = [[], []]

        for x in range(8):
            self.matrix.append([0, 0, 0, 0, 0, 0, 0, 0])

        for x in range(0, 8, 2):
            for y in range(0, 8, 2):
                self.__drawSquare(Point(x, y), Point(x + 1, y + 1), 'grey5')
                self.__drawSquare(Point(x + 1, y + 1), Point(x + 2, y + 2), 'grey5')
                self.__drawSquare(Point(x + 1, y), Point(x + 2, y + 1), 'lightgrey')
                self.__drawSquare(Point(x, y + 1), Point(x + 1, y + 2), 'lightgrey')

        border = Line(Point(0, 0), Point(0, 8))
        border.setWidth(5)
        border.draw(self.window)

        self.ticker = Text(Point(2, -0.5), "")
        self.ticker.setSize(20)
        self.ticker.draw(self.window)

        # Set the row and column labels
        for i in range(1, 9):
            bLabel = Text(Point(i - 0.1, 0.11), chr(64 + i))
            lLabel = Text(Point(0.1, i - 0.15), str(i))

            tLabel = Text(Point(8.1 - i, 7.85), chr(64 + i))
            rLabel = Text(Point(7.95, 8.1 - i), str(i))

            self.Labels[0].append(bLabel)
            self.Labels[0].append(lLabel)
            self.Labels[1].append(tLabel)
            self.Labels[1].append(rLabel)

        for L in self.Labels:
            for x in L:
                x.setSize(8)
                x.setStyle("bold")
                x.setTextColor("blue")

        for L in self.Labels[0]:
            L.draw(self.window)

        self.endB = Button(self.window, Point(7.5, -0.5), 1, 0.5, "END")
        self.endB.activate()

    def __drawSquare(self, Point1, Point2, color):
        square = Rectangle(Point1, Point2)
        square.setFill(color)
        square.draw(self.window)
        return square

# ========== END BOARD DRAWING ROUTINES ==========

    def printMatrix(self):
        for column in self.matrix:
            line = ""
            for p in column:
                if p: line = line + p.side[0] + p.tx + " "
                else: line = line + "-- "
            print(line)
        print()

    def flipMatrix(self):
        self.matrix.reverse()
        for col in self.matrix:
            col.reverse()

    def flashConfig(self):
        for col in self.matrix:
            for p in col:
                if p != 0:
                    x, y = p.getLocation()
                    p.position = Point(x, y)

    def feedback(self, text):
        self.ticker.setText(text)

    def occupied(self, point):
        if point:
            x, y = int(point.getX()), int(point.getY())
            return self.matrix[x][y]
        else: return False

# ========== BEGIN LEGALITY ROUTINES ==========

    def legal(self, piece, dx, dy):
    # function to check whether a move to square (dx,dy)
    # by <piece> is a legal chess move

        x,y = piece.getLocation()
        xChange, yChange = dx-x, dy-y
        
        print(type(piece))
        if type(piece) == knight:
            if not self.kLegal(xChange, yChange): return False
            O = self.occupied(Point(dx,dy))
        else:
            if not self.straight(xChange, yChange): return False
            Path = self.path(xChange, yChange)

            if not Path: return False
            if self.distance(xChange, yChange) > piece.footprint[Path]:
                return False

            # O is the variable for storing path obstruction.
            O = self.obs(Point(x,y), Point(dx,dy))
            if O == True: return False

        if type(piece) == king and xChange > 1:
            if self.castleLegal(piece, dx): return True
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
                enPass = self.occupied(Point(dx, dy -1))
                if type(enPass) == pawn and enPass.EP:
                    return enPass
                else: return False
            return True

    def obs(self, start, end):
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

        square = self.occupied(Point(sx, sy))

        if sx == ex and sy == ey: return square
        if square: return True;
        else: return self.obs(Point(sx, sy), end)

    def findRook(self, king, x):
        ox = king.position.getX()
        if ox < x: return self.matrix[7][0]
        else: return self.matrix[0][0]

    def castleLegal(self, king, dx):
        rook = self.findRook(king, dx)
        kx = king.position.getX()

        if self.obs(king.position, rook.position) == True: return False
        elif king.moved or rook.moved: return False
        elif king.check: return False
        else: return True

    #    kx, rx = king.position.getX(), rook.position.getY()
    #    if kx < rx: s = 1
    #    else: s = -1
    #
    #    for sq in range(1,2):
    #        kx = kx + s
    #        if isCheck(self, Point(kx, ky))

# =======================================================================

    # Function to check legality of knight moves
    def kLegal(self, x, y):
        return (abs(x) == 1 and abs(y) == 2) or (abs(x) == 2 and abs(y) == 1)
    
    def distance(self, xChange, yChange):
        return max(abs(xChange), abs(yChange))
    
    def path(self, x,y):
        p = ""
        if y > 0: p = "f"       # Forward
        elif y < 0: p = "b"     # Back
        if x > 0: p = p + "r"   # Right
        elif x < 0: p = p + "l" # Left
        return p
    
    def straight(self, xChange, yChange):
        # Test for straight lines on path
        return ((abs(xChange) == abs(yChange)) \
           or (yChange and not xChange) \
           or (xChange and not yChange))
