from graphics import *
from button import Button

class board:
    ''' Class to define the parameters of the chess board.
        The matrix is a nested set of lists storing the current
        configuration of the board.
        Selected piece is stored in select
        '''

    def __init__(self, window, selected = False, enPassant = False):
        self.window = window
        self.window.setCoords(0, -1, 8, 9)
        self.selected = selected # Holds coord for move in progress

        self.matrix = [] # storage list for the current state of the board
        for x in range(8):
            self.matrix.append([0,0,0,0,0,0,0,0])

        self.moveList = [] # List of previous moves

        self.endB = Button(self.window, Point(7.5,-0.5), 1, 0.5, "END")

    def draw(self):
        for x in range(0,8,2):
            for y in range(0,8,2):
                self.__drawSquare(Point(x,y), Point(x+1, y+ 1), 'grey5')
                self.__drawSquare(Point(x+1, y+1), Point(x+2, y+2), 'grey5')
                self.__drawSquare(Point(x+1, y), Point(x+2, y+1), 'lightgrey')
                self.__drawSquare(Point(x, y+1), Point(x+1, y+2), 'lightgrey')

        border = Line(Point(0,0), Point(0,8))
        border.setWidth(5)
        border.draw(self.window)

        # Draw the row and column labels
        f = True
        for i in range(0,8):
            xlabel = Text(Point(i+0.9, 0.11), chr(65+i))
            ylabel = Text(Point(0.1, i+0.85), str(i+1))
            xlabel.setSize(8); ylabel.setSize(8)

            if f:
                xlabel.setFill('white')
                ylabel.setFill('white')
            if f: f = False
            else: f = True

            xlabel.draw(self.window)
            ylabel.draw(self.window)

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

    def deselect(self):
        if self.selected:
            for o in self.selected.obj:
                o.setWidth(1)
                o.setOutline(self.selected.outline)
            self.selected = False

#================================================================

class Player:
    def __init__(self, board, side):
        self.side = side
        self.prison = [] # Storage for captured pieces
        self.active = False
        self.board = board

    def Turn(self):
        self.active = True

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
            if self.board.selected:
                dCheck = self.legal(self.board, self.board.selected, x, y)
                if dCheck:
                    if type(dCheck) != bool: dCheck.capture(self.board)
                    self.board.selected._move(self.board, x, y)
                    self.board.deselect()
                else: self.board.deselect()
            else:
                if get:
                    get.select()
                    self.board.selected = get

    # function to check whether a move to square (dx,dy)
    # on <board> by <piece> is a legal chess move
    def legal(self, board, piece, dx, dy):
        x,y = piece.getLocation()

        path = "" # init direction that the piece is moving
        xChange, yChange = dx-x, dy-y
        distance = max(abs(xChange), abs(yChange))

        if type(piece) == knight :
            if not self.kLegal(piece, xChange, yChange): return False
        else:
            # Test for straight lines on path
            if not ((abs(xChange) == abs(yChange)) \
               or (yChange and not xChange) \
               or (xChange and not yChange)): return False

            # if piece is black reverse vertical for the path
            if piece.side == 'black':
                yChange = yChange*-1

            # check if destination (dx, dy) is in the footprint of the piece
            if yChange > 0: path = "f"          # Forward
            elif yChange < 0: path = "b"        # Back
            if xChange > 0: path = path + "r"   # Right
            elif xChange < 0: path = path + "l" # Left
            if not path: return False           # same piece selected

            if distance > piece.footprint[path]: return False

            # check to see if the path is obstructed
            if (path == "f" and piece.side == 'white') or \
               (path == "b" and piece.side == 'black'):
                for ySq in range(y+1, dy):
                    if board.matrix[x][ySq]: return False

            elif (path == "f" and piece.side == 'black') or \
               (path == "b" and piece.side == 'white'):
                for ySq in range(y-1, dy, -1):
                    if board.matrix[x][ySq]: return False

            elif path =='r':
                for xSq in range(x+1, dx):
                    if board.matrix[xSq][y]: return False

            elif path =='l':
                for xSq in range(x-1, dx, -1):
                    if board.matrix[xSq][y]: return False

            elif (path == 'fr' and piece.side == 'white') or \
               (path == 'br' and piece.side == 'black'):
                ox,oy = x+1, y+1
                while ox < dx:
                    if board.matrix[ox][oy]: return False
                    ox,oy = ox+1, oy+1

            elif (path == 'br' and piece.side == 'white') or \
               (path == 'fr' and piece.side == 'black'):
                ox,oy = x+1, y-1
                while ox < dx:
                    if board.matrix[ox][oy]: return False
                    ox,oy = ox+1, oy-1

            elif (path == 'bl' and piece.side == 'white') or \
               (path == 'fl' and piece.side == 'black'):
                ox,oy = x-1, y-1
                while ox > dx:
                    if board.matrix[ox][oy]: return False
                    ox,oy = ox-1, oy-1

            elif (path == 'fl' and piece.side == 'white') or \
               (path == 'bl' and piece.side == 'black'):
                ox,oy = x-1, y+1
                while ox > dx:
                    if board.matrix[ox][oy]: return False
                    ox,oy = ox-1, oy+1

        # Check capture legality and return the piece if captured
        dest = board.occupied(Point(dx,dy))
        if dest:
            # pawn can't capture forward
            if type(piece) == pawn and path == 'f': return False
            if dest.side is not piece.side: return dest
            else: return False
        else:
            # pawn can only move fr or fl to capture
            if type(piece) == pawn and (path =='fr' or path == 'fl'):
                if piece.side == 'white': dy = dy -1
                else: dy = dy + 1
                enPass = board.occupied(Point(dx, dy))
                if enPass and enPass.EP: return enPass
                else: return False
            return True

    # Function to check legality of knight moves
    def kLegal(self, piece, x, y):
        return (abs(x) == 1 and abs(y) == 2) or (abs(x) == 2 and abs(y) == 1)

