# ITCS 6150
# Noah Foster
# Project 3
print("Noah Foster's ITCS 6150 Project 3")

# Helper to determine if color is a conflicting choice...
def isAdjacentColor(state, color, colors, adjacentLists):
    adjacent = adjacentLists[state]
    for each in adjacent:
        if color == colors[each]:
            return True
    return False
    

# Helper to find the first singleton (in the order)
def findSingleton(order, possibleColors):
    for each in order:
        if len(possibleColors[each])==1:
            return each
    return False

def recurDFS(adjacentLists, order, colors, possibleColors): # a recursive basic DFS function
    backtrack = 0
    if (len(order)==0): # our base case, we don't have any left to color
        #print("DONE!")
        return colors, 0
    curr = order[0] # the state we are coloring
    for each in possibleColors[curr]: # we want to loop through possible colors for the state until we run out
        isAdjacent = isAdjacentColor(curr, each, colors, adjacentLists)
        if (isAdjacent==False):
            neworder = order.copy() # copy order so we don't destroy it
            popped = neworder.pop(0) # remove the state we just colored from the new order list for recursion.
            newcolors = {} # copy colors so we don't destroy it
            for each2 in colors:
                newcolors[each2]=colors[each2]
            newcolors[curr]=each
            answer, backs = recurDFS(adjacentLists, neworder, newcolors, possibleColors) # recur
            if answer!=False: # this branch didn't fail, passing answer up
                return answer, backs+backtrack
            else: 
                backtrack+=backs
        else: 
            backtrack+=1
    return False, backtrack # we ran out of colors for the state

        
    

def ColorDepthFirst(adjacentLists, orderReference): # helper to ready the data for the recursive function.
    colors = {} # initializing variables
    maximum = 0
    done = False
    backtracks = 0
    while done!=True:
        for each in adjacentLists: # Intialize Colors as -1 to indicate blank
            colors[each]=-1
        possible = [] # set possible colors based on current max value
        for each in range(0,maximum+1):
            possible.append(each)
        #print(possible)
        possibleColors = {} # assign arrays of possible color values in dictionary
        for each in adjacentLists:
            possibleColors[each]=possible.copy()
        order = orderReference.copy() # make a copy of our priority order so we don't screw it up
        answer, back = recurDFS(adjacentLists, order, colors, possibleColors)
        if answer==False: # the algorithm failed with this many colors, try one more
            maximum=maximum+1
            #print(maximum)
            #print("Backtracks: "+str(back))
        else:
            colors = answer # the algorithm didn't fail, assign and return.
            done=True
        backtracks+=back
    return colors, backtracks




def recurDFSForward(adjacentLists, order, colors, possibleColors): # a recursive DFS function with forward checking
    backtrack = 0 # initialize backtrack counter
    if (len(order)==0): # our base case, we don't have any left to color
        #print("DONE!")
        return colors, 0
    curr = order[0] # the state we are coloring
    if len(possibleColors[curr])==0: # if this state has no possible colors, we are about to backtrack, increment counter
        backtrack+=1
    for each in possibleColors[curr]: # we want to loop through possible colors for the state until we run out
        isAdjacent = isAdjacentColor(curr, each, colors, adjacentLists)
        if (isAdjacent==False):
            neworder = order.copy() # copy order so we don't destroy it
            popped = neworder.pop(0) # remove the state we just colored from the new order list for recursion.
            newcolors = {} # copy colors so we don't destroy it
            for each2 in colors:
                newcolors[each2]=colors[each2]
            newcolors[curr]=each
            newPossibleColors={} # copy possible colors so we don't destroy it
            for each2 in possibleColors:
                newPossibleColors[each2]=possibleColors[each2].copy()
            adjacents=adjacentLists[curr] # find and check adjacent states (forward checking)
            for each2 in adjacents:
                if each in newPossibleColors[each2]:
                    newPossibleColors[each2].remove(each)
            answer, backs = recurDFSForward(adjacentLists, neworder, newcolors, newPossibleColors) # recur
            if answer!=False: # this branch didn't fail, passing answer up, adding up backtrack counter
                return answer, backs+backtrack
            else:
                backtrack+=backs
        else:
            backtrack+=1
    return False, backtrack # we ran out of colors for the state. pass up backtrack counter.

        
    

def ColorDepthFirstForward(adjacentLists, orderReference): # helper to ready the data for the recursive function.
    colors = {} # initializing variables
    maximum = 0
    done = False
    backtracks = 0
    while done!=True:
        for each in adjacentLists: # Intialize Colors as -1 to indicate blank
            colors[each]=-1
        possible = [] # set possible colors based on current max value
        for each in range(0,maximum+1):
            possible.append(each)
        #print(possible)
        possibleColors = {} # assign arrays of possible color values in dictionary
        for each in adjacentLists:
            possibleColors[each]=possible.copy()
        order = orderReference.copy() # make a copy of our priority order so we don't screw it up
        answer, back = recurDFSForward(adjacentLists, order, colors, possibleColors)
        if answer==False: # the algorithm failed with this many colors, try one more
            maximum=maximum+1
            #print(maximum)
            #print("Backtracks: "+str(back))
        else:
            colors = answer # the algorithm didn't fail, assign and return.
            done=True
        backtracks+=back
    return colors, backtracks
        
    
    
    
    
def recurDFSForwardSingleton(adjacentLists, order, colors, possibleColors): # a recursive DFS function with forward checking
    backtrack = 0
    if (len(order)==0): # our base case, we don't have any left to color
        #print("DONE!") # line used for testing
        return colors, 0
    singleton = findSingleton(order,possibleColors)
    if singleton==False:
        curr = order[0] # the state we are coloring
    else:
        # print("Singleton Found") # line used for initial testing
        curr = singleton
    if len(possibleColors[curr])==0: # if this state has no possible colors, we are about to backtrack, increment counter
        backtrack+=1
    for each in possibleColors[curr]: # we want to loop through possible colors for the state until we run out
        isAdjacent = isAdjacentColor(curr, each, colors, adjacentLists)
        if (isAdjacent==False):
            neworder = order.copy() # copy order so we don't destroy it
            popped = neworder.remove(curr) # remove the state we just colored from the new order list for recursion.
            newcolors = {} # copy colors so we don't destroy it
            for each2 in colors:
                newcolors[each2]=colors[each2]
            newcolors[curr]=each
            newPossibleColors={} # copy possible colors so we don't destroy it
            for each2 in possibleColors:
                newPossibleColors[each2]=possibleColors[each2].copy()
            adjacents=adjacentLists[curr] # find and check adjacent states (forward checking)
            for each2 in adjacents:
                if each in newPossibleColors[each2]:
                    newPossibleColors[each2].remove(each)
            answer, backs = recurDFSForwardSingleton(adjacentLists, neworder, newcolors, newPossibleColors) # recur
            if answer!=False: # this branch didn't fail, passing answer up
                return answer, backs+backtrack 
            else:
                backtrack+=backs # counting backtracks for failure purposes
        else:
            backtrack+=1
    return False, backtrack # we ran out of colors for the state

        
    

