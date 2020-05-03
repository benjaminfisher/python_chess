from graphics import *

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
        self.captured = captured
        self.side = side
        self.position = start

        if self.side == 'black': self.outline = 'white'
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

    def flip(self):
        rev = [7,5,3,1,-1,-3,-5,-7]
        x,y = self.getLocation()
        dx,dy = rev[x],rev[y]

        self.position = Point(x+dx, y+dy)
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
        self.tx = "p"
        self.EP = False
        self.footprint = {'f':2, 'fr':1, 'r':0, 'br':0,
                          'b':0, 'bl':0, 'l':0, 'fl':1}

        x, y = self.getLocation()

        self.obj = [Polygon(Point(x+0.3, y+0.3), Point(x+0.7, y+0.3),
                       Point(x+0.55, y+0.4), Point(x+0.45, y+0.4)),
                       Rectangle(Point(x+0.45, y+0.8), Point(x+0.55, y+0.4)),
                       Circle(Point(x+0.5, y+0.8),0.1)]
        for o in self.obj:
            o.setFill(self.side)
            o.setOutline(self.outline)

    def _move(self, board, x, y):
        # check legality of en Passant capture
        if y - self.position.getY() > 1:
            self.EP = True

        # disable 1rst move 2 step
        self.footprint['f'] = 1
        return self.move(board, x, y)
#==================================================================

class rook(Piece):
    def __init__(self, location, side):
        Piece.__init__(self, location, side)
        self.tx = 'R'
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
            o.setFill(self.side)
            o.setOutline(self.outline)

    def _move(self, board, x, y):
        return self.move(board, x, y)
#==================================================================

class knight(Piece):
    def __init__(self, location, side):
        Piece.__init__(self, location, side)
        self.tx = "N"
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
            o.setFill(self.side)
            o.setOutline(self.outline)

    def _move(self, board, x, y):
        return self.move(board, x, y)
#==================================================================

class bishop(Piece):
    def __init__(self, location, side):
        Piece.__init__(self, location, side)
        self.tx = "B"
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
            o.setFill(self.side)
            o.setOutline(self.outline)

    def _move(self, board, x, y):
        return self.move(board, x, y)
#==================================================================

class queen(Piece):
    def __init__(self, location, side):
        Piece.__init__(self, location, side)
        self.tx = "Q"
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
            o.setFill(self.side)
            o.setOutline(self.outline)

    def _move(self, board, x, y):
        return self.move(board, x, y)
#==================================================================

class king(Piece):
    def __init__(self, location, side):
        Piece.__init__(self, location, side)
        self.tx = "K"
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
            o.setFill(self.side)
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