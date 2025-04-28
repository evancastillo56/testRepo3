import random
import os
from math import comb

#This function takes our position array and prints it to the console
def initBoard(bVals):
    for x in range(0,8):
        for y in range((8*x), (8*x+8)):
            print('|', bVals[y], end= "")
        print('|')
        for t in range(0,8):
            print('+--', end="")
        print('+')

#Generate an array where queens are randomly placed on a unique column
def generateRandomProblem():
    queens = [0,1,2,3,4,5,6,7]
    for i in range(0,8):
        rand = random.randrange(0,8)
        queens[i] += rand*8
    return queens

"""
This function calculates the heuristic cost associated with a given board
configuration. It begins by scanning each row, column, and diagonal
(we'll call them lines). If there is more than one queen present in
a given line, we take the total number of queens in that line, denoted n,
and calculate choose(n,2). This gives us the amount of pairwise attacks
in a line. Note that it is considered an attack even if there is an
intermediate piece between any two. To get the total heuristic cost, we simply
sum the number of pairwise attacks for all lines in the board.
"""
def hCost(bVals):
    attacks = 0
    #Check rows
    for i in range(0,8):
        numQueens = 0
        for j in range(0,8):
            pos = (8*i) + j
            if (bVals[pos] in {'Q'}):
                numQueens += 1
        if(numQueens > 1):
            attacks += comb(numQueens, 2)

    #Check columns
    for i in range(0,8):
        numQueens = 0
        for j in range(0,8):
            pos= (i+8*j)
            if (bVals[pos] in {'Q'}):
                numQueens += 1
        if(numQueens > 1):
            attacks += comb(numQueens, 2)
    
    


#Initialize our 8 Queens problem.
board = ['0' for x in range(0,64)]
myQueens = [0,8,16,24,25,41,49,57]
for y in myQueens:
    board[y] = 'Q'
initBoard(board)
h = hCost(board)
print(h)

    