def ColorDepthFirstForwardSingleton(adjacentLists, orderReference): # helper to ready the data for the recursive function.
    colors = {} # initializing variables
    maximum = 0
    done = False
    backtracks = 0
    while done!=True:
        for each in adjacentLists: # Intialize Colors as -1 to indicate blank
            colors[each]=-1
        possible = [] # set possible colors based on current max value
        for each in range(0,maximum+1):
            possible.append(each)
        #print(possible)
        possibleColors = {} # assign arrays of possible color values in dictionary
        for each in adjacentLists:
            possibleColors[each]=possible.copy()
        order = orderReference.copy() # make a copy of our priority order so we don't screw it up
        answer, back = recurDFSForwardSingleton(adjacentLists, order, colors, possibleColors)
        if answer==False: # the algorithm failed with this many colors, try one more
            maximum=maximum+1
            
            #print(maximum)
            #print("Backtracks: "+str(back))
        else:
            colors = answer # the algorithm didn't fail, assign and return.
            done=True
        backtracks+=back
    return colors, backtracks
        
import heapq
# Helper to Heuristic-Sort the order list
def chooseState(order, adjacentLists, possibleColors):
    newOrder=[]
    heapq.heapify(newOrder)
    for each in order:
        index = order.index(each)
        numColors = len(possibleColors[each]) # MRV
        numAdjacent = 0
        for each2 in adjacentLists[each]:
            if each2 in order:
                numAdjacent+=1
        heapq.heappush(newOrder, (numColors, -1*numAdjacent, each))
    retNewOrder=[]
    for each in newOrder:
        (coln, adjn, val) = each
        retNewOrder.append(val)
    return retNewOrder

def chooseColors(state, adjacentLists, order, possibleColors):
    possibles = possibleColors[state]
    sortPossibles = []
    heapq.heapify(sortPossibles)
    adjacents = adjacentLists[state]
    for color in possibles:
        rulesout = 0
        for each in adjacents:
            if each in order:
                if color in possibleColors[each]:
                    rulesout+=1
        heapq.heappush(sortPossibles, (rulesout,color))
    retPossibles = []
    for each in sortPossibles:
        (rulesN,color)=each
        retPossibles.append(color)
            
    return retPossibles

# Helper to find the list of singletons
def findSingletons(order, possibleColors):
    singletons = []
    for each in order:
        if len(possibleColors[each])==1:
            singletons.append(each)
    if len(singletons)==0:
        return False
    else: 
        return singletons


def recurDFSH(adjacentLists, order, colors, possibleColors): # a recursive basic DFS function
    backtrack = 0
    if (len(order)==0): # our base case, we don't have any left to color
        #print("DONE!")
        return colors, 0
    order = order.copy() 
    order = chooseState(order, adjacentLists, possibleColors) # running heuristic sort on list
    curr = order[0] # the state we are coloring
    possSort = chooseColors(curr, adjacentLists, order, possibleColors)
    for each in possSort: # we want to loop through possible colors for the state until we run out
        isAdjacent = isAdjacentColor(curr, each, colors, adjacentLists)
        if (isAdjacent==False):
            neworder = order.copy() # copy order so we don't destroy it
            popped = neworder.pop(0) # remove the state we just colored from the new order list for recursion.
            newcolors = {} # copy colors so we don't destroy it
            for each2 in colors:
                newcolors[each2]=colors[each2]
            newcolors[curr]=each
            answer, backs = recurDFSH(adjacentLists, neworder, newcolors, possibleColors) # recur
            if answer!=False: # this branch didn't fail, passing answer up
                return answer, backs+backtrack
            else: 
                backtrack+=backs
        else: 
            backtrack+=1
    return False, backtrack # we ran out of colors for the state

        
    

def ColorDepthFirstH(adjacentLists, orderReference): # helper to ready the data for the recursive function.
    colors = {} # initializing variables
    maximum = 0
    done = False
    backtracks = 0
    while done!=True:
        for each in adjacentLists: # Intialize Colors as -1 to indicate blank
            colors[each]=-1
        possible = [] # set possible colors based on current max value
        for each in range(0,maximum+1):
            possible.append(each)
        #print(possible)
        possibleColors = {} # assign arrays of possible color values in dictionary
        for each in adjacentLists:
            possibleColors[each]=possible.copy()
        order = orderReference.copy() # make a copy of our priority order so we don't screw it up
        answer, back = recurDFSH(adjacentLists, order, colors, possibleColors)
        if answer==False: # the algorithm failed with this many colors, try one more
            maximum=maximum+1
            #print(maximum)
            #print("Backtracks: "+str(back))
        else:
            colors = answer # the algorithm didn't fail, assign and return.
            done=True
        backtracks+=back
    return colors, backtracks




