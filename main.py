#!/usr/bin/python
import sys, getopt

from PyQt5 import QtWidgets
from time import sleep

from Snake import Snake
from Solver import Solver
from GUI import GUI


def main(argv):
    # Default values
    target_score = 20
    play_speed = 10  # ms
    debug = False

    # Get command line arguments
    try:
        opts, args = getopt.getopt(argv, "s:t:d", ["score=", "time=", "debug"])

    except getopt.GetoptError:
        print('main.py -s <target_score> -t <time_delay_between_each_move> (OPTIONAL : -d to debug the A* solver)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -s <target_score> -t <time_delay_between_each_move>')
            sys.exit()
        elif opt in ("-s", "--score"):
            target_score = int(arg)
        elif opt in ("-t", "--time"):
            play_speed = int(arg)
        elif opt in ("-d", "--debug"):
            debug = True

    # Create a snake game
    print("Generating a snake game with target score of " + str(target_score) + "...\n")
    app = QtWidgets.QApplication(sys.argv)
    ex = Snake(-1, -1, -1, -1, -1, -1, True, False)

    # Solve it
    solver = Solver(ex, target_score, debug)
    print("Found a solution !")
    sol = solver.getSolution()

    # Create a GUI
    ui = GUI(sol, play_speed)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv[1:])
