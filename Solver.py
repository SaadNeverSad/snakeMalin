from Snake import Snake


class Solver:
    class SearchNode:
        def __init__(self, snake, priority):
            self.snake = snake
            self.priority = priority
            self.parent = None

        def compareTo(self, otherSearchNode):
            if self.priority < otherSearchNode.priority:
                return -1
            elif self.priority > otherSearchNode.priority:
                return 1
            else:
                return 0

    def __init__(self):
        self.initialSnake = Snake(-1, -1, -1, False)
        self.solution = None

    def AStar(self):
        print("Astar")
