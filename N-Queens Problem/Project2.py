# ITCS 6150
# Noah Foster
# Project 2

import random
# helper function makes a 2d array size nxn filled with zeroes
def makeArray(n):
    array = []
    for i in range(0,n):
        inner = []
        for j in range(0, n):
            inner.append(0)
        array.append(inner)
    return array
# helper function generates n tuples (i,j) representing queens at position row i, column j with one in each row
def makeQueens(n):
    queens = []
    for i in range(0,n):
        queen = (i, random.randint(0,n-1))
        queens.append(queen)  
    return queens
# helper function to find queens attacking each square and populate array accordingly.
def populateAttacking(array, queens):
    for each in queens:
        (i,j)=each
        incrementRow(array, i)
        incrementColumn(array, j)
        incrementDiags(array, i, j)
        array[i][j]=array[i][j]-2 # decrement for repeated counts on the space we are sitting on.
# helper for populateAttacking to increment for attacks on same row
def incrementRow(array, i):
    j=0
    while j<len(array[i]):
        array[i][j]=array[i][j]+1
        j=j+1
# helper for populateAttacking to increment for attacks on same column
def incrementColumn(array, j):
    i=0
    while i<len(array):
        array[i][j]=array[i][j]+1
        i=i+1
# helper for populateAttacking to increment for attacks on the diagonal
def incrementDiags(array, qi, qj):
    i=0
    j=0
    while i<len(array):
        j=0
        while j<len(array[i]):
            if ((i+j == qi+qj) or (i-j==qi-qj)):
                array[i][j]=array[i][j]+1
            j=j+1
        i=i+1
# helper for determining if a square is attacked by a queen 
# (helpful because if it is, we want to consider that square to have a lower value when considering to move the queen there)
def isAttacking(queen,i,j):
    (qi,qj)=queen
    if (qi==i or qj==j or qi+qj==i+j or qi-qj==i-j):
        return 1
    else:
        return 0
        

# helper to show board of queens
def showQueens(n, queens):
    #n = len(queens)
    array = []
    for i in range(0,n):
        inner = []
        for j in range(0, n):
            inner.append(0)
        array.append(inner)
    for each in queens:
        (i,j) = each
        array[i][j] = 'Q'
    printArray(array)
        
    

# Helper Function to Print 2D Arrays.
def printArray(array):
    for row in array:
        string = ""
        for each in row:
            string = string + str(each) + " "
        print(string)
        
# Helper to Print Path of Queens
def printPath(n, path):
    for each in path[:-1]:
        showQueens(n, each)
        print(" \/")
    showQueens(n,path[len(path)-1])
        

# helper to find the best move for a given queen and array and array of queens
def bestMove(array,qi,qj,queens):
    besti=None
    bestj=None
    bestH=len(array)**2 # impossibly large so the first better value is always chosen
    qH = array[qi][qj]-1
    i=0
    while i<len(array):
        j=0
        while j<len(array[i]):
            h = array[i][j]
            if(isAttacking((qi,qj),i,j)): # lower h value because we don't want to consider attacks by the queen we are moving.
                h=h-1
            
            isOccupied=False
            for each in queens:
                (oi,oj)=each
                if (i==oi and j==oj):
                    isOccupied=True
            if(isOccupied): # we don't consider the square any queen is on as a possible move
                pass
            else: 
                if(h>=qH): # the current position of the queen is better
                    pass
                else:
                    if (h<bestH): # if, after all that, the h is less than the best h, we replace the best values
                        bestH=h
                        besti=i
                        bestj=j
            j=j+1
        i=i+1
    return(bestH,besti,bestj)

# helper to find sidewaysMoves
def sidewaysFinder(array,qi,qj,queens):
    qH = array[qi][qj]-1
    sideways=[]
    i=0
    for i in range(0,len(queens)):
        (testi,testj)=queens[i]
        if (testi==qi and testj==qj):
            q=i
    i=0
    while i<len(array):
        j=0
        while j<len(array[i]):
            h = array[i][j]
            if(isAttacking((qi,qj),i,j)): # lower h value because we don't want to consider attacks by the queen we are moving.
                h=h-1
            
            isOccupied=False
            for each in queens:
                (oi,oj)=each
                if (i==oi and j==oj):
                    isOccupied=True
            if(isOccupied): # we don't consider the square any queen is on as a possible move
                pass
            else: 
                if(h==qH): # sideways move found
                    sideways.append((q,i,j))
            j=j+1
        i=i+1
    return sideways

