from graphics import *

def main():
    win = GraphWin("Test", 100, 100)
    win.setBackground('green')
    pawnFile = Pixmap("images/blackqueen.gif")
    pawn = Image(Point(50,50),pawnFile)
    pawn.draw(win)
    wait = win.getMouse()

main()
