#written by Efe Arın 02.2017

print("written by Efe Arın 02.2017")
print("")
print("this mini program solves 9-puzzle problems using breadth-first, depth-first or a* search with manhattan priority heruistic function")
print("")
print("program throws result.txt file so make sure that you have write permition in working directory if not copying the program to another folder then running may help")
print("")
print("if you want to reach goal state other than 0,1,2,3,4,5,6,7,8 open code and change finalBoard")
print("")
#
resultFile = open("result.txt", "w")
#
print("type method ex: ast (bfs and dfs are not recomended choices)")
method = input()
resultFile.write("method choosen: "+method+"\n")
#
print("type board (ex: 5,1,0,7,8,4,2,3,6)")
board = input()
resultFile.write("board entered: "+board+"\n")
#
finalBoard=[0,1,2,3,4,5,6,7,8]
resultFile.write("goal board is: "+str(finalBoard).strip("[]")+"\n")
#
def checkInputNumbers():
    for x in range(0,9):
        try:
            board.index(x)
        except:
            return False
    return True
#
def chckInput ():
    if type(board[0])!=int:
        return False
    if len(board) != 9:
        return False
    elif not checkInputNumbers(): 
        return False
    elif method != 'bfs' and method !='dfs' and method !='ast' :
        return False
    return True
#
def splitter ():
    global board
    board = board.split(",")
    try:
        board = list(map(int, board))
    except:
        pass
#
def goalTest(state):
    for x in range (0,9):
        if state[x]!=finalBoard[x]:
            return False
    return True
#
def findActionsToChildren(state):
    position = state.index(0)
    if position==0:
        return[2,4]
    elif position==1:
        return[2,3,4]
    elif position==2:
        return[2,3]
    elif position==3:
        return[1,2,4]
    elif position==4:
        return[1,2,3,4]
    elif position==5:
        return[1,2,3]
    elif position==6:
        return[1,4]
    elif position==7:
        return[1,3,4]
    else:
        return[1,3]
#
def getChildrenStates(initialState,actions):
    childrenStates=[]
    zeroPlace=initialState[0].index(0)
    for x in actions:
        first=list(initialState[0])
        second=list(initialState[1])
        state=[first,second]
        if x==1:
            state[0][zeroPlace] = state[0][zeroPlace-3]
            state[0][zeroPlace-3] = 0
            state[1][0]=state[1][0]+1
            state[1][1]=1
            childrenStates.append(state)
        elif x==2:
            state[0][zeroPlace] = state[0][zeroPlace+3]
            state[0][zeroPlace+3] = 0
            state[1][0]=state[1][0]+1
            state[1][1]=2
            childrenStates.append(state)
        elif x==3:
            state[0][zeroPlace] = state[0][zeroPlace-1]
            state[0][zeroPlace-1] = 0
            state[1][0]=state[1][0]+1
            state[1][1]=3
            childrenStates.append(state)
        else:
            state[0][zeroPlace] = state[0][zeroPlace+1]
            state[0][zeroPlace+1] = 0
            state[1][0]=state[1][0]+1
            state[1][1]=4
            childrenStates.append(state) 
    return childrenStates
#
def checkAlreadyIn(state,visitedStates,queue):
    for y in visitedStates:
        if state[0]==y[0]:
            return True
    for y in queue:
        if state[0]==y[0]:
            return True
    return False
#
def addChildrenToQueue(children,queue,visitedStates):
    for x in children:
        if not checkAlreadyIn(x,visitedStates,queue):
            queue.append(x)
#
def getReverseActionState(state):
    action = state[1][1]
    zeroPlace=state[0].index(0)
    if action==1:
        state[0][zeroPlace] = state[0][zeroPlace+3]
        state[0][zeroPlace+3] = 0
        return state[0]
    elif action==2:
        state[0][zeroPlace] = state[0][zeroPlace-3]
        state[0][zeroPlace-3] = 0
        return state[0]
    elif action==3:
        state[0][zeroPlace] = state[0][zeroPlace+1]
        state[0][zeroPlace+1] = 0
        return state[0]
    else:
        state[0][zeroPlace] = state[0][zeroPlace-1]
        state[0][zeroPlace-1] = 0
        return state[0]
