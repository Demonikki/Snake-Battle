from __future__ import division
import sys, os, random, copy, time

## directions
RIGHT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (1, 0)
MOVES = [UP, RIGHT, DOWN, LEFT]
def oppDir(direction):
    if (direction == UP): return DOWN
    if (direction == DOWN): return UP
    if (direction == RIGHT): return LEFT
    if (direction == LEFT): return RIGHT

def processMove(moveDir, direction):
        if direction == UP:
            if moveDir == UP:
                return ''
            if moveDir == DOWN:
                return ''
            if moveDir == LEFT:
                return 'left'
            if moveDir == RIGHT:
                return 'right'
        if direction == DOWN:
            if moveDir == UP:
                return ''
            if moveDir == DOWN:
                return ''
            if moveDir == LEFT:
                return 'right'
            if moveDir == RIGHT:
                return 'left'
        if direction == LEFT:
            if moveDir == UP:
                return 'right'
            if moveDir == DOWN:
                return 'left'
            if moveDir == LEFT:
                return ''
            if moveDir == RIGHT:
                return ''
        if direction == RIGHT:
            if moveDir == UP:
                return 'left'
            if moveDir == DOWN:
                return 'right'
            if moveDir == LEFT:
                return ''
            if moveDir == RIGHT:
                return ''  


SIZE = 70

COLOR_P1 = (255, 30, 30) # player 1
COLOR_P2 = (30, 255, 30) # player 2

# Could probably benefit from inheritance but keeping it open to flexibility

''' Simple AI that only moves diagonally
'''
class Simple_ai:
    def __init__(self, direction, marked_tiles, currHead, oppHead):
        self.toggle = True
        self.direction = direction 
        self.marked = marked_tiles
        self.choice = UP
        self.head = currHead
        self.oppHead = oppHead
    
    def computeMove(self, marked_tiles, currHead, oppHead, direction, oppDirUnused):
        #Set fields
        self.marked = marked_tiles
        self.head = currHead
        self.oppHead = oppHead
        # print(self.toggle)
        self.toggle = not self.toggle
        if (self.toggle): return 'left'
        else: return 'right'


''' Purely Random Player
    Returns 'left' or 'right' decision randomly
'''
class Random_ai:
    def __init__(self, direction, marked_tiles, currHead, oppHead):
        self.direction = direction 
        self.marked = marked_tiles
        self.choice = UP
        self.head = currHead
        self.oppHead = oppHead
    
    def computeMove(self, marked_tiles, currHead, oppHead, direction, oppDirUnused):
        result = random.randint(0,2)
        if (result == 0): return 'left'
        else: return 'right'


