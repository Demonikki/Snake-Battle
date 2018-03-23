import sys, os, random


## directions
UP = (0, -1)
RIGHT = (-1, 0)
DOWN = (0, 1)
LEFT = (1, 0)


class Simple_ai:
    def __init__(self, direction, marked_tiles):
        self.toggle = True
        self.direction = direction 
        self.marked = marked_tiles
        self.choice = UP
    
    def computeMove(self):
        # print(self.toggle)
        self.toggle = not self.toggle
        if (self.toggle): return 'left'
        else: return 'right'