#================================================================
class Piece:
    ''' Piece is a base class for chess pieces with a subclass
    for each individual piece.  The parameters are as follows:
    start = starting location on the board
    side = pieces alignment (black/white)
    position = current location on the chess board
    captured = whether the piece has been captured

    the footprint library is a definition of legal moves
    in number of squares per direction (except knights):
    (f=forward, b = back, l=left, r=right)
    '''

    def __init__(self, start, side, captured = False):
        self.side = side
        self.captured = captured
        self.position = start

        self.color = self.side
        if self.color == 'black': self.outline = 'white'
        else: self.outline = 'black'

    def getSide(self):
        return self.side

    def getLocation(self):
        return (self.position.getX(), self.position.getY())

    def select(self):
        if type(self.obj) == Image:
            self.obj = Image(self.getLocation(),self.sfile)
        for o in self.obj:
            o.setWidth(2)
            o.setOutline('red')

    def move(self, board, x, y):
        ox, oy = self.getLocation()
        self.moved = True

        # Set the place holders in the matrix and the object position
        # to the new configuration
        board.matrix[x][y] = self
        board.matrix[ox][oy] = 0
        self.position = Point(x,y)

        # Move the graphical representation of the piece
        dx, dy = x - ox, y - oy
        for o in self.obj:
                o.move(dx,dy)


    def place(self, board):
        # Method to put a piece on the board
        # Note: Piece must be initialized before it can be placed
        if type(self.obj) == Image:
            self.obj.draw(board.window)
        else:
            for o in self.obj:
                o.draw(board.window)
        self.start = self.position.clone()
        x,y = self.getLocation()
        board.matrix[x][y] = self

    def capture(self, board):
        self.captured = True
        x,y = self.getLocation()
        board.matrix[x][y] = 0
        if type(self.obj) == Image:
            self.obj.undraw()
        else:
            for o in self.obj:
                o.undraw()

# ========== BEGIN PIECE DEFINITIONS ==========

class pawn(Piece):
    def __init__(self, location, side):
        Piece.__init__(self, location, side)
        self.EP = False
        self.footprint = {'f':2, 'fr':1, 'r':0, 'br':0,
                          'b':0, 'bl':0, 'l':0, 'fl':1}

        x, y = self.getLocation()

##        self.file = Pixmap("images/whitepawn.gif")
##        self.sfile = Pixmap("images/s_pawn.gif")
##        self.obj = Image(Point(x,y),self.file)

        self.obj = [Polygon(Point(x+0.3, y+0.3), Point(x+0.7, y+0.3),
                       Point(x+0.55, y+0.4), Point(x+0.45, y+0.4)),
                       Rectangle(Point(x+0.45, y+0.8), Point(x+0.55, y+0.4)),
                       Circle(Point(x+0.5, y+0.8),0.1)]
        for o in self.obj:
            o.setFill(self.color)
            o.setOutline(self.outline)

    def _move(self, board, x, y):
        # check legality of en Passant capture
        if abs(y - self.position.getY()) > 1:
            self.EP = True
        else: self.EP = False

        # disable 1rst move 2 step
        self.footprint['f'] = 1
        return self.move(board, x, y)
#==================================================================

class rook(Piece):
    def __init__(self, location, side):
        Piece.__init__(self, location, side)
        self.footprint = {'f':7, 'fr':0, 'r':7, 'br':0,
                          'b':7, 'bl':0, 'l':7, 'fl':0}

        x, y = self.getLocation()

        self.obj = [Polygon(Point(x+0.2, y+0.1), Point(x+0.8, y+0.1),
                       Point(x+0.6, y+0.25), Point(x+0.4, y+0.25)),
                       Rectangle(Point(x+0.4, y+0.5), Point(x+0.6, y+0.25)),
                       Polygon(Point(x+0.25, y+0.5), Point(x+0.25, y+0.9),
                               Point(x+0.35, y+0.9), Point(x+0.35, y+0.7),
                               Point(x+0.45, y+0.7), Point(x+0.45, y+0.9),
                               Point(x+0.55, y+0.9), Point(x+0.55, y+0.7),
                               Point(x+0.65, y+0.7), Point(x+0.65, y+0.9),
                               Point(x+0.75, y+0.9), Point(x+0.75, y+0.5))]
        for o in self.obj:
            o.setFill(self.color)
            o.setOutline(self.outline)

    def _move(self, board, x, y):
        return self.move(board, x, y)