def recurDFSForwardH(adjacentLists, order, colors, possibleColors): # a recursive DFS function with forward checking
    backtrack = 0 # initialize backtrack counter
    if (len(order)==0): # our base case, we don't have any left to color
        #print("DONE!")
        return colors, 0
    order = order.copy()
    order = chooseState(order, adjacentLists, possibleColors) # running heuristic sort on list
    curr = order[0] # the state we are coloring
    if len(possibleColors[curr])==0: # if this state has no possible colors, we are about to backtrack, increment counter
        backtrack+=1
    possSort = chooseColors(curr, adjacentLists, order, possibleColors)
    for each in possSort: # we want to loop through possible colors for the state until we run out
        isAdjacent = isAdjacentColor(curr, each, colors, adjacentLists)
        if (isAdjacent==False):
            neworder = order.copy() # copy order so we don't destroy it
            popped = neworder.pop(0) # remove the state we just colored from the new order list for recursion.
            newcolors = {} # copy colors so we don't destroy it
            for each2 in colors:
                newcolors[each2]=colors[each2]
            newcolors[curr]=each
            newPossibleColors={} # copy possible colors so we don't destroy it
            for each2 in possibleColors:
                newPossibleColors[each2]=possibleColors[each2].copy()
            adjacents=adjacentLists[curr] # find and check adjacent states (forward checking)
            for each2 in adjacents:
                if each in newPossibleColors[each2]:
                    newPossibleColors[each2].remove(each)
            answer, backs = recurDFSForwardH(adjacentLists, neworder, newcolors, newPossibleColors) # recur
            if answer!=False: # this branch didn't fail, passing answer up, adding up backtrack counter
                return answer, backs+backtrack
            else:
                backtrack+=backs
        else:
            backtrack+=1
    return False, backtrack # we ran out of colors for the state. pass up backtrack counter.

        
    

def ColorDepthFirstForwardH(adjacentLists, orderReference): # helper to ready the data for the recursive function.
    colors = {} # initializing variables
    maximum = 0
    done = False
    backtracks = 0
    while done!=True:
        for each in adjacentLists: # Intialize Colors as -1 to indicate blank
            colors[each]=-1
        possible = [] # set possible colors based on current max value
        for each in range(0,maximum+1):
            possible.append(each)
        #print(possible)
        possibleColors = {} # assign arrays of possible color values in dictionary
        for each in adjacentLists:
            possibleColors[each]=possible.copy()
        order = orderReference.copy() # make a copy of our priority order so we don't screw it up
        answer, back = recurDFSForwardH(adjacentLists, order, colors, possibleColors)
        if answer==False: # the algorithm failed with this many colors, try one more
            maximum=maximum+1
            #print(maximum)
            #print("Backtracks: "+str(back))
        else:
            colors = answer # the algorithm didn't fail, assign and return.
            done=True
            backtracks+=back
    return colors, backtracks
        
    
    
    
    
def recurDFSForwardSingletonH(adjacentLists, order, colors, possibleColors): # a recursive DFS function with forward checking
    backtrack = 0
    if (len(order)==0): # our base case, we don't have any left to color
        #print("DONE!") # line used for testing
        return colors, 0
    singletons = findSingletons(order,possibleColors)
    if singletons==False:
        order = order.copy()
        order = chooseState(order, adjacentLists, possibleColors) # running heuristic sort on list
        curr = order[0] # the state we are coloring
    else:
        # print("Singleton Found") # line used for initial testing
        singletons = singletons.copy()
        singletons = chooseState(singletons, adjacentLists, possibleColors) # running heuristic sort on list
        curr = singletons[0]
    if len(possibleColors[curr])==0: # if this state has no possible colors, we are about to backtrack, increment counter
        backtrack+=1
    possSort = chooseColors(curr, adjacentLists, order, possibleColors)
    for each in possSort: # we want to loop through possible colors for the state until we run out
        isAdjacent = isAdjacentColor(curr, each, colors, adjacentLists)
        if (isAdjacent==False):
            neworder = order.copy() # copy order so we don't destroy it
            popped = neworder.remove(curr) # remove the state we just colored from the new order list for recursion.
            newcolors = {} # copy colors so we don't destroy it
            for each2 in colors:
                newcolors[each2]=colors[each2]
            newcolors[curr]=each
            newPossibleColors={} # copy possible colors so we don't destroy it
            for each2 in possibleColors:
                newPossibleColors[each2]=possibleColors[each2].copy()
            adjacents=adjacentLists[curr] # find and check adjacent states (forward checking)
            for each2 in adjacents:
                if each in newPossibleColors[each2]:
                    newPossibleColors[each2].remove(each)
            answer, backs = recurDFSForwardSingletonH(adjacentLists, neworder, newcolors, newPossibleColors) # recur
            if answer!=False: # this branch didn't fail, passing answer up
                return answer, backs+backtrack 
            else:
                backtrack+=backs # counting backtracks for failure purposes
        else:
            backtrack+=1
    return False, backtrack # we ran out of colors for the state

        
    

def ColorDepthFirstForwardSingletonH(adjacentLists, orderReference): # helper to ready the data for the recursive function.
    colors = {} # initializing variables
    maximum = 0
    done = False
    backtracks = 0
    while done!=True:
        for each in adjacentLists: # Intialize Colors as -1 to indicate blank
            colors[each]=-1
        possible = [] # set possible colors based on current max value
        for each in range(0,maximum+1):
            possible.append(each)
        #print(possible)
        possibleColors = {} # assign arrays of possible color values in dictionary
        for each in adjacentLists:
            possibleColors[each]=possible.copy()
        order = orderReference.copy() # make a copy of our priority order so we don't screw it up
        answer, back = recurDFSForwardSingletonH(adjacentLists, order, colors, possibleColors)
        if answer==False: # the algorithm failed with this many colors, try one more
            maximum=maximum+1
            #print(maximum)
            #print("Backtracks: "+str(back))
        else:
            colors = answer # the algorithm didn't fail, assign and return.
            done=True
        backtracks+=back
    return colors, backtracks
        

# I tried using geopandas for visualization, but its dependencies didn't want to install for some reason.

