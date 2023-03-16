# ITCS 6150
# Noah Foster
# Project 1

# Helper Function Finds the number given in given 2D array.
def findNum(array, num):
    i=0
    j=0
    while i<len(array):
        while j<len(array[i]):
            if array[i][j] == num:
                return (i,j)
            j=j+1
        j=0
        i=i+1
    return (None, None)
            
# Helper Function Swaps Two Spaces In 2D array, returning the new array.
def swapSpaces(array,i1,j1,i2,j2):
    array2=copy2dArray(array)
    temp = array2[i2][j2]
    array2[i2][j2]=array2[i1][j1]
    array2[i1][j1]=temp
    return array2

# Helper function to copy a 2d Array
def copy2dArray(array):
    array2 = []
    for each in array:
        array2.append(each.copy())
    return array2

# Helper Function to Print 2D Arrays.
def printArray(array):
    for row in array:
        string = ""
        for each in row:
            string = string + str(each) + " "
        print(string)
        
def printPath(path):
    for each in path[:-1]:
        printArray(each)
        print(" \/")
    printArray(path[len(path)-1])
    
# Helper Function to find possible swaps at this state of the array and return them in a list.
def findSwaps(array):
    swaps = []
    (zeroi,zeroj) = findNum(array, 0)
    if (zeroi>0):
        swaps.append(swapSpaces(array,zeroi,zeroj,zeroi-1,zeroj))
    if (zeroj>0):
        swaps.append(swapSpaces(array,zeroi,zeroj,zeroi,zeroj-1))
    if (zeroj<len(array[zeroi])-1):
        swaps.append(swapSpaces(array,zeroi,zeroj,zeroi,zeroj+1))
    if (zeroi<len(array)-1):
        swaps.append(swapSpaces(array,zeroi,zeroj,zeroi+1,zeroj))
    return swaps;

# Heuristic Functions (assume given arrays are equal in size)

# First Heuristic: Nodes Out Of Place.
def outOfPlace(array, goal):
    misplaced = 0
    i=0
    j=0
    while i<len(array):
        while j<len(array[i]):
            if array[i][j] != goal[i][j]:
                misplaced = misplaced+1
            j=j+1
        j=0
        i=i+1
    return misplaced;

# Second Heuristic: Manhattan Distance
def manhattanDistance(array, goal):
    distance=0
    i=0
    j=0
    while i<len(array):
        while j<len(array[i]):
            num = array[i][j]
            if num!=0:
                (i2,j2)=findNum(goal, num)
                idis = abs(i-i2)
                jdis = abs(j-j2)
                distance = distance + idis + jdis
            j=j+1
        j=0
        i=i+1
    return distance;

# Class to store an array, the path so far, and path cost so far
class Step:
    def __init__(self, gtemp, pathtemp, arraytemp):
        self.g = gtemp
        self.path = pathtemp
        self.array = copy2dArray(arraytemp)

import heapq

