from Snake import Snake


class Solver:
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
            return self.snake.score == (self.snake.windowSize*self.snake.windowSize)

    def __init__(self, snake):
        self.initialSnake = snake
        self.solution = None
        self.AStar()

    def AStar(self):
        startSearchN = Solver.SearchNode(None, self.initialSnake, 0)
        nodeArray = []
        nodeArray.insert(startSearchN)
        current = nodeArray.pop()
        while not current.isGoal():
            self.addNext(nodeArray, current)
        if current.isGoal():
            self.solution = current

    def addNext(self, nodeArray, current):
        for next in current.snake.getNeighbors():
            if not next.equals(current.parent.Snake):
                nodeArray.insert(Solver.SearchNode(current, next, current.priority + 1))

    def solution(self):
        res = []
        current = self.solution
        while current is not None:
            res.append(current.Snake)
            current = current.parent
        return res
