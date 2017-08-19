from enum import Enum
from constants import WALL_SIZE

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @property
    def opposite(self):
        return Direction(self.value ^ 2)

DIRECTIONS = {
    Direction.NORTH: (0, 1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, -1),
    Direction.WEST: (-1, 0)
}

class Maze:
    def __init__(self, make_cell, width, height):
        self.cells = [ make_cell(x, y) for y in range(height) for x in range(width) ]
        self.width = width
        self.height = height

    def convert(self, target_cell_type):
        make_cell = lambda x, y: target_cell_type(x, y, self[x, y])
        return Maze(make_cell, self.width, self.height)

    def __getitem__(self, key):
        x, y = key
        return self.cells[y * self.width + x]

    def neighbours_of(self, cell):
        options = [ (d, (cell.x + i, cell.y + j)) for (d, (i, j)) in DIRECTIONS.items() ]
        def satisfactory(x, y):
            return 0 <= x and x < self.width and 0 <= y and y < self.height
        return [ (d, self[k]) for (d, k) in options if satisfactory(*k) ]

    def offset(self, cell, offset):
        return self[cell.x + offset[0], cell.y + offset[1]]

    def display(self, turtle):
        pass

    def test_display(self):
        from turtle import Turtle
        t = Turtle()
        t.left(90)
        t.speed(0)
        for i in range(self.width):
            for j in range(self.height):
                t.forward(WALL_SIZE)
                t.right(90)
                t.forward(WALL_SIZE)
                t.backward(WALL_SIZE)
                t.left(90)
            t.backward(WALL_SIZE * self.height)
            t.right(90)
            t.forward(WALL_SIZE)
            t.left(90)
        t.forward(WALL_SIZE * self.height)

        t.penup()
        found_start = False
        found_end = False
        for x in range(self.width):
            for y in range(self.height):
                t.penup()
                t.setx(WALL_SIZE * x + 1)
                t.sety(WALL_SIZE * y + 1)
                t.color(self[x, y].background_colour)
                t.begin_fill()
                t.forward(WALL_SIZE-2)
                t.right(90)
                t.forward(WALL_SIZE-1)
                t.right(90)
                t.forward(WALL_SIZE-1)
                t.right(90)
                t.forward(WALL_SIZE-1)
                t.right(90)
                t.end_fill()
                t.end_fill()
                t.penup()
                t.setx(WALL_SIZE * x)
                t.sety(WALL_SIZE * y)
                for feature in self[x, y].features:
                    feature.draw(t)
                for direction in [Direction.WEST, Direction.NORTH, Direction.EAST, Direction.SOUTH]:
                    t.forward(1)
                    if direction in self[x, y].passages:
                        t.pendown()
                    t.forward(WALL_SIZE-2)
                    if direction in self[x, y].passages:
                        t.penup()
                    t.forward(1)
                    t.right(90)
        t.setx(0)
        t.sety(0)
        t.hideturtle()
        t.getscreen().exitonclick()

class FinishedCell:
    def __init__(self, x, y, other=None):
        self.x = x
        self.y = y
        if other:
            self.passages = other.passages
            self.features = other.features
            self.background_colour = other.background_colour
        else:
            self.passages = []
            self.features = []
            self.background_colour = 'white'