print("Loading Data and Performing Sanity Check...")
# America Adjacent States Data
AmericaAdjacentStates = { 
    "Alabama":["Mississippi", "Tennessee", "Florida", "Georgia"],
    "Alaska":[],
    "Arizona":["Nevada", "New Mexico", "Utah", "California", "Colorado"],
    "Arkansas":["Oklahoma","Tennessee","Texas","Louisiana","Mississippi","Missouri"],
    "California":["Oregon","Arizona","Nevada"],
    "Colorado":["New Mexico","Oklahoma","Utah","Wyoming","Arizona","Kansas","Nebraska"],
    "Connecticut":["New York","Rhode Island","Massachusetts"],
    "Delaware":["New Jersey","Pennsylvania","Maryland"],
    "Florida":["Georgia","Alabama"],
    "Georgia":["North Carolina","South Carolina","Tennessee","Alabama","Florida"],
    "Hawaii":[],
    "Idaho":["Utah", "Washington","Wyoming","Montana","Nevada","Oregon"],
    "Illinois":["Kentucky","Missouri","Wisconsin","Indiana","Iowa","Michigan"],
    "Indiana":["Michigan","Ohio","Illinois","Kentucky"],
    "Iowa":["Nebraska","South Dakota","Wisconsin","Illinois","Minnesota","Missouri"],
    "Kansas":["Nebraska","Oklahoma","Colorado","Missouri"],
    "Kentucky":["Tennessee","Virginia","West Virginia","Illinois","Indiana","Missouri","Ohio"],
    "Louisiana":["Texas","Arkansas","Mississippi"],
    "Maine":["New Hampshire"],
    "Maryland":["Virginia","West Virginia","Delaware","Pennsylvania"],
    "Massachusetts":["New York","Rhode Island","Vermont","Connecticut","New Hampshire"],
    "Michigan":["Ohio","Wisconsin","Illinois","Indiana","Minnesota"],
    "Minnesota":["North Dakota","South Dakota","Wisconsin","Iowa","Michigan"],
    "Mississippi":["Louisiana","Tennessee","Alabama","Arkansas"],
    "Missouri":["Nebraska","Oklahoma","Tennessee","Arkansas","Illinois","Iowa","Kansas","Kentucky"],
    "Montana":["South Dakota","Wyoming","Idaho","North Dakota"],
    "Nebraska":["Missouri","South Dakota","Wyoming","Colorado","Iowa","Kansas"],
    "Nevada":["Idaho","Oregon","Utah","Arizona","California"],
    "New Hampshire":["Vermont","Maine","Massachusetts"],
    "New Jersey":["Pennsylvania","Delaware","New York"],
    "New Mexico":["Oklahoma","Texas","Utah","Arizona","Colorado"],
    "New York":["Pennsylvania","Rhode Island","Vermont","Connecticut","Massachusetts","New Jersey"],
    "North Carolina":["Tennessee","Virginia","Georgia","South Carolina"],
    "North Dakota":["South Dakota","Minnesota","Montana"],
    "Ohio":["Michigan","Pennsylvania","West Virginia","Indiana","Kentucky"],
    "Oklahoma":["Missouri","New Mexico","Texas","Arkansas","Colorado","Kansas"],
    "Oregon":["Nevada","Washington","California","Idaho"],
    "Pennsylvania":["New York","Ohio","West Virginia","Delaware","Maryland","New Jersey"],
    "Rhode Island":["Massachusetts","New York","Connecticut"],
    "South Carolina":["North Carolina","Georgia"],
    "South Dakota":["Nebraska","North Dakota","Wyoming","Iowa","Minnesota","Montana"],
    "Tennessee":["Mississippi","Missouri","North Carolina","Virginia","Alabama","Arkansas","Georgia","Kentucky"],
    "Texas":["New Mexico","Oklahoma","Arkansas","Louisiana"],
    "Utah":["Nevada","New Mexico","Wyoming","Arizona","Colorado","Idaho"],
    "Vermont":["New Hampshire","New York","Massachusetts"],
    "Virginia":["North Carolina","Tennessee","West Virginia","Kentucky","Maryland"],
    "Washington":["Oregon","Idaho"],
    "West Virginia":["Pennsylvania","Virginia","Kentucky","Maryland","Ohio"],
    "Wisconsin":["Michigan","Minnesota","Illinois","Iowa"],
    "Wyoming":["Nebraska","South Dakota","Utah","Colorado","Idaho","Montana"]
}

# Checking List Validity for spelling errors and length errors
AmericaStates={}
for each in AmericaAdjacentStates:
    AmericaStates[each] = True
    for each2 in AmericaAdjacentStates[each]:
        AmericaStates[each2]=True
print("Number of Unique States in America List: " + str(len(AmericaStates)))


# Australia Adjacent States Data
AustraliaAdjacentStates = {
    "New South Wales":["South Australia","Victoria","Queensland"],
    "Northern Territory":["South Australia","Queensland","Western Australia"],
    "Queensland":["New South Wales","South Australia","Northern Territory"],
    "South Australia":["New South Wales","Northern Territory","Queensland","Victoria","Western Australia"],
    "Victoria":["New South Wales", "South Australia"],
    "Western Australia":["Northern Territory","South Australia"],
    "Tasmania":[]
}

# Checking List Validity for spelling errors and length errors
AustraliaStates={}
for each in AustraliaAdjacentStates:
    AustraliaStates[each] = True
    for each2 in AustraliaAdjacentStates[each]:
        AustraliaStates[each2]=True
print("Number of Unique States in Australia List: " + str(len(AustraliaStates)))
print("\n")

import random
import timeit

print("This program colors maps of Australia and the US using CSP techniques")
print("Running on Four Random Australia Arrangements without Heuristic:")
AustraliaOrder1 = []
for each in AustraliaAdjacentStates:
    AustraliaOrder1.append(each)
random.shuffle(AustraliaOrder1)
AustraliaOrder2 = []
for each in AustraliaAdjacentStates:
    AustraliaOrder2.append(each)
random.shuffle(AustraliaOrder2)
AustraliaOrder3 = []
for each in AustraliaAdjacentStates:
    AustraliaOrder3.append(each)
random.shuffle(AustraliaOrder3)
AustraliaOrder4 = []
for each in AustraliaAdjacentStates:
    AustraliaOrder4.append(each)
random.shuffle(AustraliaOrder4)
print()
print("Order 1: \n"+str(AustraliaOrder1))
print("Order 2: \n"+str(AustraliaOrder2))
print("Order 3: \n"+str(AustraliaOrder3))
print("Order 4: \n"+str(AustraliaOrder4))


start = timeit.default_timer()
AustraliaColored1, backtracks1 = ColorDepthFirst(AustraliaAdjacentStates, AustraliaOrder1)
end = timeit.default_timer()
time1 = end-start

start = timeit.default_timer()
AustraliaColored2, backtracks2 = ColorDepthFirst(AustraliaAdjacentStates, AustraliaOrder2)
end = timeit.default_timer()
time2 = end-start

start = timeit.default_timer()
AustraliaColored3, backtracks3 = ColorDepthFirst(AustraliaAdjacentStates, AustraliaOrder3)
end = timeit.default_timer()
time3 = end-start