#
def findStatesInLevel(visitedStates,level):
    result=[]
    for x in visitedStates:
        if x[1][0]==level:
            result.append(x)
    return result
#
def getSolutionActions(visitedStates):
    actions=[]
    node = visitedStates[-1]
    solutionLevel = node [1][0]
    actions.insert(0,node[1][1])
    for x in range(solutionLevel-1,0,-1):
        upperLayerStates=findStatesInLevel(visitedStates,x)
        node = getReverseActionState(node)
        lenght = len(upperLayerStates)
        if not lenght==1:
            for y in range(0,lenght):
                if upperLayerStates[y][0]==node:
                    node = upperLayerStates[y]
                    break
        else:
            node=upperLayerStates[0]
        actions.insert(0,node[1][1])
    return actions
#
def writeActions(actions):
    for x in actions:
        if x==1:
            print("Up")
        elif x==2:
            print("Down")
        elif x==3:
            print("Left")
        elif x==4:
            print("Right")
#
def getThirdElement(a):
    return a[2]
#
def reorderQueue(queue):
    queue.sort(key=getThirdElement)
#
def getHeuristic(state):
    sum=0
    for x in range(1,9):
        lineDistance=abs(state.index(x)-finalBoard.index(x))
        k=lineDistance%3
        b=(lineDistance-k)//3
        sum=sum+(k+b)
    return sum
#
def addHeuristicToChildren(children):
    for x in range(0,len(children)):
        heuristic=getHeuristic(children[x][0])
        total=getHeuristic(children[x][0])+children[x][1][0]
        children[x].append([total])
#
def bfs (board):
    board = [board,[0,0]]
    queue = [board]
    visitedStates=[]
    maxSizeOfQueue=0
    maxDepthOfSearch=0
    while not goalTest(queue[0][0]):
        nowWisiting=queue[0]
        del queue[0]
        actions = findActionsToChildren(nowWisiting[0])
        children = getChildrenStates(nowWisiting,actions)
        depthOfChildren=children[0][1][0]
        if maxDepthOfSearch<depthOfChildren:
            maxDepthOfSearch=depthOfChildren
        addChildrenToQueue(children,queue,visitedStates)
        leghtOfQueue = len(queue)
        if maxSizeOfQueue< leghtOfQueue :
            maxSizeOfQueue=leghtOfQueue
        visitedStates.append(nowWisiting)
    print("number of visited nodes ",len(visitedStates))
    resultFile.write("number of visited nodes: "+str(len(visitedStates))+"\n")
    print("maximum size of queue ",maxSizeOfQueue)
    resultFile.write("maximum size of queue: "+str(maxSizeOfQueue)+"\n")
    print("maximum depth of search",maxDepthOfSearch)
    resultFile.write("maximum depth of search: "+str(maxDepthOfSearch)+"\n")
    print("depth of solution",queue[0][1][0])
    resultFile.write("depth of solution: "+str(queue[0][1][0])+"\n")
    visitedStates.append(queue[0])
    actions=getSolutionActions(visitedStates)
    print("actions to reach goal")
    resultFile.write("actions to reach goal: "+str(actions).strip("[]")+"\n")
    writeActions(actions)
    return(actions)
