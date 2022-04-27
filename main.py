#!/usr/bin/python
import sys

from PyQt5 import QtWidgets
from time import sleep

from Snake import Snake
from Solver import Solver
from GUI import GUI


def main():
    # Create a snake game
    app = QtWidgets.QApplication(sys.argv)
    ex = Snake(-1, -1, -1, -1, -1, -1, True, False)

    # Solve it
    target_score = 20
    solver = Solver(ex, target_score)
    print("Found a solution !")
    sol = solver.getSolution()

    # Create a GUI
    play_speed = 10  # ms
    ui = GUI(sol, play_speed)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
