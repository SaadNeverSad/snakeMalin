#!/usr/bin/python
import sys
from random import randrange

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt


class Snake(QtWidgets.QWidget):
    def __init__(self):
        super(Snake, self).__init__()
        self.windowSize = 900
        self.squareSize = 24
        self.speed = 100
        self.Food1Placed = False
        self.Food1Type = "Pomme"
        self.Food2Placed = False
        self.Food2Type = "Pomme"
        self.rocks = []
        self.rocksGenerated = False
        self.rockNumber = 30  # number of rocks to be generated
        self.isOver = False
        self.isPaused = False
        self.foody = 0
        self.foodx = 0
        self.y = self.squareSize * 4
        self.x = self.squareSize
        self.snakeArray = [[self.x, self.y], [self.x - self.squareSize, self.y], [self.x - self.squareSize*2, self.y]]
        self.timer = QtCore.QBasicTimer()
        self.highscore = 0
        self.gameOverText = ""
        self.spaceText = ""
        self.qp = QtGui.QPainter()
        self.initUI()

    def initUI(self):
        self.newGame()
        self.setStyleSheet("QWidget { background: #A9F5D0 }")
        self.setFixedSize(self.windowSize, self.windowSize)
        self.setWindowTitle('Snake')
        self.show()

    def paintEvent(self, event):
        self.qp.begin(self)
        self.scoreBoard()
        self.drawRocks(self.qp)
        self.placeFood()
        self.drawSnake(self.qp)
        self.scoreText(event)
        if self.isOver:
            self.gameOver(event)
        self.qp.end()

    def keyPressEvent(self, e):
        if not self.isPaused:
            # print "inflection point: ", self.x, " ", self.y
            if e.key() == Qt.Key_Up and self.lastKeyPress != 'UP' and self.lastKeyPress != 'DOWN':
                self.direction("UP")
                self.lastKeyPress = 'UP'
            elif e.key() == Qt.Key_Down and self.lastKeyPress != 'DOWN' and self.lastKeyPress != 'UP':
                self.direction("DOWN")
                self.lastKeyPress = 'DOWN'
            elif e.key() == Qt.Key_Left and self.lastKeyPress != 'LEFT' and self.lastKeyPress != 'RIGHT':
                self.direction("LEFT")
                self.lastKeyPress = 'LEFT'
            elif e.key() == Qt.Key_Right and self.lastKeyPress != 'RIGHT' and self.lastKeyPress != 'LEFT':
                self.direction("RIGHT")
                self.lastKeyPress = 'RIGHT'
            elif e.key() == Qt.Key_P:
                self.pause()
        elif e.key() == Qt.Key_P:
            self.start()
        elif e.key() == Qt.Key_Space:
            self.newGame()
        elif e.key() == Qt.Key_Escape:
            self.close()

    def newGame(self):
        self.y = self.squareSize * 4
        self.x = self.squareSize
        self.snakeArray = [[self.x, self.y], [self.x - self.squareSize, self.y], [self.x - self.squareSize * 2, self.y]]
        self.lastKeyPress = 'RIGHT'
        self.score = 0
        if not self.rocksGenerated:
            self.generateRocks(self.rockNumber)
        self.start()

    def pause(self):
        self.isPaused = True
        self.timer.stop()
        self.update()

    def start(self):
        self.isPaused = False
        self.timer.start(self.speed, self)
        self.update()

    def direction(self, dir):
        if dir == "DOWN" and self.checkStatus(self.x, self.y + self.squareSize):
            self.y += self.squareSize
            self.repaint()
            self.snakeArray.insert(0, [self.x, self.y])
        elif dir == "UP" and self.checkStatus(self.x, self.y - self.squareSize):
            self.y -= self.squareSize
            self.repaint()
            self.snakeArray.insert(0, [self.x, self.y])
        elif dir == "RIGHT" and self.checkStatus(self.x + self.squareSize, self.y):
            self.x += self.squareSize
            self.repaint()
            self.snakeArray.insert(0, [self.x, self.y])
        elif dir == "LEFT" and self.checkStatus(self.x - self.squareSize, self.y):
            self.x -= self.squareSize
            self.repaint()
            self.snakeArray.insert(0, [self.x, self.y])

    def scoreBoard(self):
        self.qp.setPen(Qt.NoPen)
        self.qp.setBrush(QtGui.QColor(25, 80, 0, 160))
        self.qp.drawRect(0, 0, 900, self.squareSize)

    def scoreText(self, event):
        self.qp.setPen(QtGui.QColor(255, 255, 255))
        self.qp.setFont(QtGui.QFont('Decorative', 10))
        self.qp.drawText(8, 17, "SCORE: " + str(self.score))
        self.qp.drawText(195, 17, "HIGHSCORE: " + str(self.highscore))

    def gameOver(self, event):
        self.highscore = max(self.highscore, self.score)

    def checkStatus(self, x, y):
        for rock in self.rocks:
            if x == rock["x"] and y == rock["y"]:
                self.pause()
                self.isPaused = True
                self.isOver = True
                return False
        if y > self.windowSize - self.squareSize or x > self.windowSize - self.squareSize or x < 0 or y < self.squareSize:
            self.pause()
            self.isPaused = True
            self.isOver = True
            return False
        elif self.snakeArray[0] in self.snakeArray[1:len(self.snakeArray)]:
            self.pause()
            self.isPaused = True
            self.isOver = True
            return False
        elif self.y == self.food1y and self.x == self.food1x:
            self.Food1Placed = False
            self.score += self.getScoreType(1)
            return True
        elif self.y == self.food2y and self.x == self.food2x:
            self.Food2Placed = False
            self.score += self.getScoreType(2)
            return True
        elif self.score >= 573:
            print("you win!")

        self.snakeArray.pop()

        return True

    # generates n rocks
    def generateRocks(self, n=10):
        for i in range(n):
            rock = {"x": randrange(1, int(self.windowSize / self.squareSize)) * self.squareSize,
                    "y": randrange(1, int(self.windowSize / self.squareSize)) * self.squareSize}
            self.rocks.append(rock)
        self.rocksGenerated = True

    def drawRocks(self, qp):
        qp.setBrush(QtGui.QColor(45, 45, 45, 255))
        # Draw rocks on the map
        for rock in self.rocks:
            qp.drawRect(rock["x"], rock["y"], self.squareSize, self.squareSize)

    # places the food when theres none on the board
    def placeFood(self):
        if not self.Food1Placed:
            self.food1x = randrange(1, int(self.windowSize / self.squareSize)) * self.squareSize
            self.food1y = randrange(1, int(self.windowSize / self.squareSize)) * self.squareSize
            rand = randrange(1, 3)
            if rand == 2:
                self.Food1Type = "Pomme"
            else:
                self.Food1Type = "Cerise"
            if not [self.food1x, self.food1y] in self.snakeArray:
                self.Food1Placed = True
        if not self.Food2Placed:
            self.food2x = randrange(1, int(self.windowSize / self.squareSize)) * self.squareSize
            self.food2y = randrange(1, int(self.windowSize / self.squareSize)) * self.squareSize
            rand = randrange(1, 3)
            if rand == 2:
                self.Food2Type = "Pomme"
            else:
                self.Food2Type = "Cerise"
            if not [self.food2x, self.food2y] in self.snakeArray:
                self.Food2Placed = True

        if self.Food1Type == "Pomme":
            self.qp.setBrush(QtGui.QColor(80, 180, 0, 160))
        else:
            self.qp.setBrush(QtGui.QColor(255, 0, 0, 160))
        self.qp.drawRect(self.food1x, self.food1y, self.squareSize, self.squareSize)

        if self.Food2Type == "Pomme":
            self.qp.setBrush(QtGui.QColor(80, 180, 0, 160))
        else:
            self.qp.setBrush(QtGui.QColor(255, 0, 0, 160))
        self.qp.drawRect(self.food2x, self.food2y, self.squareSize, self.squareSize)

    # draws each component of the snake
    def drawSnake(self, qp):
        qp.setPen(Qt.NoPen)
        qp.setBrush(QtGui.QColor(255, 80, 0, 255))
        for i in self.snakeArray:
            qp.drawRect(i[0], i[1], self.squareSize, self.squareSize)

    # game thread
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.direction(self.lastKeyPress)
            self.repaint()
        else:
            QtWidgets.QFrame.timerEvent(self, event)

    def getScoreType(self, number):
        if number == 1:
            if self.Food1Type == "Pomme":
                return 1
            if self.Food1Type == "Cerise":
                return 5
        if number == 2:
            if self.Food2Type == "Pomme":
                return 1
            if self.Food2Type == "Cerise":
                return 5

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Snake()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
