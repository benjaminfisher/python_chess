## Executable to start a new chess game
## Compatible with Python versions 2.6 - 3.0
## Author: Benjamin Fisher

from graphics import *
from chess import *

def main():
    win = GraphWin('Python Chess', 500, 550)
    win.setBackground('green')

    myGame = Game(win)

    player1 = Player(myGame, 'white')
    player2 = Player(myGame, 'black')

    while not myGame.over:
        click = win.checkMouse()
        if click: myGame.inter(click)
        if click and myGame.board.endB.clicked(click): myGame.over = True

    win.close()

main()


