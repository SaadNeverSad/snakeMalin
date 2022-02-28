#!/usr/bin/python
import sys

from PyQt5 import QtWidgets

from Snake import Snake
from Solver import Solver


def main():
    # Create a snake game
    app = QtWidgets.QApplication(sys.argv)
    ex = Snake(-1, -1, -1, -1, True)

    # Solve it
    # solver = Solver(ex)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
