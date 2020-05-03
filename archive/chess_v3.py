''' Version 2 - Added Game Class.  Added flip to pieces and turnChange to Game
Added standard piece configuration to the Player class init.
'''

from graphics import *
from Legal import *
from Pieces import *
from button import Button

class Game:
    ''' Class to control the interaction of game play between the players
        and the board.
        '''
    def __init__(self, window, over = False, turn = "white",
    moveList = [], selected = False):
        self.window = window
        self.board = board(window)
        self.over = over
        self.turn = turn
        self.moveList = moveList
        self.selected = selected # Holds coord for move in progress

        self.ticker = Text(Point(4,8.5),"Testing")
        self.ticker.draw(self.window)

    def deselect(self):
        if self.selected:
            for o in self.selected.obj:
                o.setWidth(1)
                o.setOutline(self.selected.outline)
            self.selected = False

    def feedback(self, text):
        self.ticker.setText(text)

    def inter(self, point):
        # is mouse click inside the board?
        if point.getX()>=0 and point.getX()<8\
           and point.getY() >=0 and point.getY()<8:
            # board coord of mouse click
            x,y = int(point.getX()), int(point.getY())
            # contents of clicked square
            get = self.board.occupied(point)

            # if a piece is selected (selected != False)
            # and the destination square is a legal move
            # (deselect selected piece if illegal) then move the piece
            # else store the piece in selected
            if self.selected:
                dCheck = legal(self.board, self.selected, x, y)
                if dCheck:
                    if type(dCheck) != bool: dCheck.capture(self.board)
                    self.selected._move(self.board, x, y)
                    self.deselect()
                    self.turnChange()
                else: self.deselect()
            else:
                if get and get.side == self.turn:
                    get.select()
                    self.selected = get

    def turnChange(self):
        if self.turn == "white":
            self.turn = "black"; lx, ly = 0, 1
        else: self.turn = "white"; lx, ly = 1, 0

        self.board.matrix.reverse()
        for col in self.board.matrix:
            col.reverse()

        for i in self.board.matrix:
            for j in i:
                if j: j.flip()

        ' Swap board labels'
        for L in self.board.Labels[lx]: L.undraw()
        for L in self.board.Labels[ly]: L.draw(self.window)

class board:
    ''' Class to define the parameters of the chess board.
        The matrix is a nested set of lists storing the current
        configuration of the board.
        Selected piece is stored in select
        '''

    def __init__(self, window):
        self.window = window
        self.window.setCoords(0, -1, 8, 9)
        self.matrix = [] # storage list for the current state of the board
        self.Labels = [[],[]]

        for x in range(8):
            self.matrix.append([0,0,0,0,0,0,0,0])

        for x in range(0,8,2):
            for y in range(0,8,2):
                self.__drawSquare(Point(x,y), Point(x+1, y+ 1), 'grey5')
                self.__drawSquare(Point(x+1, y+1), Point(x+2, y+2), 'grey5')
                self.__drawSquare(Point(x+1, y), Point(x+2, y+1), 'lightgrey')
                self.__drawSquare(Point(x, y+1), Point(x+1, y+2), 'lightgrey')

        border = Line(Point(0,0), Point(0,8))
        border.setWidth(5)
        border.draw(self.window)

        # Set the row and column labels
        for i in range(1,9):
            bottomLabel = Text(Point(i-0.1, 0.11), chr(64+i))
            leftLabel = Text(Point(0.1, i-0.15), str(i))

            topLabel = Text(Point(8.1-i, 7.85), chr(64+i))
            rightLabel = Text(Point(7.95, 8.1-i), str(i))

            self.Labels[0].append(bottomLabel)
            self.Labels[0].append(leftLabel)
            self.Labels[1].append(topLabel)
            self.Labels[1].append(rightLabel)

        for L in self.Labels:
            for x in L:
                x.setSize(8)
                x.setStyle("bold")
                x.setTextColor("blue")

        for L in self.Labels[0]:
            L.draw(self.window)

        self.endB = Button(self.window, Point(7.5,-0.5), 1, 0.5, "END")
        self.endB.activate()

    def __drawSquare(self, Point1, Point2, color):
        square = Rectangle(Point1, Point2)
        square.setFill(color)
        square.draw(self.window)
        return square

# ========== END BOARD DRAWING ROUTINES ==========

    def occupied(self, point):
        if point:
            x,y = int(point.getX()), int(point.getY())
            return self.matrix[x][y]
        else: return False

class Player:
    def __init__(self, game, side):
        self.game = game
        self.side = side
        self.prison = [] # Storage for captured pieces
        self.active = False

        if side == 'white':
            y,yp = 0,1
        else:
            y,yp = 7,6

        self.pawns = []
        for p in range(8):
            self.pawns.append(pawn(Point(p,yp), side))

        for p in pawns:
            p.place(game.board)

        q1 = queen(Point(3,y), side)
        q1.place(game.board)

        k1 = king(Point(4,y), side)
        k1.place(game.board)

        rooks = [rook(Point(0,y), side),
                 rook(Point(7,y), side)]
        for r in rooks:
            r.place(game.board)

        knights = [knight(Point(1,y), side),
                   knight(Point(6,y), side)]
        for kn in knights:
            kn.place(game.board)

        bishops = [bishop(Point(2,y), side),
                   bishop(Point(5,y), side),]
        for b in bishops:
            b.place(game.board)
