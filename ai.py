import sys, os, random


## directions
UP = (0, -1)
RIGHT = (-1, 0)
DOWN = (0, 1)
LEFT = (1, 0)

# Could probably benefit from inheritance but keeping it open to flexibility

class Simple_ai:
    def __init__(self, direction, marked_tiles, currHead, oppHead):
        self.toggle = True
        self.direction = direction 
        self.marked = marked_tiles
        self.choice = UP
        self.head = currHead
        self.oppHead = oppHead
    
    def computeMove(self):
        # print(self.toggle)
        self.toggle = not self.toggle
        if (self.toggle): return 'left'
        else: return 'right'

''' Runs Adverserial search to go down the path that gives maximum reward
    Look 3 steps ahead (depth 3) and computes total cost of each path possible
    Takes the path with least cost - and RECALCULATES at every step to ensure
    that the best possible path is still being taken
'''

class Adverse_ai:
    def __init__(self, direction, marked_tiles, currHead, oppHead):
        self.toggle = True
        self.direction = direction 
        self.marked = marked_tiles
        self.choice = UP
        self.head = currHead
        self.oppHead = oppHead
    
    def computeMove(self):
        decision = ''

       