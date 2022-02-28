#!/usr/bin/python
import sys

from PyQt5 import QtWidgets

from Snake import Snake
from Solver import Solver


def main():
    # Create a snake game
    app = QtWidgets.QApplication(sys.argv)
    ex = Snake(-1, -1, -1, -1, -1, -1, True, False)

    # Solve it
    solver = Solver(ex)

    sol = solver.solution()

    solver.initUI()

    for state in sol:
        solver.snake = state
        solver.qp.repaint()


    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