# Implementation of A*, takes in array, goal, and a h-cost function.
def AStar(array, goal, heuristic):
    generated = 0 # counter, used to count generated nodes.
    expanded = 0 # counter, used to count expanded nodes.
    g=0 
    h=heuristic(array,goal) # we get an initial estimation of h
    path = [] # we initialize an empty array for path so we can place it in the path slot of the first position.
    last = Step(g,[array],array) # we store the last array expanded, and initialize it as the first array.
    frontier=[]
    counter=0 # since heapq will take the second part of the tuple for tiebreakers, we need to make a counter to serve as a tiebreaker
    heapq.heapify(frontier) # heapq is used here to store the frontier, since it is a priority queue
    # the below line pushes to the heap the f cost, the tiebreaker, and the Step object, using a nested tuple. heapq only seems to take tuples of length 2, so this is necessary.
    heapq.heappush(frontier, (g+heuristic(array,goal), (counter,Step(g,path,array)))) 
    counter=counter+1 # increment the tiebreaker counter every time we add to the frontier.
    visited={str(array):True} # dictionary to store visited states. dictionaries in python are hashmaps, meaning it's way quicker to check if something is in it.
    while (h>0): # this loop will ensure we stop when we reach a solution.
        if len(frontier)==0: # so, if the frontier is ever empty, that means we expended all paths, and must break the loop, with no solution
            break
        (expandingF, (irrelevant, expanding)) = heapq.heappop(frontier) # we get the lowest value on the heap, and assign values. it first sorts by f, and if there are ties, it will take the one that was generated first, using the counter.
        last = expanding # set last, to be used if this is the solution.
        expanded = expanded + 1 # we are expanding a node, so increment expanded counter.
        toAdd = findSwaps(expanding.array) # so, toAdd uses findSwaps to get an array of possible swaps.
        for each in toAdd: # this loop increments through possible swaps to find ones we have not yet explored and puts them on the frontier.
            if str(each) in visited: # if we already explored this swap, we discard it.
                pass
            else: 
                generated = generated+1 # we are generating a node! increment the counter!
                addPath=expanding.path.copy() # we want to make a new array that stores the path for this node, we use array.copy()
                addPath.append(expanding.array) # appending the new part of the path.
                f=expanding.g+1+heuristic(each,goal) # the cost, used to sort the heap.
                heapq.heappush(frontier, (f, (counter,Step(expanding.g+1,addPath,each)))) #adding to heap
                counter=counter+1 # incrementing tiebreaker
                visited[str(each)]=True # add this node to the visited dictionary, so we will not visit it again.
        h=heuristic(expanding.array, goal) # the new h value. if this is zero, we exit the loop, because we have the solution!
    if (h>0): # this only acts if we exited the loop because of the break. We did not find a solution.
        print("Solution Not Found")
    else: # if we found a solution, print the path to it!
        if expanded==0: # message to help the user understand if they input the goal and solution as the same
            print("Did you mean to input identical Arrays as both Puzzle and Goal?")
        path = last.path
        path.append(last.array)
        print("Path: ")
        printPath(path)
    print("Nodes Generated: "+str(generated)) # we always want to print the nodes generated and expanded.
    print("Nodes Expanded: "+str(expanded))



# This is the User-Interactable section of the program. This is what runs the user side on the .py version.

print("A* 8 Puzzle Solver") # program title
numRows = int(input("Please type the number of rows the puzzle has: ")) 
numColumns = int(input("Please type the number of columns the puzzle has: "))
# technically, this program should work with any number of rows and columns, as long as the user stays consistent on the number they input in goal and puzzle.

# Code to take user input of puzzle array
array_input = []
print("Please type each row of the puzzle as a comma separated string, like this: 1,2,3 where the blank space is 0")
for x in range(0, numRows):
    row = []
    while len(row)!=numColumns: # while loop ensures proper entry
        row = input("Row "+str(x+1)+": ").split(",")
        if len(row)!=numColumns: # this catches incorrect user input.
            print("The number of elements entered should be consistent with the number of columns you entered. Try again.")
        else: 
            int_row = [int(num) for num in row]
    array_input.append(int_row)

# Code to take user input of goal array
goal_input = []
print("Please type each row of the goal state as a comma separated string, like this: 1,2,3 where the blank space is 0")
for x in range(0, numRows):
    row = []
    while len(row)!=numColumns: # while loop ensures proper entry
        row = input("Row "+str(x+1)+": ").split(",")
        if len(row)!=numColumns: # this catches incorrect user input.
            print("The number of elements entered should be consistent with the number of columns you entered. Try again.")
        else: 
            int_row = [int(num) for num in row]
    goal_input.append(int_row)
# mode selection and program execution.
mode = int(input("Please select a mode. Input 1 for the Out of Place Heuristic, 2 for Manhattan Distance, 3 for both: "))
if mode == 1:
    print(" ")
    print("Out of Place: ")
    AStar(array_input,goal_input,outOfPlace)
elif mode == 2:
    print(" ")
    print("Manhattan Distance: ")
    AStar(array_input,goal_input,manhattanDistance)
elif mode == 3:
    print(" ")
    print("Out of Place: ")
    AStar(array_input,goal_input,outOfPlace)
    print(" ")
    print("Manhattan Distance: ")
    AStar(array_input,goal_input,manhattanDistance)