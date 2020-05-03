from Pieces import *

# function to check whether a move to square (dx,dy)
# on <board> by <piece> is a legal chess move
def legal(board, piece, dx, dy):
    print(piece)
    x,y = piece.getLocation()

    path = "" # init direction that the piece is moving
    xChange, yChange = dx-x, dy-y
    distance = max(abs(xChange), abs(yChange))

    if type(piece) == knight :
        if not kLegal(piece, xChange, yChange): return False
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
def kLegal(piece, x, y):
    return (abs(x) == 1 and abs(y) == 2) or (abs(x) == 2 and abs(y) == 1)