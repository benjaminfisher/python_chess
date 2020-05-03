from graphics import *
from button import Button
from chess import *
from Pieces import *

def main():
    win = GraphWin('Python Chess', 500, 550)
    win.setBackground('green')

    myGame = Game(win)

    P1 = Player(myGame, 'white')
    P2 = Player(myGame, 'black')

    for p in P1.pieces:
        print(type(p))
        if type(p) != king or type(p) != rook:
            p.capture()

    for p in P2.pieces:
        if type(p) != king or type(p) != rook:
            p.capture()

    while not myGame.over:
        click = win.checkMouse()
        if click: myGame.inter(click)
        if click and myGame.board.endB.clicked(click): myGame.over = True

    win.close()

main()
