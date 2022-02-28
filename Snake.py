from random import randrange


class Snake:
    def __init__(self, x, y, s, terrain, new):
        super(Snake, self).__init__()

        # Game parameters
        self.windowSize = 900  # size of the gui window, in pixel
        self.squareSize = 24  # size of one position, in pixel
        self.speed = 100  # length of the delay between each move in ms (lower --> faster)
        self.isOver = False  # set to True if the game is over
        self.highscore = 0
        self.safeZone = 15  # zone in which no rocks will be generated at spawn (number of positions)

        # Entities attributes
        self.Food1Placed, self.Food2Placed = False, False  # set to True when food has been placed
        self.Food1Type, self.Food2Type = "Pomme", "Pomme"  # the type of Food1 (either Pomme or Cerise)
        self.food1x, self.food1y, self.food2x, self.food2y = 0, 0, 0, 0  # the position of the food

        # Initialize the spawn point
        if x != -1 & y != -1:
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
            self.rocksGenerated = True

        # Initialize the snake array, which contains the positions occupied by the snake
        self.snakeArray = [[self.x, self.y], [self.x - self.squareSize, self.y], [self.x - self.squareSize * 2, self.y]]

        # Set the score
        if s != -1:
            self.score = s
        else:
            self.score = 0

        # Display the game
        if new:
            self.newGame()

    def newGame(self):
        self.y = self.squareSize * 4
        self.x = self.squareSize
        # Index: 0 = tête
        self.snakeArray = [[self.x, self.y], [self.x - self.squareSize, self.y], [self.x - self.squareSize * 2, self.y]]
        self.score = 0
        if not self.rocksGenerated:
            self.generateRocks(self.rockNumber)

    def checkStatus(self, x, y):
        for rock in self.rocks:
            if x == rock["x"] and y == rock["y"]:
                self.pause()
                self.isOver = True
                return False
        if y > self.windowSize - self.squareSize or x > self.windowSize - self.squareSize or x < 0 or y < self.squareSize:
            self.pause()
            self.isOver = True
            return False
        elif self.snakeArray[0] in self.snakeArray[1:len(self.snakeArray)]:
            self.pause()
            self.isOver = True
            return False
        elif self.y == self.food1y and self.x == self.food1x:
            self.Food1Placed = False
            self.score += self.getScoreType(1)

            # Make the snake grow
            for i in range(self.getScoreType(1)):
                self.snakeArray.insert(i, [self.x, self.y])
            self.snakeArray.pop()
            return True
        elif self.y == self.food2y and self.x == self.food2x:
            self.Food2Placed = False
            self.score += self.getScoreType(2)

            # Make the snake grow
            for i in range(self.getScoreType(2)):
                self.snakeArray.insert(i, [self.x, self.y])
            self.snakeArray.pop()
            return True

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

    # places the food when theres none on the board
    def placeFood(self):
        if not self.Food1Placed:
            self.food1x = randrange(1, int(self.windowSize / self.squareSize)) * self.squareSize
            self.food1y = randrange(1, int(self.windowSize / self.squareSize)) * self.squareSize

            # Make sure the food does not spawn on a rock
            for rock in self.rocks:
                if self.food1x == rock["x"] and self.food1y == rock["y"]:
                    self.placeFood()

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

            # Make sure the food does not spawn on a rock
            for rock in self.rocks:
                if self.food2x == rock["x"] and self.food2y == rock["y"]:
                    self.placeFood()

            rand = randrange(1, 3)
            if rand == 2:
                self.Food2Type = "Pomme"
            else:
                self.Food2Type = "Cerise"
            if not [self.food2x, self.food2y] in self.snakeArray:
                self.Food2Placed = True

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

    def getNearestFood(self):
        distFood1 = abs(self.food1x - self.x) + abs(self.food1y - self.y)
        distFood2 = abs(self.food2x - self.x) + abs(self.food2y - self.y)
        if distFood1 < distFood2:
            return [self.food1x, self.food1y, distFood1]
        else:
            return [self.food2x, self.food2y, distFood2]

    def getNeighbors(self):
        result = []

        if self.checkStatus(self.x + self.squareSize, self.y):
            result.append(Snake(self.x + self.squareSize, self.y, self.score, False, False))
        elif self.checkStatus(self.x - self.squareSize, self.y):
            result.append(Snake(self.x - self.squareSize, self.y, self.score, False, False))
        elif self.checkStatus(self.x, self.y + self.squareSize):
            result.append(Snake(self.x, self.y + self.squareSize, self.score, False, False))
        elif self.checkStatus(self.x, self.y - self.squareSize):
            result.append(Snake(self.x, self.y - self.squareSize, self.score, False, False))

        return result

    def getTerrain(self):
        return self.rocks
