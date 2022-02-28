#!/usr/bin/python
import sys

from PyQt5 import QtWidgets

from Snake import Snake
from Solver import Solver
from Solver import SearchNode


def main():
    # Create a snake game
    app = QtWidgets.QApplication(sys.argv)
    ex = Snake(-1, -1, -1, -1, -1, -1, True, False)


    # Solve it
    solver = Solver(ex)

    print(solver)
    solver.initUI()
    print("Found solution !")

    sol = solver.getSolution()

    solver.initUI()

    for state in sol:
        solver.snake = state
        solver.repaint()


    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
