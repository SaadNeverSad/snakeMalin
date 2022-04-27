#!/usr/bin/python
import sys, getopt

from PyQt5 import QtWidgets
from time import sleep

from Snake import Snake
from Solver import Solver
from GUI import GUI


def main(argv):
    # Default values
    target_score = 30
    play_speed = 25  # ms
    debug = False
    recursion = 5000

    # Get command line arguments
    try:
        opts, args = getopt.getopt(argv, "s:t:r:d", ["score=", "time=", "recursion=", "debug"])

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
        elif opt in ("-r", "--recursion"):
            recursion = int(arg)

    # Create a snake game
    print("Generating a snake game with target score of " + str(target_score) + "...\n")
    app = QtWidgets.QApplication(sys.argv)
    ex = Snake(-1, -1, -1, -1, -1, -1, True, False)

    # Solve it
    solver = Solver(ex, target_score, debug, recursion)
    sol = solver.getSolution()

    # Create a GUI
    ui = GUI(sol, play_speed)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv[1:])
