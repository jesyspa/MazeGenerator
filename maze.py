from enum import Enum

WALL_SIZE = 20

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

def draw_dot(turtle, colour):
    old_colour = turtle.pencolor()
    turtle.pencolor(colour)
    xcor = turtle.xcor()
    ycor = turtle.ycor()
    turtle.goto(xcor + WALL_SIZE/2, ycor + WALL_SIZE/2)
    turtle.dot(WALL_SIZE/3)
    turtle.goto(xcor, ycor)
    turtle.pencolor(old_colour)

class Feature(Enum):
    ENTRANCE = 0
    EXIT = 1


    def draw(self, turtle):
        colour = {
                Feature.ENTRANCE: 'green',
                Feature.EXIT: 'red'
        }[self]
        draw_dot(turtle, colour)

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

        t.pencolor('white')
        t.penup()
        found_start = False
        found_end = False
        for x in range(self.width):
            for y in range(self.height):
                t.setx(WALL_SIZE * x)
                t.sety(WALL_SIZE * y)
                for feature in Feature:
                    if feature in self[x, y].features:
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
