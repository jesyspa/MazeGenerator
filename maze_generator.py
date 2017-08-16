from enum import Enum
from random import randint, choice

from maze import Maze, Direction, Feature

class HomeDirection(Enum):
    UNKNOWN = 0
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4
    HERE = 5

    @classmethod
    def from_direction(cls, direction):
        return HomeDirection(direction.value+1)

    @property
    def is_direction(self):
        return 1 <= self.value and self.value < 5

    def to_direction(self):
        if not self.is_direction:
            raise Exception("{} is not a direction.".format(self))
        return Direction(self.value-1)


def create_maze(width, height, difficulty):
    class ScaffoldCell:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.explored = False
            self.home_direction = HomeDirection.UNKNOWN
            self.distance = 0
            self.is_exit = False

        @property
        def passages(self):
            if self.home_direction.is_direction:
                return [self.home_direction.to_direction()]
            return []

        @property
        def features(self):
            if self.home_direction == HomeDirection.HERE:
                return [Feature.ENTRANCE]
            if self.is_exit:
                return [Feature.EXIT]
            return []

    scaffold = Maze(ScaffoldCell, width, height)
    x_start = randint(0, width-1)
    y_start = randint(0, height-1)
    start = scaffold[x_start, y_start]

    start.explored = True
    start.home_direction = HomeDirection.HERE
    active_list = [start]
    max_distance = 0
    exit = start

    while active_list:
        if randint(0, 200) < difficulty:
            # easy case: latest node
            index = len(active_list)-1
        else:
            # hard case: random node
            index = randint(len(active_list)//2, len(active_list)-1)

        active = active_list[index]
        neighbours = scaffold.neighbours_of(active)

        unexplored = [ (d, n) for (d, n) in neighbours if not n.explored ]

        if not unexplored:
            active_list.pop(index)
            continue
        (direction, neighbour) = choice(unexplored)
        neighbour.explored = True
        neighbour.distance = active.distance+1
        if neighbour.distance > max_distance:
            max_distance = neighbour.distance
            exit = neighbour
        neighbour.home_direction = HomeDirection.from_direction(direction.opposite)

        active_list.append(neighbour)
        if active == start:
            active_list.pop(0)

    exit.is_exit = True

    scaffold.test_display()

if __name__ == '__main__':
    create_maze(12, 12, int(input("difficulty: ")))
    input()