start = timeit.default_timer()
AustraliaColored4, backtracks4 = ColorDepthFirst(AustraliaAdjacentStates, AustraliaOrder4)
end = timeit.default_timer()
time4 = end-start

print()
print("Order 1 DFS:")
print("Took "+str(time1)+" seconds and "+str(backtracks1)+" backtracks to find this solution:")
print(AustraliaColored1)
print()
print("Order 2 DFS:")
print("Took "+str(time2)+" seconds and "+str(backtracks2)+" backtracks to find this solution:")
print(AustraliaColored2)
print()
print("Order 3 DFS:")
print("Took "+str(time3)+" seconds and "+str(backtracks3)+" backtracks to find this solution:")
print(AustraliaColored3)
print()
print("Order 4 DFS:")
print("Took "+str(time4)+" seconds and "+str(backtracks4)+" backtracks to find this solution:")
print(AustraliaColored4)
print()
avAusDFSback = (backtracks1+backtracks2+backtracks3+backtracks4)/4
avAusDFStime = (time1+time2+time3+time4)/4

start = timeit.default_timer()
AustraliaColored1, backtracks1 = ColorDepthFirstForward(AustraliaAdjacentStates, AustraliaOrder1)
end = timeit.default_timer()
time1 = end-start

start = timeit.default_timer()
AustraliaColored2, backtracks2 = ColorDepthFirstForward(AustraliaAdjacentStates, AustraliaOrder2)
end = timeit.default_timer()
time2 = end-start

start = timeit.default_timer()
AustraliaColored3, backtracks3 = ColorDepthFirstForward(AustraliaAdjacentStates, AustraliaOrder3)
end = timeit.default_timer()
time3 = end-start

start = timeit.default_timer()
AustraliaColored4, backtracks4 = ColorDepthFirstForward(AustraliaAdjacentStates, AustraliaOrder4)
end = timeit.default_timer()
time4 = end-start

print()
print("Order 1 DFS w/ Forward:")
print("Took "+str(time1)+" seconds and "+str(backtracks1)+" backtracks to find this solution:")
print(AustraliaColored1)
print()
print("Order 2 DFS w/ Forward:")
print("Took "+str(time2)+" seconds and "+str(backtracks2)+" backtracks to find this solution:")
print(AustraliaColored2)
print()
print("Order 3 DFS w/ Forward:")
print("Took "+str(time3)+" seconds and "+str(backtracks3)+" backtracks to find this solution:")
print(AustraliaColored3)
print()
print("Order 4 DFS w/ Forward:")
print("Took "+str(time4)+" seconds and "+str(backtracks4)+" backtracks to find this solution:")
print(AustraliaColored4)
print()
avAusDFSFback = (backtracks1+backtracks2+backtracks3+backtracks4)/4
avAusDFSFtime = (time1+time2+time3+time4)/4

start = timeit.default_timer()
AustraliaColored1, backtracks1 = ColorDepthFirstForwardSingleton(AustraliaAdjacentStates, AustraliaOrder1)
end = timeit.default_timer()
time1 = end-start

start = timeit.default_timer()
AustraliaColored2, backtracks2 = ColorDepthFirstForwardSingleton(AustraliaAdjacentStates, AustraliaOrder2)
end = timeit.default_timer()
time2 = end-start

start = timeit.default_timer()
AustraliaColored3, backtracks3 = ColorDepthFirstForwardSingleton(AustraliaAdjacentStates, AustraliaOrder3)
end = timeit.default_timer()
time3 = end-start

start = timeit.default_timer()
AustraliaColored4, backtracks4 = ColorDepthFirstForwardSingleton(AustraliaAdjacentStates, AustraliaOrder4)
end = timeit.default_timer()
time4 = end-start

print()
print("Order 1 DFS w/ Forward and Singleton:")
print("Took "+str(time1)+" seconds and "+str(backtracks1)+" backtracks to find this solution:")
print(AustraliaColored1)
print()
print("Order 2 DFS w/ Forward and Singleton:")
print("Took "+str(time2)+" seconds and "+str(backtracks2)+" backtracks to find this solution:")
print(AustraliaColored2)
print()
print("Order 3 DFS w/ Forward and Singleton:")
print("Took "+str(time3)+" seconds and "+str(backtracks3)+" backtracks to find this solution:")
print(AustraliaColored3)
print()
print("Order 4 DFS w/ Forward and Singleton:")
print("Took "+str(time4)+" seconds and "+str(backtracks4)+" backtracks to find this solution:")
print(AustraliaColored4)
print()
avAusDFSFSback = (backtracks1+backtracks2+backtracks3+backtracks4)/4
avAusDFSFStime = (time1+time2+time3+time4)/4


print("Running on Four Random America Arrangements without Heuristic:")
AmericaOrder1 = []
for each in AmericaAdjacentStates:
    AmericaOrder1.append(each)
random.shuffle(AmericaOrder1)
AmericaOrder2 = []
for each in AmericaAdjacentStates:
    AmericaOrder2.append(each)
random.shuffle(AmericaOrder2)
AmericaOrder3 = []
for each in AmericaAdjacentStates:
    AmericaOrder3.append(each)
random.shuffle(AmericaOrder3)
AmericaOrder4 = []
for each in AmericaAdjacentStates:
    AmericaOrder4.append(each)
random.shuffle(AmericaOrder4)
print()
print("Order 1: \n"+str(AmericaOrder1))
print("Order 2: \n"+str(AmericaOrder2))
print("Order 3: \n"+str(AmericaOrder3))
print("Order 4: \n"+str(AmericaOrder4))