#==================================================================

class knight(Piece):
    def __init__(self, location, side):
        Piece.__init__(self, location, side)
        self.footprint = {}

        x, y = self.getLocation()

        self.obj = [Polygon(Point(x+0.2, y+0.1), Point(x+0.8, y+0.1),
                            Point(x+0.6, y+0.25), Point(x+0.4, y+0.25)),
                    Rectangle(Point(x+0.4, y+0.5), Point(x+0.6, y+0.25)),
                    Polygon(Point(x+0.4, y+0.5), Point(x+0.3, y+0.55),
                            Point(x+0.3, y+0.9), Point(x+0.4, y+0.78),
                            Point(x+0.8, y+0.75), Point(x+0.8, y+0.6),
                            Point(x+0.6, y+0.5))]
        for o in self.obj:
            o.setFill(self.color)
            o.setOutline(self.outline)

    def _move(self, board, x, y):
        return self.move(board, x, y)
#==================================================================

class bishop(Piece):
    def __init__(self, location, side):
        Piece.__init__(self, location, side)
        self.footprint = {'f':0, 'fr':7, 'r':0, 'br':7,
                          'b':0, 'bl':7, 'l':0, 'fl':7}

        x, y = self.getLocation()

        self.obj = [Polygon(Point(x+0.2, y+0.1), Point(x+0.8, y+0.1),
                            Point(x+0.6, y+0.25), Point(x+0.4, y+0.25)),
                    Rectangle(Point(x+0.4, y+0.5), Point(x+0.6, y+0.25)),
                    Polygon(Point(x+0.3, y+0.5), Point(x+0.5, y+0.9),
                            Point(x+0.7, y+0.5)),
                    Polygon(Point(x+0.4, y+0.5), Point(x+0.5, y+0.7),
                            Point(x+0.6, y+0.5))]
        for o in self.obj:
            o.setFill(self.color)
            o.setOutline(self.outline)

    def _move(self, board, x, y):
        return self.move(board, x, y)
#==================================================================

class queen(Piece):
    def __init__(self, location, side):
        Piece.__init__(self, location, side)
        self.footprint = {'f':7, 'fr':7, 'r':7, 'br':7,
                          'b':7, 'bl':7, 'l':7, 'fl':7}

        x, y = self.getLocation()

        self.obj = [Polygon(Point(x+0.2, y+0.1), Point(x+0.8, y+0.1),
                            Point(x+0.6, y+0.25), Point(x+0.4, y+0.25)),
                    Rectangle(Point(x+0.4, y+0.6), Point(x+0.6, y+0.25)),
                    Polygon(Point(x+0.4, y+0.6), Point(x+0.2, y+0.7),
                            Point(x+0.5, y+0.9), Point(x+0.8, y+0.7),
                            Point(x+0.6, y+0.6))]
        for o in self.obj:
            o.setFill(self.color)
            o.setOutline(self.outline)

    def _move(self, board, x, y):
        return self.move(board, x, y)
#==================================================================

class king(Piece):
    def __init__(self, location, side):
        Piece.__init__(self, location, side)
        self.check = False
        self.footprint = {'f':1, 'fr':1, 'r':2, 'br':1,
                          'b':1, 'bl':1, 'l':2, 'fl':1}

        x, y = self.getLocation()

        self.obj = [Polygon(Point(x+0.2, y+0.1), Point(x+0.8, y+0.1),
                            Point(x+0.6, y+0.25), Point(x+0.4, y+0.25)),
                    Rectangle(Point(x+0.4, y+0.6), Point(x+0.6, y+0.25)),
                    Polygon(Point(x+0.4, y+0.6), Point(x+0.2, y+0.7),
                            Point(x+0.5, y+0.9), Point(x+0.8, y+0.7),
                            Point(x+0.6, y+0.6)),
                    Rectangle(Point(x+0.49, y+0.85), Point(x+0.51, y+0.65)),
                    Rectangle(Point(x+0.44, y+0.8), Point(x+0.55, y+0.78))]
        for o in self.obj:
            o.setFill(self.color)
            o.setOutline(self.outline)

    def _move(self, board, x, y):
        # disable castle ability
        self.footprint['r'], self.footprint['l'] = 1,1
        return self.move(board, x, y)

    def _castle(self, board, side):
        y = self.position.getY()

        # find the castling rook
        if side == 'r': x = 7
        elif side == 'l': x = 0
        r = board.matrix[x][y]

#==================================================================