import heapq
# hill climb search
def hillClimbSearch(n, queens=None):
    steps=0
    if queens == None:
        queens = makeQueens(n)
    path=[queens.copy()] # variable to store path that we take to answer.
    while (True):
        array = makeArray(n) 
        populateAttacking(array, queens) # populating the array with heuristic values
        priorityQueens = []
        heapq.heapify(priorityQueens) # array to store indexes of queens as sorted list by which one is worst
        q=0
        while(q<len(queens)): # sort queens by how many queens are attacking them
            (qi,qj)=queens[q]
            qH = array[qi][qj]-1
            heapq.heappush(priorityQueens, (qH*-1,q)) # heaps sort from smallest to largest and we want largest to smallest, so multiply by -1
            q=q+1
        (worstH,worst)=priorityQueens[0]
        if(worstH==0): # the worst queen is 0, we solved it
            return (queens, steps, path)
        qi=None
        qj=None
        qH=None
        (bestH,besti,bestj)=(None,None,None)
        while(len(priorityQueens)>0 and besti==None): # we want to check all the queens, stopping when we have an answer
            (qHNeg,q)=heapq.heappop(priorityQueens)
            qH=qHNeg*-1 # reverse the negativeness that we applied earlier
            (qi,qj)=queens[q] # position of the queen we are checking
            (bestH,besti,bestj)=bestMove(array,qi,qj,queens)
        if (besti==None): # the algorithm failed.
            return (None, steps, path)
        queens[q]=(besti,bestj)
        path.append(queens.copy()) # appending step to queens array
        steps=steps+1
            
# hill climb search but it supports sideways moves up to a certain count in a row.
def hillClimbSearchSideways(n, maxSidewaysMoves, queens=None):
    steps=0
    if queens==None:
        queens = makeQueens(n)
    path=[queens.copy()] # variable to store path that we take to answer.
    visited={str(queens):True} # store initial state of queens in a dictionary that will also store visited states
    sidewaysMovesCount=0
    while (True):
        goodMoveMade=False
        array = makeArray(n) 
        populateAttacking(array, queens) # populating the array with heuristic values
        priorityQueens = []
        heapq.heapify(priorityQueens) # array to store indexes of queens as sorted list by which one is worst
        q=0
        while(q<len(queens)): # sort queens by how many queens are attacking them
            (qi,qj)=queens[q]
            qH = array[qi][qj]-1
            heapq.heappush(priorityQueens, (qH*-1,q)) # heaps sort from smallest to largest and we want largest to smallest, so multiply by -1
            q=q+1
        (worstH,worst)=priorityQueens[0]
        priorityQueensSideways=priorityQueens.copy()
        if(worstH==0): # the worst queen is 0, we solved it
            return (queens, steps, path)
        qi=None
        qj=None
        qH=None
        (bestH,besti,bestj)=(None,None,None)
        while(len(priorityQueens)>0 and besti==None): # we want to check all the queens, stopping when we have an answer
            (qHNeg,q)=heapq.heappop(priorityQueens)
            qH=qHNeg*-1 # reverse the negativeness that we applied earlier
            (qi,qj)=queens[q] # position of the queen we are checking
            (bestH,besti,bestj)=bestMove(array,qi,qj,queens)
        if (besti!=None): # a best move was found, proceed.
            queens[q]=(besti,bestj)
            goodMoveMade=True
            sidewaysMovesCount=0
            path.append(queens.copy()) # appending good step to queens array
            steps=steps+1
        if (goodMoveMade==False):
            # by virtue of getting here, we have reached the sideways moves.
            if(sidewaysMovesCount<maxSidewaysMoves):
                qi=None
                qj=None
                qH=None
                (besti,bestj)=(None,None)
                sidewaysMoves=[]
                while(len(priorityQueensSideways)>0): # we want to check all the queens, stopping when we have an answer
                    (qHNeg,q)=heapq.heappop(priorityQueensSideways)
                    qH=qHNeg*-1 # reverse the negativeness that we applied earlier
                    (qi,qj)=queens[q] # position of the queen we are checking
                    sidewaysMoves=sidewaysMoves+sidewaysFinder(array,qi,qj,queens)
                i=0
                while(i<len(sidewaysMoves)): # testing if a potential sideways move is in the visited dictionary
                    (qtest,testi,testj)=sidewaysMoves[i]
                    testqueens=queens.copy()
                    testqueens[qtest]=(testi,testj)
                    if str(testqueens) in visited:
                        sidewaysMoves.pop(i)
                    else:
                        i=i+1
                    
                if (len(sidewaysMoves)>0):
                    (q,besti,bestj)=sidewaysMoves[random.randint(0,len(sidewaysMoves)-1)]
                    
                
            if (sidewaysMovesCount>=maxSidewaysMoves): # too many sideways moves
                return (None, steps, path)
            if (len(sidewaysMoves)==0): # no sideways moves found, somehow
                return (None, steps, path)
            queens[q]=(besti,bestj)
            sidewaysMovesCount=sidewaysMovesCount+1
            path.append(queens.copy()) # appending sideways step to path array
            steps=steps+1
        visited[str(queens)]=True # store state of queens after move


