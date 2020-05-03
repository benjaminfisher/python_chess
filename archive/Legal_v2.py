from Pieces import *
from chess import *

# function to check whether a move to square (dx,dy)
# on <board> by <piece> is a legal chess move
def legal(board, piece, dx, dy):

    x,y = piece.getLocation()
    xChange, yChange = dx-x, dy-y
    distance = max(abs(xChange), abs(yChange))

    if type(piece) == knight :
        if not kLegal(piece, xChange, yChange): return False
    else:
        # Test for straight lines on path
        if not ((abs(xChange) == abs(yChange)) \
           or (yChange and not xChange) \
           or (xChange and not yChange)): return False

        P = path(xChange, yChange)

        if not P: return False
        if distance > piece.footprint[P]: return False

        # check to see if the path is obstructed
        if P == "f":
            for ySq in range(y+1, dy):
                if board.matrix[x][ySq]: return False

        elif P == "b":
            for ySq in range(y-1, dy, -1):
                if board.matrix[x][ySq]: return False

        elif P =='r':
            for xSq in range(x+1, dx):
                if board.matrix[xSq][y]: return False

        elif P =='l':
            for xSq in range(x-1, dx, -1):
                if board.matrix[xSq][y]: return False

        elif P == 'fr':
            ox,oy = x+1, y+1
            while ox < dx:
                if board.matrix[ox][oy]: return False
                ox,oy = ox+1, oy+1

        elif P == 'br':
            ox,oy = x+1, y-1
            while ox < dx:
                if board.matrix[ox][oy]: return False
                ox,oy = ox+1, oy-1

        elif P == 'bl':
            ox,oy = x-1, y-1
            while ox > dx:
                if board.matrix[ox][oy]: return False
                ox,oy = ox-1, oy-1

        elif path == 'fl':
            ox,oy = x-1, y+1
            while ox > dx:
                if board.matrix[ox][oy]: return False
                ox,oy = ox-1, oy+1

    # Check capture legality and return the piece if captured
    dest = board.occupied(Point(dx,dy))
    if dest:
        # pawn can't capture forward
        if type(piece) == pawn and P == 'f': return False
        if dest.side is not piece.side: return dest
        else: return False
    else:
        # pawn can only move fr or fl to capture
        if type(piece) == pawn and (P =='fr' or P == 'fl'):
            enPass = board.occupied(Point(dx, dy -1))
            if enPass and type(enPass)== pawn and enPass.EP:
                return enPass
            else: return False
        return True

# Function to check legality of knight moves
def kLegal(piece, x, y):
    return (abs(x) == 1 and abs(y) == 2) or (abs(x) == 2 and abs(y) == 1)

def path(x,y):
    p = ""
    if y > 0: p = "f"       # Forward
    elif y < 0: p = "b"     # Back
    if x > 0: p = p + "r"   # Right
    elif x < 0: p = p + "l" # Left
    return p

def obs(start, end):
    if start == end : return False
    sx, sy = start.getX(), start.getY()
    ex, ey = end.getX(), end.getY()

    occ = board.matrix[sx][sy]
    if occ : return occ
    elif sx > ex: sx = sx + 1
    elif sy > ey: sy = sy + 1
    elif sx < ex: sx = sx - 1
    elif sy < ey: sy = sy - 1

    obs(Point(sx, sy),end)



