import argparse, pygame, sys, os, random
from pygame.locals import *
from ai import *



#Run simulations
auto = True
draw = False



def_fps = 10000000

## start arguments
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-s', '--tilesize', dest='tilesize', metavar='PX', help='the size of a tile', type=int, default=12)
arg_parser.add_argument('-t', '--tiles', dest='tiles', nargs=2, metavar=('X', 'Y'), help='the number of tiles', type=int, default=[70, 70])
arg_parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='show debug information on the screen')
arg_parser.add_argument('-f', '--fps', dest='fps', nargs=1, metavar='TPS', help='framerate in ticks per second', type=int, default=def_fps)
arg_parser.add_argument('-b', '--delay', dest='delay', metavar='MS', help='button delay (raspi mode)', type=int, default=100)
args = arg_parser.parse_args()

## center window
os.environ['SDL_VIDEO_CENTERED'] = '1'

## window dimensions
TILE_SIZE = args.tilesize
TILES_X = args.tiles[0]
TILES_Y = args.tiles[1]

marked_tiles = {}

## colors
COLOR_BG = (30, 30, 30) # background
COLOR_FG = (255, 255, 255) # foreground
COLOR_P1 = (255, 30, 30) # player 1
COLOR_P2 = (30, 255, 30) # player 2
COLOR_FD = (255, 200, 30) # food
COLOR_DB = (50, 150, 250) # debug

## settings
TPS = args.fps # ticks lock
DEBUG = args.debug # debugging

## tiles to pixels
def get_dimension(x, y, width = 0, height = 0):
    return (x * TILE_SIZE, y * TILE_SIZE, width * TILE_SIZE, height * TILE_SIZE)
  
## init
pygame.init()
pygame.display.set_caption('Snake Battle AI' )
CLOCK = pygame.time.Clock()
DISPLAY_SURFACE = pygame.display.set_mode((TILE_SIZE * TILES_X, TILE_SIZE * TILES_Y))
DISPLAY_SURFACE.fill(COLOR_BG)

## fonts (change font files here)
FONT_DB = pygame.font.Font(None, 20) # debug font
FONT_SC = pygame.font.Font(None, TILE_SIZE * 5) # score

## directions
UP = (0, -1)
RIGHT = (-1, 0)
DOWN = (0, 1)
LEFT = (1, 0)

## game over
game_over = False
winners = []    #1 represents Player 1, 2 represents Player 2, 0 means draw

## print game over message
def game_over_msg(winner):
    winners.append(winner)
    with open("results.txt", "a") as myfile:
        myfile.write(str(winner))

## players
class Player:
    x = None
    y = None
    left = False
    right = False
    direction = None
    length = 2
    # tail = []

    def turn(self):
        if self.right:
            if self.direction == UP:
                self.direction = LEFT
            elif self.direction == RIGHT:
                self.direction = UP
            elif self.direction == DOWN:
                self.direction = RIGHT
            elif self.direction == LEFT:
                self.direction = DOWN
        elif self.left:
            if self.direction == UP:
                self.direction = RIGHT
            elif self.direction == RIGHT:
                self.direction = DOWN
            elif self.direction == DOWN:
                self.direction = LEFT
            elif self.direction == LEFT:
                self.direction = UP

game_over = False
p1 = Player()
p1.x = random.randint(1,69)
p1.y = random.randint(1,69)
p1.direction = UP

p2 = Player()
p2.x = random.randint(1,69)
p2.y = random.randint(1,69)
while (p2.x == p1.x and p2.y == p1.y):
    p2.x = random.randint(0,TILES_X)
    p2.y = random.randint(0,TILES_Y)
p2.direction = UP


## Define which AI for which player
# Create AI objects
player1_ai = Adverse_ai(UP, marked_tiles, (p1.x,p1.y), (p2.x,p2.y))
player2_ai = Original_ai(UP, marked_tiles, (p2.x,p2.y), (p1.x,p1.y))
#player2_ai = Adverse_ai(UP, marked_tiles, (p2.x,p2.y), (p1.x,p1.y))



## main loop
while not game_over:
    ## event queue
    for event in pygame.event.get():
        ## QUIT event
        if event.type == QUIT:
            print("## Quit ##")
            pygame.quit()
            sys.exit()

        ## keyboard mode
        elif event.type == KEYDOWN :
            if event.key == K_a:
                p1.left = True
                p1.right = False
                p1.turn()
            elif event.key == K_d:
                p1.right = True
                p1.left = False
                p1.turn()
            elif event.key == K_LEFT:
                p2.left = True
                p2.right = False
                p2.turn()
            elif event.key == K_RIGHT:
                p2.right = True
                p2.left = False
                p2.turn()
    ## run simulation
    if auto:
        move1 = player1_ai.computeMove(marked_tiles, (p1.x,p1.y), (p2.x,p2.y), p1.direction, p2.direction)
        if move1 == 'left': 
            p1.left = True
            p1.right = False
            p1.turn()
        elif move1 == 'right':
            p1.left = False
            p1.right = True
            p1.turn() 
        move2 = player2_ai.computeMove(marked_tiles, (p2.x,p1.y), (p1.x,p1.y), p2.direction, p1.direction)
        if move2 == 'left': 
            p2.left = True
            p2.right = False
            p2.turn()
        elif move2 == 'right':
            p2.left = False
            p2.right = True
            p2.turn()       


    #Reset turn values
    p1.left = False
    p1.right = False
    p2.left = False
    p2.right = False

    ## clear
    DISPLAY_SURFACE.fill(COLOR_BG)

    ## draw head
    pygame.draw.rect(DISPLAY_SURFACE, COLOR_P1, get_dimension(p1.x, p1.y, 1, 1))
    pygame.draw.rect(DISPLAY_SURFACE, COLOR_P2, get_dimension(p2.x, p2.y, 1, 1))

    ## move head
    p1.x += p1.direction[0]
    p1.y += p1.direction[1]
    p2.x += p2.direction[0]
    p2.y += p2.direction[1]
    
    ## draw trail
    for i, color in marked_tiles.items():
        pygame.draw.rect(DISPLAY_SURFACE, color, get_dimension(i[0], i[1], 1, 1))

    #Increment length every loop
    p1.length += 1
    p2.length += 1

    ## check game over (edges)
    if (p1.x >= TILES_X or p1.y >= TILES_Y or p1.x < 0 or p1.y < 0) and (p2.x >= TILES_X or p2.y >= TILES_Y or p2.x < 0 or p2.y < 0):
        game_over_msg(0)
        game_over = True
    else:
        if p1.x >= TILES_X or p1.y >= TILES_Y or p1.x < 0 or p1.y < 0:
            game_over_msg(2)
            game_over = True
        elif p2.x >= TILES_X or p2.y >= TILES_Y or p2.x < 0 or p2.y < 0:
            game_over_msg(1)
            game_over = True

    ## check game over (touch)
    if p1.x == p2.x and p1.y == p2.y:
        game_over_msg(0)
        game_over = True
    else:
        for (i,c) in marked_tiles.items():
            if i[0] == p1.x and i[1] == p1.y:
                game_over_msg(2)
                game_over = True
            if i[0] == p2.x and i[1] == p2.y:
                game_over_msg(1)
                game_over = True

    #add head to marked tiles
    marked_tiles[(p1.x, p1.y)] =  COLOR_P1
    marked_tiles[(p2.x, p2.y)] =  COLOR_P2

    ## update
    CLOCK.tick(TPS)
    pygame.display.update()


pygame.time.wait(0)
