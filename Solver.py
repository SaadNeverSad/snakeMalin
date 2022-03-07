from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt


class SearchNode:
    def __init__(self, parent, snake, priority):
        self.snake = snake
        self.priority = priority
        self.parent = parent

    def compareTo(self, otherSearchNode):
        if self.priority < otherSearchNode.priority:
            return -1
        elif self.priority > otherSearchNode.priority:
            return 1
        else:
            return 0

    def isGoal(self):
        return self.snake.score == 1


class Solver(QtWidgets.QWidget):

    def __init__(self, snake):
        super().__init__()
        self.initialSnake = snake
        self.solution = None
        self.AStar()
        self.qp = QtGui.QPainter()

    def AStar(self):
        startSearchN = SearchNode(None, self.initialSnake, 0)
        nodeArray = [startSearchN]
        current = nodeArray.pop()
        i = 0
        while not current.isGoal():
            self.addNext(nodeArray, current)
            min = 99999
            for node in nodeArray:
                if node.priority < min:
                    min = node.priority
            for node in nodeArray:
                if node.priority is min:
                    current = nodeArray.pop()
                    break
            if i == 10:
                self.solution = current
                break
            i += 1
        if current.isGoal():
            self.solution = current

    def addNext(self, nodeArray, current):
        for next in current.snake.getNeighbors():
            if (current.parent is None) or (not next.equals(current.parent.snake)):
                nearestFood = current.snake.getNearestFood()
                print("Nearest food selected: " + str(nearestFood[2]))
                nodeArray.append(SearchNode(current, next, current.priority + 1/nearestFood[2]))

    def getSolution(self):
        res = []
        current = self.solution
        while current is not None:
            res.append(current.snake)
            current = current.parent
        print("senior")
        print(res)
        return res

    def initUI(self):
        self.setStyleSheet("QWidget { background: #A9F5D0 }")
        self.setFixedSize(self.initialSnake.windowSize, self.initialSnake.windowSize)
        self.setWindowTitle('Snake')
        self.show()

    def paintEvent(self, event):
        self.qp.begin(self)
        self.scoreBoard()
        self.drawRocks()
        self.drawFood()
        self.drawSnake()
        self.scoreText()
        if self.initialSnake.isOver:
            self.gameOver()
        self.qp.end()

    def direction(self, dir):
        if dir == "DOWN" and self.snake.checkStatus(self.snake.x, self.snake.y + self.snake.squareSize):
            self.snake.y += self.snake.squareSize
            self.repaint()
            self.snake.snakeArray.insert(0, [self.snake.x, self.snake.y])
        elif dir == "UP" and self.snake.checkStatus(self.snake.x, self.snake.y - self.snake.squareSize):
            self.snake.y -= self.snake.squareSize
            self.repaint()
            self.snake.snakeArray.insert(0, [self.snake.x, self.snake.y])
        elif dir == "RIGHT" and self.snake.checkStatus(self.snake.x + self.snake.squareSize, self.snake.y):
            self.snake.x += self.snake.squareSize
            self.repaint()
            self.snake.snakeArray.insert(0, [self.snake.x, self.snake.y])
        elif dir == "LEFT" and self.snake.checkStatus(self.snake.x - self.snake.squareSize, self.snake.y):
            self.snake.x -= self.snake.squareSize
            self.repaint()
            self.snake.snakeArray.insert(0, [self.snake.x, self.snake.y])

    def scoreBoard(self):
        self.qp.setPen(Qt.NoPen)
        self.qp.setBrush(QtGui.QColor(25, 80, 0, 160))
        self.qp.drawRect(0, 0, self.snake.windowSize, self.snake.squareSize)

    def scoreText(self):
        self.qp.setPen(QtGui.QColor(255, 255, 255))
        self.qp.setFont(QtGui.QFont('Arial', 10))
        self.qp.drawText(8, 17, "SCORE: " + str(self.snake.score))
        self.qp.drawText(195, 17, "HIGHSCORE: " + str(self.snake.highscore))

    def gameOver(self):
        self.highscore = max(self.snake.highscore, self.snake.score)

    def drawRocks(self):
        self.qp.setBrush(QtGui.QColor(45, 45, 45, 255))
        # Draw rocks on the map
        for rock in self.snake.rocks:
            self.qp.drawRect(rock["x"], rock["y"], self.snake.squareSize, self.snake.squareSize)

    def drawFood(self):
        if self.snake.fruits["food1_type"] == "Pomme":
            self.qp.setBrush(QtGui.QColor(80, 180, 0, 160))
        else:
            self.qp.setBrush(QtGui.QColor(255, 0, 0, 160))
        self.qp.drawRect(self.snake.fruits["food1_x"], self.snake.fruits["food1_y"], self.snake.squareSize,
                         self.snake.squareSize)

        if self.snake.fruits["food2_type"] == "Pomme":
            self.qp.setBrush(QtGui.QColor(80, 180, 0, 160))
        else:
            self.qp.setBrush(QtGui.QColor(255, 0, 0, 160))
        self.qp.drawRect(self.snake.fruits["food2_x"], self.snake.fruits["food2_y"], self.snake.squareSize,
                         self.snake.squareSize)

    # draws each component of the snake
    def drawSnake(self):
        self.qp.setPen(Qt.NoPen)
        self.qp.setBrush(QtGui.QColor(255, 80, 0, 255))
        for i in self.snake.snakeArray:
            self.qp.drawRect(i[0], i[1], self.snake.squareSize, self.snake.squareSize)