start = timeit.default_timer()
AmericaColored1, backtracks1 = ColorDepthFirst(AmericaAdjacentStates, AmericaOrder1)
end = timeit.default_timer()
time1 = end-start
print(".")
start = timeit.default_timer()
AmericaColored2, backtracks2 = ColorDepthFirst(AmericaAdjacentStates, AmericaOrder2)
end = timeit.default_timer()
time2 = end-start
print(".")
start = timeit.default_timer()
AmericaColored3, backtracks3 = ColorDepthFirst(AmericaAdjacentStates, AmericaOrder3)
end = timeit.default_timer()
time3 = end-start
print(".")
start = timeit.default_timer()
AmericaColored4, backtracks4 = ColorDepthFirst(AmericaAdjacentStates, AmericaOrder4)
end = timeit.default_timer()
time4 = end-start
print(".")
print()
print("Order 1 DFS:")
print("Took "+str(time1)+" seconds and "+str(backtracks1)+" backtracks to find this solution:")
print(AmericaColored1)
print()
print("Order 2 DFS:")
print("Took "+str(time2)+" seconds and "+str(backtracks2)+" backtracks to find this solution:")
print(AmericaColored2)
print()
print("Order 3 DFS:")
print("Took "+str(time3)+" seconds and "+str(backtracks3)+" backtracks to find this solution:")
print(AmericaColored3)
print()
print("Order 4 DFS:")
print("Took "+str(time4)+" seconds and "+str(backtracks4)+" backtracks to find this solution:")
print(AmericaColored4)
print()
avAmDFSback = (backtracks1+backtracks2+backtracks3+backtracks4)/4
avAmDFStime = (time1+time2+time3+time4)/4

start = timeit.default_timer()
AmericaColored1, backtracks1 = ColorDepthFirstForward(AmericaAdjacentStates, AmericaOrder1)
end = timeit.default_timer()
time1 = end-start
print(".")
start = timeit.default_timer()
AmericaColored2, backtracks2 = ColorDepthFirstForward(AmericaAdjacentStates, AmericaOrder2)
end = timeit.default_timer()
time2 = end-start
print(".")
start = timeit.default_timer()
AmericaColored3, backtracks3 = ColorDepthFirstForward(AmericaAdjacentStates, AmericaOrder3)
end = timeit.default_timer()
time3 = end-start
print(".")
start = timeit.default_timer()
AmericaColored4, backtracks4 = ColorDepthFirstForward(AmericaAdjacentStates, AmericaOrder4)
end = timeit.default_timer()
time4 = end-start
print(".")
print()
print("Order 1 DFS w/ Forward:")
print("Took "+str(time1)+" seconds and "+str(backtracks1)+" backtracks to find this solution:")
print(AmericaColored1)
print()
print("Order 2 DFS w/ Forward:")
print("Took "+str(time2)+" seconds and "+str(backtracks2)+" backtracks to find this solution:")
print(AmericaColored2)
print()
print("Order 3 DFS w/ Forward:")
print("Took "+str(time3)+" seconds and "+str(backtracks3)+" backtracks to find this solution:")
print(AmericaColored3)
print()
print("Order 4 DFS w/ Forward:")
print("Took "+str(time4)+" seconds and "+str(backtracks4)+" backtracks to find this solution:")
print(AmericaColored4)
print()
avAmDFSFback = (backtracks1+backtracks2+backtracks3+backtracks4)/4
avAmDFSFtime = (time1+time2+time3+time4)/4

start = timeit.default_timer()
AmericaColored1, backtracks1 = ColorDepthFirstForwardSingleton(AmericaAdjacentStates, AmericaOrder1)
end = timeit.default_timer()
time1 = end-start
print(".")
start = timeit.default_timer()
AmericaColored2, backtracks2 = ColorDepthFirstForwardSingleton(AmericaAdjacentStates, AmericaOrder2)
end = timeit.default_timer()
time2 = end-start
print(".")
start = timeit.default_timer()
AmericaColored3, backtracks3 = ColorDepthFirstForwardSingleton(AmericaAdjacentStates, AmericaOrder3)
end = timeit.default_timer()
time3 = end-start
print(".")
start = timeit.default_timer()
AmericaColored4, backtracks4 = ColorDepthFirstForwardSingleton(AmericaAdjacentStates, AmericaOrder4)
end = timeit.default_timer()
time4 = end-start
print(".")
print()
print("Order 1 DFS w/ Forward and Singleton:")
print("Took "+str(time1)+" seconds and "+str(backtracks1)+" backtracks to find this solution:")
print(AmericaColored1)
print()
print("Order 2 DFS w/ Forward and Singleton:")
print("Took "+str(time2)+" seconds and "+str(backtracks2)+" backtracks to find this solution:")
print(AmericaColored2)
print()
print("Order 3 DFS w/ Forward and Singleton:")
print("Took "+str(time3)+" seconds and "+str(backtracks3)+" backtracks to find this solution:")
print(AmericaColored3)
print()
print("Order 4 DFS w/ Forward and Singleton:")
print("Took "+str(time4)+" seconds and "+str(backtracks4)+" backtracks to find this solution:")
print(AmericaColored4)
print()
avAmDFSFSback = (backtracks1+backtracks2+backtracks3+backtracks4)/4
avAmDFSFStime = (time1+time2+time3+time4)/4

print("Running on the same Four Random Australia Arrangements with Heuristic:")

print()
print("Order 1: \n"+str(AustraliaOrder1))
print("Order 2: \n"+str(AustraliaOrder2))
print("Order 3: \n"+str(AustraliaOrder3))
print("Order 4: \n"+str(AustraliaOrder4))


start = timeit.default_timer()
AustraliaColored1, backtracks1 = ColorDepthFirstH(AustraliaAdjacentStates, AustraliaOrder1)
end = timeit.default_timer()
time1 = end-start

start = timeit.default_timer()
AustraliaColored2, backtracks2 = ColorDepthFirstH(AustraliaAdjacentStates, AustraliaOrder2)
end = timeit.default_timer()
time2 = end-start

start = timeit.default_timer()
AustraliaColored3, backtracks3 = ColorDepthFirstH(AustraliaAdjacentStates, AustraliaOrder3)
end = timeit.default_timer()
time3 = end-start

start = timeit.default_timer()
AustraliaColored4, backtracks4 = ColorDepthFirstH(AustraliaAdjacentStates, AustraliaOrder4)
end = timeit.default_timer()
time4 = end-start

print()
print("Order 1 DFS w/ Heuristics:")
print("Took "+str(time1)+" seconds and "+str(backtracks1)+" backtracks to find this solution:")
print(AustraliaColored1)
print()
print("Order 2 DFS w/ Heuristics:")
print("Took "+str(time2)+" seconds and "+str(backtracks2)+" backtracks to find this solution:")
print(AustraliaColored2)
print()
print("Order 3 DFS w/ Heuristics:")
print("Took "+str(time3)+" seconds and "+str(backtracks3)+" backtracks to find this solution:")
print(AustraliaColored3)
print()
print("Order 4 DFS w/ Heuristics:")
print("Took "+str(time4)+" seconds and "+str(backtracks4)+" backtracks to find this solution:")
print(AustraliaColored4)
print()
avAusDFSHback = (backtracks1+backtracks2+backtracks3+backtracks4)/4
avAusDFSHtime = (time1+time2+time3+time4)/4