#
def dfs (board):
    board = [board,[0,0]]
    queue = [board]
    visitedStates=[]
    maxSizeOfQueue=0
    maxDepthOfSearch=0
    while not goalTest(queue[-1][0]):
        nowWisiting=queue[-1]
        del queue[-1]
        actions = findActionsToChildren(nowWisiting[0])
        actions.reverse()
        children = getChildrenStates(nowWisiting,actions)
        depthOfChildren=children[0][1][0]
        if maxDepthOfSearch<depthOfChildren:
            maxDepthOfSearch=depthOfChildren
        addChildrenToQueue(children,queue,visitedStates)
        leghtOfQueue = len(queue)
        if maxSizeOfQueue< leghtOfQueue :
            maxSizeOfQueue=leghtOfQueue
        visitedStates.append(nowWisiting)
    print("number of visited nodes ",len(visitedStates))
    resultFile.write("number of visited nodes: "+str(len(visitedStates))+"\n")
    print("maximum size of queue ",maxSizeOfQueue)
    resultFile.write("maximum size of queue: "+str(maxSizeOfQueue)+"\n")
    print("maximum depth of search",maxDepthOfSearch)
    resultFile.write("maximum depth of search: "+str(maxDepthOfSearch)+"\n")
    print("depth of solution",queue[-1][1][0])
    resultFile.write("depth of solution: "+str(queue[0][1][0])+"\n")
    visitedStates.append(queue[-1])
    actions=getSolutionActions(visitedStates)
    print("actions to reach goal")
    resultFile.write("actions to reach goal: "+str(actions).strip("[]")+"\n")
    writeActions(actions)
    return(actions)
#
def ast(board):
    board = [board,[0,0],[getHeuristic(board)]]
    queue = [board]
    visitedStates=[]
    maxSizeOfQueue=0
    maxDepthOfSearch=0
    while not goalTest(queue[0][0]):
        nowWisiting=queue[0]
        del queue[0]
        actions = findActionsToChildren(nowWisiting[0])
        children = getChildrenStates(nowWisiting,actions)
        addHeuristicToChildren(children)
        depthOfChildren=children[0][1][0]
        if maxDepthOfSearch<depthOfChildren:
            maxDepthOfSearch=depthOfChildren
        addChildrenToQueue(children,queue,visitedStates)
        reorderQueue(queue)
        leghtOfQueue = len(queue)
        if maxSizeOfQueue< leghtOfQueue :
            maxSizeOfQueue=leghtOfQueue
        visitedStates.append(nowWisiting)
    print("number of visited nodes ",len(visitedStates))
    resultFile.write("number of visited nodes: "+str(len(visitedStates))+"\n")
    print("maximum size of queue ",maxSizeOfQueue)
    resultFile.write("maximum size of queue: "+str(maxSizeOfQueue)+"\n")
    print("maximum depth of search",maxDepthOfSearch)
    resultFile.write("maximum depth of search: "+str(maxDepthOfSearch)+"\n")
    print("depth of solution",queue[0][1][0])
    resultFile.write("depth of solution: "+str(queue[0][1][0])+"\n")
    visitedStates.append(queue[0])
    actions=getSolutionActions(visitedStates)
    print("actions to reach goal")
    resultFile.write("actions to reach goal(1up,2down,3left,4right): "+str(actions).strip("[]")+"\n")
    writeActions(actions)
    return(actions)
#
def askForSimulation(actions):
    print("want to simulate?(press y for yes, any other keys for no)")
    simulate=input()
    if simulate=="y":
        tempBoard=[board,[0,0]]
        show(tempBoard[0])
        print("")
        for x in range(0,len(actions)-1):
            action=[actions[x]]
            writeActions(action)
            tempBoard = getChildrenStates(tempBoard,action)
            tempBoard=tempBoard[0]
            show(tempBoard[0])
            print("")
        writeActions([actions[-1]])
        show(finalBoard)
#
def show(board):
    print(board[0],board[1],board[2])
    print(board[3],board[4],board[5])
    print(board[6],board[7],board[8])
#        MAIN
splitter()
if chckInput() :
    if board==finalBoard:
        print("Puzzle is already solved")
        resultFile.write("already solved")
    elif method=="bfs":
        print("this may take a while")
        actions = bfs(board)
    elif method=="dfs":
        print("this may take a while")
        actions = dfs(board)
    elif method=="ast":
        print("this may take a while")
        actions = ast(board)
else:
    print("Err: Inputs are improper")
    resultFile.write("improper inputs")
resultFile.close()
print("result file is created in working directory named as result.txt")
askForSimulation(actions)
print("press any to close")
input()