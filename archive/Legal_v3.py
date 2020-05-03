from Pieces import *
from chess import *

# function to check whether a move to square (dx,dy)
# on <board> by <piece> is a legal chess move
def legal(board, piece, dx, dy):

    x,y = piece.getLocation()
    xChange, yChange = dx-x, dy-y
    distance = max(abs(xChange), abs(yChange))

    if type(piece) == knight :
        if not kLegal(xChange, yChange): return False
        O = board.occupied(Point(dx,dy))
    else:
        # Test for straight lines on path
        if not ((abs(xChange) == abs(yChange)) \
           or (yChange and not xChange) \
           or (xChange and not yChange)): return False

        P = path(xChange, yChange)
        if not P: return False
        if distance > piece.footprint[P]: return False

        O = obs(board, Point(x,y), Point(dx,dy))
        if O == True: return False

    # Check capture legality and return the piece if captured
    if O:
        # pawn can't capture forward
        if type(piece) == pawn and P == 'f': return False
        if O.side is not piece.side: return O
        else: return False
    else:
        # pawn can only move fr or fl to capture
        if type(piece) == pawn and (P =='fr' or P == 'fl'):
            enPass = board.occupied(Point(dx, dy -1))
            if type(enPass) == pawn and enPass.EP:
                return enPass
            else: return False
        return True

# Function to check legality of knight moves
def kLegal(x, y):
    return (abs(x) == 1 and abs(y) == 2) or (abs(x) == 2 and abs(y) == 1)

def path(x,y):
    p = ""
    if y > 0: p = "f"       # Forward
    elif y < 0: p = "b"     # Back
    if x > 0: p = p + "r"   # Right
    elif x < 0: p = p + "l" # Left
    return p

def obs(board, start, end):
    sx, sy = int(start.getX()), int(start.getY())
    ex, ey = int(end.getX()), int(end.getY())

    if sx > ex: sx = sx - 1
    elif sx < ex: sx = sx + 1
    if sy > ey: sy = sy - 1
    elif sy < ey: sy = sy + 1

    square = board.occupied(Point(sx, sy))

    if sx == ex and sy == ey: return square
    if square: return True;
    else: return obs(board, Point(sx, sy), end)