start = timeit.default_timer()
AustraliaColored1, backtracks1 = ColorDepthFirstForwardH(AustraliaAdjacentStates, AustraliaOrder1)
end = timeit.default_timer()
time1 = end-start

start = timeit.default_timer()
AustraliaColored2, backtracks2 = ColorDepthFirstForwardH(AustraliaAdjacentStates, AustraliaOrder2)
end = timeit.default_timer()
time2 = end-start

start = timeit.default_timer()
AustraliaColored3, backtracks3 = ColorDepthFirstForwardH(AustraliaAdjacentStates, AustraliaOrder3)
end = timeit.default_timer()
time3 = end-start

start = timeit.default_timer()
AustraliaColored4, backtracks4 = ColorDepthFirstForwardH(AustraliaAdjacentStates, AustraliaOrder4)
end = timeit.default_timer()
time4 = end-start

print()
print("Order 1 DFS w/ Forward and Heuristics:")
print("Took "+str(time1)+" seconds and "+str(backtracks1)+" backtracks to find this solution:")
print(AustraliaColored1)
print()
print("Order 2 DFS w/ Forward and Heuristics:")
print("Took "+str(time2)+" seconds and "+str(backtracks2)+" backtracks to find this solution:")
print(AustraliaColored2)
print()
print("Order 3 DFS w/ Forward and Heuristics:")
print("Took "+str(time3)+" seconds and "+str(backtracks3)+" backtracks to find this solution:")
print(AustraliaColored3)
print()
print("Order 4 DFS w/ Forward and Heuristics:")
print("Took "+str(time4)+" seconds and "+str(backtracks4)+" backtracks to find this solution:")
print(AustraliaColored4)
print()
avAusDFSFHback = (backtracks1+backtracks2+backtracks3+backtracks4)/4
avAusDFSFHtime = (time1+time2+time3+time4)/4

start = timeit.default_timer()
AustraliaColored1, backtracks1 = ColorDepthFirstForwardSingletonH(AustraliaAdjacentStates, AustraliaOrder1)
end = timeit.default_timer()
time1 = end-start

start = timeit.default_timer()
AustraliaColored2, backtracks2 = ColorDepthFirstForwardSingletonH(AustraliaAdjacentStates, AustraliaOrder2)
end = timeit.default_timer()
time2 = end-start

start = timeit.default_timer()
AustraliaColored3, backtracks3 = ColorDepthFirstForwardSingletonH(AustraliaAdjacentStates, AustraliaOrder3)
end = timeit.default_timer()
time3 = end-start

start = timeit.default_timer()
AustraliaColored4, backtracks4 = ColorDepthFirstForwardSingletonH(AustraliaAdjacentStates, AustraliaOrder4)
end = timeit.default_timer()
time4 = end-start

print()
print("Order 1 DFS w/ Forward and Singleton and Heuristics:")
print("Took "+str(time1)+" seconds and "+str(backtracks1)+" backtracks to find this solution:")
print(AustraliaColored1)
print()
print("Order 2 DFS w/ Forward and Singleton and Heuristics:")
print("Took "+str(time2)+" seconds and "+str(backtracks2)+" backtracks to find this solution:")
print(AustraliaColored2)
print()
print("Order 3 DFS w/ Forward and Singleton and Heuristics:")
print("Took "+str(time3)+" seconds and "+str(backtracks3)+" backtracks to find this solution:")
print(AustraliaColored3)
print()
print("Order 4 DFS w/ Forward and Singleton and Heuristics:")
print("Took "+str(time4)+" seconds and "+str(backtracks4)+" backtracks to find this solution:")
print(AustraliaColored4)
print()
avAusDFSFSHback = (backtracks1+backtracks2+backtracks3+backtracks4)/4
avAusDFSFSHtime = (time1+time2+time3+time4)/4


print("Running on the same Four Random America Arrangements with Heuristic:")

print()
print("Order 1: \n"+str(AmericaOrder1))
print("Order 2: \n"+str(AmericaOrder2))
print("Order 3: \n"+str(AmericaOrder3))
print("Order 4: \n"+str(AmericaOrder4))


start = timeit.default_timer()
AmericaColored1, backtracks1 = ColorDepthFirstH(AmericaAdjacentStates, AmericaOrder1)
end = timeit.default_timer()
time1 = end-start
print(".")
start = timeit.default_timer()
AmericaColored2, backtracks2 = ColorDepthFirstH(AmericaAdjacentStates, AmericaOrder2)
end = timeit.default_timer()
time2 = end-start
print(".")
start = timeit.default_timer()
AmericaColored3, backtracks3 = ColorDepthFirstH(AmericaAdjacentStates, AmericaOrder3)
end = timeit.default_timer()
time3 = end-start
print(".")
start = timeit.default_timer()
AmericaColored4, backtracks4 = ColorDepthFirstH(AmericaAdjacentStates, AmericaOrder4)
end = timeit.default_timer()
time4 = end-start
print(".")
print()
print("Order 1 DFS w/ Heuristic:")
print("Took "+str(time1)+" seconds and "+str(backtracks1)+" backtracks to find this solution:")
print(AmericaColored1)
print()
print("Order 2 DFS w/ Heuristic:")
print("Took "+str(time2)+" seconds and "+str(backtracks2)+" backtracks to find this solution:")
print(AmericaColored2)
print()
print("Order 3 DFS w/ Heuristic:")
print("Took "+str(time3)+" seconds and "+str(backtracks3)+" backtracks to find this solution:")
print(AmericaColored3)
print()
print("Order 4 DFS w/ Heuristic:")
print("Took "+str(time4)+" seconds and "+str(backtracks4)+" backtracks to find this solution:")
print(AmericaColored4)
print()
avAmDFSHback = (backtracks1+backtracks2+backtracks3+backtracks4)/4
avAmDFSHtime = (time1+time2+time3+time4)/4

