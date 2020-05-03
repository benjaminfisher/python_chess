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