# User Interactable Portion of Program, Finds all the things we need for the report.
print("N-Queens Problem Solver (Using Hill Climb Search)")
n = int(input("Please Input value of n (number of queens and size of board): "))
sideways = int(input("Input how many consecutive sideways moves we should tolerate (100 is suggested for n=8): "))
iterations = 1000
print("Collecting Data on "+str(iterations)+" iterations...")
regFails=0
regSuccesses=0
regFailsSteps=0
regSuccessesSteps=0
for i in range(0, iterations):
    (queens,steps,path)=hillClimbSearch(n)
    if (queens==None):
        regFails=regFails+1
        regFailsSteps=regFailsSteps+steps
    else:
        regSuccesses=regSuccesses+1
        regSuccessesSteps=regSuccessesSteps+steps
print("Regular Hill Climb Search Results:")
successRate=(regSuccesses/(regSuccesses+regFails))*100
print("Success Rate: "+str(successRate)+"%")
print("Failure Rate: "+str(100-successRate)+"%")
print("Average Steps On Success: "+str(regSuccessesSteps/regSuccesses))
print("Average Steps On Fail: "+str(regFailsSteps/regFails))
print("Running 4 Iterations of Hill Climb Search and Printing Paths: ")
for i in range(0,4):
    print("Iteration "+str(i+1)+": ")
    (queens,steps,path)=hillClimbSearch(n)
    printPath(n,path)
    if queens==None:
        print("(Fail)")
    else:
        print("(Pass)")

print("(Sideways Results may take a bit)")
sideFails=0
sideSuccesses=0
sideFailsSteps=0
sideSuccessesSteps=0
for i in range(0, iterations):
    (queens,steps,path)=hillClimbSearchSideways(n,sideways)
    if (queens==None):
        sideFails=sideFails+1
        sideFailsSteps=sideFailsSteps+steps
    else:
        sideSuccesses=sideSuccesses+1
        sideSuccessesSteps=sideSuccessesSteps+steps
print("Sideways Hill Climb Search Results:")
successRate=(sideSuccesses/(sideSuccesses+sideFails))*100
print("Success Rate: "+str(successRate)+"%")
print("Failure Rate: "+str(100-successRate)+"%")
print("Average Steps On Success: "+str(sideSuccessesSteps/sideSuccesses))
print("Average Steps On Fail: "+str(sideFailsSteps/sideFails))
print("Running 4 Iterations of Hill Climb Search w/Sideways and Printing Paths: ")
for i in range(0,4):
    print("Iteration "+str(i+1)+": ")
    (queens,steps,path)=hillClimbSearchSideways(n, sideways)
    printPath(n,path)
    if queens==None:
        print("(Fail)")
    else:
        print("(Pass)")

print("Random Restart Computing now over "+str(iterations)+" iterations...")
restartStepsReg=0
restartsReg=0
restartStepsSide=0
restartsSide=0
for i in range(0,iterations):
    queens=None
    while queens==None:
        (queens,steps,path)=hillClimbSearch(n)
        restartsReg=restartsReg+1
        restartStepsReg=restartStepsReg+steps
    queens=None
    while queens==None:
        (queens,steps,path)=hillClimbSearchSideways(n,sideways)
        restartsSide=restartsSide+1
        restartStepsSide=restartStepsSide+steps

print("Random-restart Hill Climbing Results: ")
print("Average number of Random Restarts per iteration (Regular): "+str(restartsReg/iterations))
print("Average number of Steps per iteration (Regular): "+str(restartStepsReg/iterations))
print("Average number of Random Restarts per iteration (Sideways): "+str(restartsSide/iterations))
print("Average number of Steps per iteration (Sideways): "+str(restartStepsSide/iterations))