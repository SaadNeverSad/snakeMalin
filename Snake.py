from random import randrange

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt


class Snake(QtWidgets.QWidget):
    def __init__(self, x, y, array, s, terrain, fruits, new, paint):
        super(Snake, self).__init__()

        # Game parameters
        self.windowSize = 900  # size of the gui window, in pixel
        self.squareSize = 24  # size of one position, in pixel
        self.speed = 100  # length of the delay between each move in ms (lower --> faster)
        self.isPaused = False  # set to True if the game is paused
        self.isOver = False  # set to True if the game is over
        self.timer = QtCore.QBasicTimer()  # used to track the time
        self.highscore = 0
        self.lastKeyPress = 'RIGHT'  # initial direction taken by the snake
        self.safeZone = 15  # zone in which no rocks will be generated at spawn (number of positions)
        self.fruits = {}

        # Entities attributes

        # Initialize the fruits' positions
        if fruits == -1:
            self.fruits["food1_placed"], self.fruits["food2_placed"] = False, False  # set to True when food has been placed
            self.fruits["food1_type"], self.fruits["food2_type"] = "Pomme", "Pomme"  # the type of Food1 (either Pomme or Cerise)
            self.fruits["food1_x"], self.fruits["food1_y"], self.fruits["food2_x"], self.fruits["food2_y"] = 0, 0, 0, 0  # the position of the food

        else:
            self.fruits = fruits

        # Initialize the spawn point
        if x == -1 and y == -1:
            self.y = self.squareSize * 4
            self.x = self.squareSize
        else:
            self.x = x
            self.y = y

        # Initialize terrain
        if terrain == -1:
            self.rocks = []  # array containing every rock (obstacle) on the terrain
            self.rockNumber = 50  # number of rocks to be generated
            self.rocksGenerated = False  # set to True when rocks have been generated
        else:
            self.rocks = terrain
            self.rockNumber = 50  # number of rocks to be generated
            self.rocksGenerated = True

        # Initialize the snake array, which contains the positions occupied by the snake
        if array == -1:
            self.snakeArray = [[self.x, self.y], [self.x - self.squareSize, self.y], [self.x - self.squareSize * 2, self.y]]
        else:
            self.snakeArray = array

        # Set the score
        if s != -1:
            self.score = s
        else:
            self.score = 0

        # Display the game
        if new:
            self.newGame()
        if paint:
            self.qp = QtGui.QPainter()
            self.initUI()

    def initUI(self):
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

        # Modifie la derniere touche directionelles selectionné, en interdisant de selectionné la touche inverse de la derniere selectionné
        # ou applique une des trois fonctions pause (touche P), newGame (touche Space) ou  close (touche Escape)

    def keyPressEvent(self, e):
        if not self.isPaused:
            # print "inflection point: ", self.x, " ", self.y

            # Fleche Haut
            if e.key() == Qt.Key_Up and self.lastKeyPress != 'UP' and self.lastKeyPress != 'DOWN':
                self.direction("UP")
                self.lastKeyPress = 'UP'

            # Fleche Bas
            elif e.key() == Qt.Key_Down and self.lastKeyPress != 'DOWN' and self.lastKeyPress != 'UP':
                self.direction("DOWN")
                self.lastKeyPress = 'DOWN'

            #Fleche Gauche
            elif e.key() == Qt.Key_Left and self.lastKeyPress != 'LEFT' and self.lastKeyPress != 'RIGHT':
                self.direction("LEFT")
                self.lastKeyPress = 'LEFT'

            #Fleche Droite
            elif e.key() == Qt.Key_Right and self.lastKeyPress != 'RIGHT' and self.lastKeyPress != 'LEFT':
                self.direction("RIGHT")
                self.lastKeyPress = 'RIGHT'
            elif e.key() == Qt.Key_P:
                self.pause()
        #Pause with P
        elif e.key() == Qt.Key_P:
            self.start()
        #Restart a new game with Space
        elif e.key() == Qt.Key_Space:
            self.newGame()
        #Close game with Escape
        elif e.key() == Qt.Key_Escape:
            self.close()

    #Create a new game
    def newGame(self):
        self.y = self.squareSize * 4
        self.x = self.squareSize
        # Index: 0 = tête
        self.snakeArray = [[self.x, self.y], [self.x - self.squareSize, self.y], [self.x - self.squareSize * 2, self.y]]
        self.lastKeyPress = 'RIGHT'
        self.score = 0
        #Place the rocks
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

    #Modifie la direction dans laquelle notre serpent va en fonction de notre derniere touche directionelle selectionné
    #Et redessine notre serpent sur la grille
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

    #Affiche le scoreboard
    def scoreBoard(self):
        self.qp.setPen(Qt.NoPen)
        self.qp.setBrush(QtGui.QColor(25, 80, 0, 160))
        self.qp.drawRect(0, 0, self.windowSize, self.squareSize)

    #Affiche le score
    def scoreText(self, event):
        self.qp.setPen(QtGui.QColor(255, 255, 255))
        self.qp.setFont(QtGui.QFont('Arial', 10))
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
        elif self.y == self.fruits["food1_y"] and self.x == self.fruits["food1_x"]:
            self.fruits["food1_placed"] = False
            self.score += self.getScoreType(1)

            # Make the snake grow
            for i in range(self.getScoreType(1)):
                self.snakeArray.insert(i, [self.x, self.y])
            self.snakeArray.pop()
            return True
        elif self.y == self.fruits["food2_y"] and self.x == self.fruits["food2_x"]:
            self.fruits["food2_placed"] = False
            self.score += self.getScoreType(2)

            # Make the snake grow
            for i in range(self.getScoreType(2)):
                self.snakeArray.insert(i, [self.x, self.y])
            self.snakeArray.pop()
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

            # Make a safe zone with no rocks in the spawn
            while rock["x"] < self.squareSize * self.safeZone and rock["y"] < self.squareSize * self.safeZone:
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
        if not self.fruits["food1_placed"]:

            #Place the food number 1
            self.fruits["food1_x"] = randrange(1, int(self.windowSize / self.squareSize)) * self.squareSize
            #Place the food number 2           
            self.fruits["food1_y"] = randrange(1, int(self.windowSize / self.squareSize)) * self.squareSize

            # Make sure the food does not spawn on a rock
            for rock in self.rocks:
                if self.fruits["food1_x"] == rock["x"] and self.fruits["food1_y"] == rock["y"]:
                    self.placeFood()

            #Selectionne le type de nourriture de Food1, la pomme a 1/3 d'apparaitre, la Cerise 2/3
            rand = randrange(1, 3)
            if rand == 2:
                self.fruits["food1_type"] = "Pomme"
            else:
                self.fruits["food1_type"] = "Cerise"
            if not [self.fruits["food1_x"], self.fruits["food1_y"]] in self.snakeArray:
                self.fruits["food1_placed"] = True
        if not self.fruits["food2_placed"]:
            self.fruits["food2_x"] = randrange(1, int(self.windowSize / self.squareSize)) * self.squareSize
            self.fruits["food2_y"] = randrange(1, int(self.windowSize / self.squareSize)) * self.squareSize

            # Make sure the food does not spawn on a rock
            for rock in self.rocks:
                if self.fruits["food2_x"] == rock["x"] and self.fruits["food2_y"] == rock["y"]:
                    self.placeFood()
            #Selectionne le type de nourriture de Food2, la pomme a 1/3 d'apparaitre, la Cerise 2/3
            rand = randrange(1, 3)
            if rand == 2:
                self.fruits["food2_type"] = "Pomme"
            else:
                self.fruits["food2_type"] = "Cerise"
            if not [self.fruits["food2_x"], self.fruits["food2_y"]] in self.snakeArray:
                self.fruits["food2_placed"] = True

        if self.fruits["food1_type"] == "Pomme":
            self.qp.setBrush(QtGui.QColor(80, 180, 0, 160)) #Selectionne un carré vert pour la pomme
        else:
            self.qp.setBrush(QtGui.QColor(255, 0, 0, 160)) #Selectionne un carré rouge pour la cerise
        self.qp.drawRect(self.fruits["food1_x"], self.fruits["food1_y"], self.squareSize, self.squareSize)

        if self.fruits["food2_type"] == "Pomme":
            self.qp.setBrush(QtGui.QColor(80, 180, 0, 160)) #Selectionne un carré vert pour la pomme
        else:
            self.qp.setBrush(QtGui.QColor(255, 0, 0, 160)) #Selectionne un carré rouge pour la cerise
        self.qp.drawRect(self.fruits["food2_x"], self.fruits["food2_y"], self.squareSize, self.squareSize)

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

    #Recupere le score associé a chacun des deux fruits
    def getScoreType(self, number):
        if number == 1:
            if self.fruits["food1_type"] == "Pomme":
                return 1
            if self.fruits["food1_type"] == "Cerise":
                return 5
        if number == 2:
            if self.fruits["food2_type"] == "Pomme":
                return 1
            if self.fruits["food2_type"] == "Cerise":
                return 5

    #Renvoie la position de la nourriture la plus proche ainsi que la distance a laquelle la tete de notre serpent est de cette nourriture
    def getNearestFood(self):
        distFood1 = abs(self.fruits["food1_x"] - self.x) + abs(self.fruits["food1_y"] - self.y)
        distFood2 = abs(self.fruits["food2_x"] - self.x) + abs(self.fruits["food2_y"] - self.y)
        if distFood1 < distFood2:
            print([self.fruits["food1_x"], self.fruits["food1_y"], distFood1])
            return [self.fruits["food1_x"], self.fruits["food1_y"], distFood1]
        else:
            return [self.fruits["food2_x"], self.fruits["food2_y"], distFood2]

    def getNeighbors(self):
        result = []
        new_array = self.snakeArray

        if self.checkStatus(self.x + self.squareSize, self.y):
            new_array.insert(0, [self.x + self.squareSize, self.y])
            result.append(Snake(self.x + self.squareSize, self.y, new_array, self.score, self.rocks, self.fruits, False, False))
        if self.checkStatus(self.x - self.squareSize, self.y):
            new_array.insert(0, [self.x - self.squareSize, self.y])
            result.append(Snake(self.x - self.squareSize, self.y, new_array, self.score, self.rocks, self.fruits, False, False))
        if self.checkStatus(self.x, self.y + self.squareSize):
            new_array.insert(0, [self.x, self.y + self.squareSize])
            result.append(Snake(self.x, self.y + self.squareSize, new_array, self.score, self.rocks, self.fruits, False, False))
        if self.checkStatus(self.x, self.y - self.squareSize):
            new_array.insert(0, [self.x, self.y - self.squareSize])
            result.append(Snake(self.x, self.y - self.squareSize, new_array, self.score, self.rocks, self.fruits, False, False))

        return result

    def get_terrain(self):
        return self.rocks

    def get_array(self):
        return self.snakeArray

    def get_fruits(self):
        return self.fruits

    def equals(self, snake):
        return self.fruits == snake.fruits and self.x == snake.x and self.y == snake.y and self.rocks == snake.rocks and self.snakeArray == snake.snakeArray and self.score == snake.score