start = timeit.default_timer()
AmericaColored1, backtracks1 = ColorDepthFirstForwardH(AmericaAdjacentStates, AmericaOrder1)
end = timeit.default_timer()
time1 = end-start
print(".")
start = timeit.default_timer()
AmericaColored2, backtracks2 = ColorDepthFirstForwardH(AmericaAdjacentStates, AmericaOrder2)
end = timeit.default_timer()
time2 = end-start
print(".")
start = timeit.default_timer()
AmericaColored3, backtracks3 = ColorDepthFirstForwardH(AmericaAdjacentStates, AmericaOrder3)
end = timeit.default_timer()
time3 = end-start
print(".")
start = timeit.default_timer()
AmericaColored4, backtracks4 = ColorDepthFirstForwardH(AmericaAdjacentStates, AmericaOrder4)
end = timeit.default_timer()
time4 = end-start
print(".")
print()
print("Order 1 DFS w/ Forward and Heuristics:")
print("Took "+str(time1)+" seconds and "+str(backtracks1)+" backtracks to find this solution:")
print(AmericaColored1)
print()
print("Order 2 DFS w/ Forward and Heuristics:")
print("Took "+str(time2)+" seconds and "+str(backtracks2)+" backtracks to find this solution:")
print(AmericaColored2)
print()
print("Order 3 DFS w/ Forward and Heuristics:")
print("Took "+str(time3)+" seconds and "+str(backtracks3)+" backtracks to find this solution:")
print(AmericaColored3)
print()
print("Order 4 DFS w/ Forward and Heuristics:")
print("Took "+str(time4)+" seconds and "+str(backtracks4)+" backtracks to find this solution:")
print(AmericaColored4)
print()
avAmDFSFHback = (backtracks1+backtracks2+backtracks3+backtracks4)/4
avAmDFSFHtime = (time1+time2+time3+time4)/4

start = timeit.default_timer()
AmericaColored1, backtracks1 = ColorDepthFirstForwardSingletonH(AmericaAdjacentStates, AmericaOrder1)
end = timeit.default_timer()
time1 = end-start
print(".")
start = timeit.default_timer()
AmericaColored2, backtracks2 = ColorDepthFirstForwardSingletonH(AmericaAdjacentStates, AmericaOrder2)
end = timeit.default_timer()
time2 = end-start
print(".")
start = timeit.default_timer()
AmericaColored3, backtracks3 = ColorDepthFirstForwardSingletonH(AmericaAdjacentStates, AmericaOrder3)
end = timeit.default_timer()
time3 = end-start
print(".")
start = timeit.default_timer()
AmericaColored4, backtracks4 = ColorDepthFirstForwardSingletonH(AmericaAdjacentStates, AmericaOrder4)
end = timeit.default_timer()
time4 = end-start
print(".")
print()
print("Order 1 DFS w/ Forward and Singleton and Heuristics:")
print("Took "+str(time1)+" seconds and "+str(backtracks1)+" backtracks to find this solution:")
print(AmericaColored1)
print()
print("Order 2 DFS w/ Forward and Singleton and Heuristics:")
print("Took "+str(time2)+" seconds and "+str(backtracks2)+" backtracks to find this solution:")
print(AmericaColored2)
print()
print("Order 3 DFS w/ Forward and Singleton and Heuristics:")
print("Took "+str(time3)+" seconds and "+str(backtracks3)+" backtracks to find this solution:")
print(AmericaColored3)
print()
print("Order 4 DFS w/ Forward and Singleton and Heuristics:")
print("Took "+str(time4)+" seconds and "+str(backtracks4)+" backtracks to find this solution:")
print(AmericaColored4)
print()
avAmDFSFSHback = (backtracks1+backtracks2+backtracks3+backtracks4)/4
avAmDFSFSHtime = (time1+time2+time3+time4)/4

print()
print("Final Results: ")
print("----------------------------")
print("DFS:")
print("\tAustralia:")
print("\t\tAverage Backtracks: "+str(avAusDFSback))
print("\t\tAverage Time: "+str(avAusDFStime)+" seconds")
print("\tUnited States:")
print("\t\tAverage Backtracks: "+str(avAmDFSback))
print("\t\tAverage Time: "+str(avAmDFStime)+" seconds")
print()
print("DFS w/ Forward Checking:")
print("\tAustralia:")
print("\t\tAverage Backtracks: "+str(avAusDFSFback))
print("\t\tAverage Time: "+str(avAusDFSFtime)+" seconds")
print("\tUnited States:")
print("\t\tAverage Backtracks: "+str(avAmDFSFback))
print("\t\tAverage Time: "+str(avAmDFSFtime)+" seconds")
print()
print("DFS w/ Forward Checking and Singletons:")
print("\tAustralia:")
print("\t\tAverage Backtracks: "+str(avAusDFSFSback))
print("\t\tAverage Time: "+str(avAusDFSFStime)+" seconds")
print("\tUnited States:")
print("\t\tAverage Backtracks: "+str(avAmDFSFSback))
print("\t\tAverage Time: "+str(avAmDFSFStime)+" seconds")
print()
print("DFS w/ Heuristics :")
print("\tAustralia:")
print("\t\tAverage Backtracks: "+str(avAusDFSHback))
print("\t\tAverage Time: "+str(avAusDFSHtime)+" seconds")
print("\tUnited States:")
print("\t\tAverage Backtracks: "+str(avAmDFSHback))
print("\t\tAverage Time: "+str(avAmDFSHtime)+" seconds")
print()
print("DFS w/ Forward Checking and Heuristics:")
print("\tAustralia:")
print("\t\tAverage Backtracks: "+str(avAusDFSFHback))
print("\t\tAverage Time: "+str(avAusDFSFHtime)+" seconds")
print("\tUnited States:")
print("\t\tAverage Backtracks: "+str(avAmDFSFHback))
print("\t\tAverage Time: "+str(avAmDFSFHtime)+" seconds")
print()
print("DFS w/ Forward Checking and Singletons and Heuristics:")
print("\tAustralia:")
print("\t\tAverage Backtracks: "+str(avAusDFSFSHback))
print("\t\tAverage Time: "+str(avAusDFSFSHtime)+" seconds")
print("\tUnited States:")
print("\t\tAverage Backtracks: "+str(avAmDFSFSHback))
print("\t\tAverage Time: "+str(avAmDFSFSHtime)+" seconds")



