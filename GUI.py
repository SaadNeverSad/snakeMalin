from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt


class GUI(QtWidgets.QWidget):
    def __init__(self, snakes, speed):
        super(GUI, self).__init__()

        # Game parameters
        self.windowSize = 900  # size of the gui window, in pixel
        self.squareSize = 24  # size of one position, in pixel
        self.timer = QtCore.QBasicTimer()  # used to track the time
        self.speed = speed  # length of the delay between each move in ms (lower --> faster)
        self.highscore = 0
        self.state = 0
        self.stateNb = len(snakes)
        self.snakes = snakes

        # State parameters
        self.fruits = snakes[0].fruits
        self.y = snakes[0].y
        self.x = snakes[0].x
        self.snakeArray = snakes[0].snakeArray
        self.score = snakes[0].score
        self.rocks = snakes[0].rocks

        self.qp = QtGui.QPainter()
        self.initUI()

    def nextState(self):
        self.state += 1
        self.fruits = self.snakes[self.state].fruits
        self.y = self.snakes[self.state].y
        self.x = self.snakes[self.state].x
        self.snakeArray = self.snakes[self.state].snakeArray
        self.score = self.snakes[self.state].score
        self.rocks = self.snakes[self.state].rocks

    def initUI(self):
        self.setStyleSheet("QWidget { background: #A9F5D0 }")
        self.setFixedSize(self.windowSize, self.windowSize)
        self.setWindowTitle('Snake')
        self.show()

    def paintEvent(self, event):
        self.qp.begin(self)
        self.scoreBoard()
        self.drawRocks(self.qp)
        self.drawFood()
        self.drawSnake(self.qp)
        self.scoreText(event)
        self.timer.start(self.speed, self)
        self.qp.end()

    def keyPressEvent(self, e):
        # Close game with Escape
        if e.key() == Qt.Key_Escape:
            self.close()

    # Affiche le scoreboard
    def scoreBoard(self):
        self.qp.setPen(Qt.NoPen)
        self.qp.setBrush(QtGui.QColor(25, 80, 0, 160))
        self.qp.drawRect(0, 0, self.windowSize, self.squareSize)

    # Affiche le score
    def scoreText(self, event):
        self.qp.setPen(QtGui.QColor(255, 255, 255))
        self.qp.setFont(QtGui.QFont('Arial', 10))
        self.qp.drawText(8, 17, "SCORE: " + str(self.score))
        self.qp.drawText(195, 17, "HIGHSCORE: " + str(self.highscore))

    def drawRocks(self, qp):
        qp.setBrush(QtGui.QColor(45, 45, 45, 255))
        # Draw rocks on the map
        for rock in self.rocks:
            qp.drawRect(rock["x"], rock["y"], self.squareSize, self.squareSize)

    def drawFood(self):
        if self.fruits["food1_type"] == "Pomme":
            self.qp.setBrush(QtGui.QColor(80, 180, 0, 160))  # Selectionne un carré vert pour la pomme
        else:
            self.qp.setBrush(QtGui.QColor(255, 0, 0, 160))  # Selectionne un carré rouge pour la cerise
        self.qp.drawRect(self.fruits["food1_x"], self.fruits["food1_y"], self.squareSize, self.squareSize)

        if self.fruits["food2_type"] == "Pomme":
            self.qp.setBrush(QtGui.QColor(80, 180, 0, 160))  # Selectionne un carré vert pour la pomme
        else:
            self.qp.setBrush(QtGui.QColor(255, 0, 0, 160))  # Selectionne un carré rouge pour la cerise
        self.qp.drawRect(self.fruits["food2_x"], self.fruits["food2_y"], self.squareSize, self.squareSize)

    # draws each component of the snake
    def drawSnake(self, qp):
        qp.setPen(Qt.NoPen)
        qp.setBrush(QtGui.QColor(255, 80, 0, 255))
        for i in self.snakeArray:
            qp.drawRect(i[0], i[1], self.squareSize, self.squareSize)

    # game thread
    def timerEvent(self, event):
        if self.state == self.stateNb - 1:
            self.timer.stop()

        else:
            if event.timerId() == self.timer.timerId():
                self.nextState()
                self.repaint()
            else:
                QtWidgets.QFrame.timerEvent(self, event)