''' Original AI from the Hackathon
    Simply looks 'n' steps forward and chooses the lowest cost path.
    Recalculates this path after every move.
    Does not account for movements of opponent. 
    Only accounts for current board state.
'''
class Original_ai:
    def __init__(self, direction, marked_tiles, currHead, oppHead):
        self.toggle = True
        self.direction = direction 
        self.marked = marked_tiles
        self.marked[currHead] = 1
        self.marked[oppHead] = 1
        self.choice = UP
        self.head = currHead
        self.oppHead = oppHead
        self.score = 0
        self.board =  [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        self.setBoundaries()

    #set the boundaries to be walls
    def setBoundaries(self):
        for i in range(SIZE):
            self.board[0][i] = 1
            self.board[i][0] = 1
            self.board[SIZE-1][i] = 1
            self.board[i][SIZE-1] = 1

    def updateBoard(self, head, move):
        board = copy.deepcopy(self.board)
        #general update
        for i in range (SIZE):
            for j in range (SIZE):
                if (i,j) in self.marked:
                    board[i][j] = 1
        #add heads
        board[head[0]][head[1]] = 1
        board[self.oppHead[0]][self.oppHead[1]] = 1

        nextMove = (head[0] + move[0], head[1]+move[1])
        if (nextMove[0] < 0 or nextMove[1] < 0 or nextMove[0] >= SIZE or nextMove[1] >= SIZE):
            return None
        board[nextMove[0]][nextMove[1]] = 1
        return board
    
    def getScore(self,board,head):
        exp = 2
        # Score = sum of distances to obstacles
        # Further away = higher score. Must be exponential to matter.
        dist_top    = head[1]            **exp  #distance FROM top
        dist_bot    = (SIZE - head[1])   **exp
        dist_left   = head[0]            **exp
        dist_right  = (SIZE - head[0])   **exp
        
        # if dist_top < 2: dist_top = -1000
        # if dist_bot < 2: dist_bot = -1000
        # if dist_left < 2: dist_left = -1000
        # if dist_right < 2: dist_right = -1000    
        # print ("Distance from top ", dist_top)
        # print ("Distance from bot ", dist_bot)
        # print ("Distance from left ", dist_left)
        # print ("Distance from right ", dist_right)

        total = dist_top+dist_bot+dist_left+dist_right
        return total

    def moveHead(self, head, move):
        if (not head): 
            return None
        newHead = (head[0]+move[0], head[1]+move[1])
        if (newHead[0] < 0 or newHead[1] < 0 or newHead[0] >= SIZE or newHead[1] >= SIZE):
            return None
        return newHead

    def computeMove(self, marked_tiles, currHead, oppHead, direction, oppDirUnused):
        #Set fields
        self.marked = marked_tiles
        self.head = currHead
        self.oppHead = oppHead

        board = [[]]
        head = self.head
        score = 0
        curr_score = self.getScore(board, head)
        max_score = curr_score #self.score
        max_score_dir = LEFT
        #Simulate 4 possible moves for current player
        for move in MOVES:
            head = self.head
            if(move != oppDir(direction)):
                #Update board with 1 square added
                head = self.moveHead(head, move)
                if (not head): continue
                #Compute score for this board
                score = self.getScore(board, head)
                # print (score, max_score)
                # print ("Score for moving ", move, " is ", score)
                if (score >= max_score):
                    max_score = score
                    max_score_dir = move
                    curr_score = score

        return processMove(max_score_dir, direction)

    



''' Runs Adverserial search to go down the path that gives maximum reward
    Look 3 steps ahead (depth 3) and computes total reward of each path possible
    Takes the path with highest reward - and RECALCULATES at every step to ensure
    that the best possible path is still being taken
'''
class Adverse_ai:
    def __init__(self, direction, marked_tiles, currHead, oppHead):
        self.toggle = True
        self.direction = direction 
        self.marked = marked_tiles
        self.marked[currHead] = 1
        self.marked[oppHead] = 1
        self.choice = UP
        self.head = currHead
        self.oppHead = oppHead
        self.score = 0
        self.board =  [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        self.setBoundaries()

    #set the boundaries to be walls
    def setBoundaries(self):
        for i in range(SIZE):
            self.board[0][i] = 1
            self.board[i][0] = 1
            self.board[SIZE-1][i] = 1
            self.board[i][SIZE-1] = 1

    def updateBoard(self, head, move):
        board = copy.deepcopy(self.board)
        #general update
        for i in range (SIZE):
            for j in range (SIZE):
                if (i,j) in self.marked:
                    board[i][j] = 1
        #add heads
        board[head[0]][head[1]] = 1
        board[self.oppHead[0]][self.oppHead[1]] = 1

        nextMove = (head[0] + move[0], head[1]+move[1])
        if (nextMove[0] < 0 or nextMove[1] < 0 or nextMove[0] >= SIZE or nextMove[1] >= SIZE):
            return None
        board[nextMove[0]][nextMove[1]] = 1
        return board
    
    def getScore(self,board,head):
        exp = 2
        # Score = sum of distances to obstacles
        # Further away = higher score. Must be exponential to matter.
        dist_top    = head[1]            **exp  #distance FROM top
        dist_bot    = (SIZE - head[1])   **exp
        dist_left   = head[0]            **exp
        dist_right  = (SIZE - head[0])   **exp
        
        total = dist_top+dist_bot+dist_left+dist_right
        return total

    def moveHead(self, head, move):
        if (not head): 
            return None
        newHead = (head[0]+move[0], head[1]+move[1])
        if (newHead[0] < 0 or newHead[1] < 0 or newHead[0] >= SIZE or newHead[1] >= SIZE):
            return None
        return newHead

    def computeMove(self, marked_tiles, currHead, oppHead, direction, oppDirection):
        #Set fields
        self.marked = marked_tiles
        self.head = currHead
        self.oppHead = oppHead

        playerScores = []
        oppScores = []
        board = [[]]
        head = self.head
        score = 0
        curr_score = self.getScore(board, head)
        max_score = curr_score #self.score
        max_score_dir = LEFT
        #Simulate 4 possible moves for current player
        for move in MOVES:
            head = self.head
            if(move != oppDir(direction)):
                #Update board with 1 square added
                head = self.moveHead(head, move)
                if (not head): continue
                #Compute score for this board
                score = self.getScore(board, head)
                #Check 4 possible moves of the opponent and get their 4 scores, and min of those
                oppScores = []
                for oppMove in MOVES:
                    if(oppMove != oppDir(oppDirection)):
                        #Update board with 1 move from Opponent's Head
                        oppHead = self.moveHead(oppHead, oppMove)
                        if (not oppHead): continue
                        oppScore = self.getScore(board, oppHead)/100
                        
                        #Check 4 possible moves of the player and get the max score
                        playerScores = []
                        for playerMove in MOVES:
                            head2 = head
                            if(playerMove != oppDir(move)):
                                head2 = self.moveHead(head2, playerMove)
                                if (not head2): continue
                                #Compute score for this board
                                playerScore = self.getScore(board, head2)/100
                                playerScores.append(playerScore)

                        oppScores.append(oppScore)
                # print (score)
                if (oppScores): score += min(oppScores)
                # print (score)
                if (playerScores) : score += max(playerScores)
                # print (score)
                if (score >= max_score):
                    max_score = score
                    max_score_dir = move
                    curr_score = score

        return processMove(max_score_dir, direction)

    















































# class Adverse_ai:
#     def __init__(self, direction, marked_tiles, currHead, oppHead):
#         self.toggle = True
#         self.direction = direction 
#         self.marked = marked_tiles
#         self.choice = UP
#         self.head = currHead
#         self.oppHead = oppHead
#         self.board =  [[0 for _ in range(SIZE)] for _ in range(SIZE)]
#         self.toggle = True
         
#     #set the boundaries to be walls
#     def setBoundaries(self):
#         for i in range(SIZE):
#             self.board[0][i] = 1
#             self.board[i][0] = 1
#             self.board[SIZE-1][i] = 1
#             self.board[i][SIZE-1] = 1


#     def updateBoard(self, move):
#         board = copy.deepcopy(self.board)
#         #general update
#         for i in range (SIZE):
#             for j in range (SIZE):
#                 if (i,j) in self.marked:
#                     board[i][j] = 1
#         #add heads
#         board[self.head[0]][self.head[1]] = 1
#         board[self.oppHead[0]][self.oppHead[1]] = 1
        
#         nextMove = self.head + move
#         if (nextMove[0] < 0 or nextMove[1] < 0):
#             return False
#         board[nextMove[0]][nextMove[1]] = 1
#         return board
    
#     def moveHead(self, head, move):
#         if (not head): 
#             return None
#         newHead = (head[0]+move[0], head[1]+move[1])
#         if (newHead[0] < 0 or newHead[1] < 0 or newHead[0] >= SIZE or newHead[1] >= SIZE):
#             return None
#         return newHead

#     def getScore(self,board,head):
#         exp = 2
#         # Score = sum of distances to obstacles
#         # Further away = higher score. Must be exponential to matter.
#         dist_top    = head[1]            **exp  #distance FROM top
#         dist_bot    = (SIZE - head[1])   **exp
#         dist_left   = head[0]            **exp
#         dist_right  = (SIZE - head[0])   **exp

#         total = dist_top+dist_bot+dist_left+dist_right
#         return total

#     def computeMove(self, marked_tiles, currHead, oppHead, direction, oppDirection):
#         #Set fields
#         self.marked = marked_tiles
#         self.head = currHead
#         self.oppHead = oppHead
#         board = [[]]
#         head = self.head
#         score = 0
#         curr_score = self.getScore(board, head)
#         max_score = curr_score #self.score
#         max_score_dir = LEFT
#         #Simulate 4 possible moves for current player
#         for move in MOVES:
#             head = self.head
#             if(move != oppDir(direction)):
#                 #Update board with 1 square added
#                 head = self.moveHead(head, move)
#                 if (not head): continue
#                 #Compute score for this board
#                 score = self.getScore(board, head)
#                 # print (score, max_score)
#                 # print ("Score for moving ", move, " is ", score)
#                 if (score >= max_score):
#                     max_score = score
#                     max_score_dir = move
#                     curr_score = score

        # board = [[]]
        # head = self.head
        # score = 0
        # curr_score = self.getScore(board, head)
        # max_score = curr_score #self.score
        # max_score_dir = LEFT
        # #Simulate 4 possible moves for current player
        # for move in MOVES:
        #     head = self.head
        #     oppHead = self.oppHead
        #     if(move != oppDir(direction)):
        #         #Update board with 1 square added
        #         head = self.moveHead(head, move)
        #         if (not head): continue
        #         #Compute score for this board
        #         score = self.getScore(board, head)

              
        #         if (score > max_score):
        #             max_score = score
        #             max_score_dir = move
        #             curr_score = score
                        



        # return processMove(max_score_dir, dir)
       

         #Check 4 possible moves of the opponent and get their 4 scores, and min of those
                # oppScores = []
                # for oppMove in MOVES:
                #     if(oppMove != oppDir(oppDirection)):
                #         #Update board with 1 move from Opponent's Head
                #         oppHead = self.moveHead(oppHead, oppMove)
                #         if (not oppHead): continue
                #         oppScores.append(self.getScore(board, oppHead))
                #     score += min(oppScores)