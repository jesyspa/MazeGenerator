from constants import WALL_SIZE

def draw_dot(turtle, colour):
    old_colour = turtle.pencolor()
    turtle.pencolor(colour)
    xcor = turtle.xcor()
    ycor = turtle.ycor()
    turtle.goto(xcor + WALL_SIZE/2, ycor + WALL_SIZE/2)
    turtle.dot(WALL_SIZE/3)
    turtle.goto(xcor, ycor)
    turtle.pencolor(old_colour)

class Exit:
    def draw(self, turtle):
        draw_dot(turtle, 'red')

class Entrance:
    def draw(self, turtle):
        draw_dot(turtle, 'green')

