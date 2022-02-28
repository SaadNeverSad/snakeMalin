#!/usr/bin/python
import sys

from PyQt5 import QtWidgets

from Snake import Snake


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Snake(-1, -1, -1, True)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
