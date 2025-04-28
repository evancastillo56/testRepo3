import random
import os
from math import comb
import pandas as pd

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
    size = 8

    # Check rows
    for i in range(size):
        numQueens = 0
        for j in range(size):
            pos = (size * i) + j
            if bVals[pos] == 'Q':
                numQueens += 1
        if numQueens > 1:
            attacks += comb(numQueens, 2)

    # Check columns
    for i in range(size):
        numQueens = 0
        for j in range(size):
            pos = (i + size * j)
            if bVals[pos] == 'Q':
                numQueens += 1
        if numQueens > 1:
            attacks += comb(numQueens, 2)

    # Check downward diagonals (top-left to bottom-right)
    for start in range(size):
        numQueens = 0
        x, y = 0, start
        while x < size and y < size:
            if bVals[x * size + y] == 'Q':
                numQueens += 1
            x += 1
            y += 1
        if numQueens > 1:
            attacks += comb(numQueens, 2)

    # From first column (excluding the first cell)
    for start in range(1, size):  
        numQueens = 0
        x, y = start, 0
        while x < size and y < size:
            if bVals[x * size + y] == 'Q':
                numQueens += 1
            x += 1
            y += 1
        if numQueens > 1:
            attacks += comb(numQueens, 2)

    # Check upward diagonals (bottom-left to top-right)
    for start in range(size):
        numQueens = 0
        x, y = size - 1, start
        while x >= 0 and y < size:
            if bVals[x * size + y] == 'Q':
                numQueens += 1
            x -= 1
            y += 1
        if numQueens > 1:
            attacks += comb(numQueens, 2)

    # From first column (excluding the last cell)
    for start in range(size - 2, -1, -1):  
        numQueens = 0
        x, y = start, 0
        while x >= 0 and y < size:
            if bVals[x * size + y] == 'Q':
                numQueens += 1
            x -= 1
            y += 1
        if numQueens > 1:
            attacks += comb(numQueens, 2)

    return attacks

#Make move based on first-choice hillclimbing
def makeMove(bVals,queenPos):
    betterMove = False
    size = 8
    h0 = hCost(bVals)
    h1 = 0

    tempQueen = queenPos.copy()

    while betterMove == False and len(tempQueen) > 0:
        tempBoard = bVals.copy()
        rand = random.randrange(0,len(tempQueen))
        #qStar is a randomly selected queen
        qStar = tempQueen[rand]
        col = qStar % 8

        #Generate legal moves for a qStar
        legalMoves = []
        for i in range(size):
            if(not(tempBoard[col+8*i] == 'Q')):
                legalMoves.append(col+8*i)
            else:
                pass

        #select a random move from available moves in a column
        while len(legalMoves) > 0:
            h1 = 0
            tempBoard = bVals.copy()
            rand2 = random.randrange(0,len(legalMoves))
            suggestMove = legalMoves[rand2]
            #Set previous queen spot to 0, and set new spot to Q
            tempBoard[qStar] = '0'
            tempBoard[suggestMove] = 'Q'
            h1 = hCost(tempBoard)
            if (h1 < h0):
                betterMove = True
                queenPos[queenPos.index(qStar)] = suggestMove
                break
            else:
                #remove move from available pool of moves for the column
                legalMoves.pop(rand2)
                h1 = 0
        #If no move in column improves hCost, then remove queen and try again
        h1 = 0
        tempQueen.pop(rand)
        #print("queenPos: ", queenPos)
    return queenPos

        


    

iterations = 1
trialArr = []      
while (iterations < 51):
    #Initialize our 8 Queens problem.
    board1 = ['0' for x in range(0,64)]
    # board2 = ['0' for x in range(0,64)]
    myQueens = generateRandomProblem()
    tempBoard = board1.copy()
    for y in myQueens:
        tempBoard[y] = 'Q'
    h = hCost(tempBoard)

    i = 0
    while (i < 200 and not(hCost == 0)):
        myQueens = makeMove(tempBoard,myQueens)
        tempBoard = board1.copy()
        for y in myQueens:
            tempBoard[y] = 'Q' 
        # initBoard(tempBoard)
        h = hCost(tempBoard)
        i += 1
    solution = (28-h, iterations)
    trialArr.append([solution[0], (solution[0]/28)])
    iterations += 1

problemsSolved = 0
for x in trialArr:
    if (x[0] == 28):
        problemsSolved += 1
    else:
        pass
percentSuccess = (problemsSolved/len(trialArr))*100

df = pd.DataFrame(trialArr, columns =['hCost:', 'solution/optimal'])
print("percent success: ", percentSuccess, "%")
print("problems Solved: ",problemsSolved)
print(df)