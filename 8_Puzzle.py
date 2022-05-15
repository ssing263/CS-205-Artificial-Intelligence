from copy import deepcopy
import queue
import time

finalState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
directionList = [(-1, 0), (0, -1), (0, 1), (1, 0)]
mhnDict = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (1, 0), 5: (1, 1), 6: (1, 2), 7: (2, 0), 8: (2, 1), 0: (2, 2)}


# Below is the main driver function which takes inout from the user through command line and calls the
# general Search Function.

def main():
    # The main driver function which takes inout from the user through command line and calls the
    # general Search Function.
    print("*************************************************",
          "CS 205, Project 1: \"8-puzzle Solver\"",
          "\nBy Name: Sourav Singha, SID: 862323554",
          "*************************************************", "\n", sep="\n")

    initialPuzzleState = []

    puzzleType = int(input(
        "Select the choice for the type of puzzle \n1. Trivial \n2. Very Easy \n3. Easy \n4. Doable \n5. Oh Boy \n6. Custom Input \n\nEnter your choice: "))

    if puzzleType == 1:
        initialPuzzleState = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    elif puzzleType == 2:
        initialPuzzleState = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
    elif puzzleType == 3:
        initialPuzzleState = [[1, 2, 0], [4, 5, 3], [7, 8, 6]]
    elif puzzleType == 4:
        initialPuzzleState = [[0, 1, 2], [4, 5, 3], [7, 8, 6]]
    elif puzzleType == 5:
        initialPuzzleState = [[8, 7, 1], [6, 0, 2], [5, 4, 3]]
    elif puzzleType == 6:
        print("\nEnter the puzzle in single space separated manner, use 0 to denote space/blank")
        for i in range(3):
            initialPuzzleState.extend(
                map(lambda x: int(x), input("Enter inputs for row " + str(i + 1) + ": ").split(" ")))
    else:
        print("Invalid Input !!!")
        return ""

    searchType = int(input("Select the choice for the type of Search Algorithm \n1. Uniform Cost Search \n2. A* Misplaced Tile Heuristic \n3. A* Manhattan Distance Heuristic \n\nEnter your choice: "))

    if searchType not in [1, 2, 3]:
        print("Invalid Input !!!")
        return 0

    output = generalSearch(Problem(initialPuzzleState), searchType)
    print(output)


class Node:
    # Create a Node class for creating the Search Space Tree nodes.
    # The node class contains the current node state, gn, fn, hn values and also the pointer to its parent Node

    gn, hn, fn, parentNode = 0, 0, 0, None

    def __init__(self, board, gn, hn, fn, parent):
        self.board = board
        self.gn = gn
        self.hn = hn
        self.fn = fn
        self.parent = parent

    def getState(self):
        return self.board

    def setGn(self, gn):
        self.gn = gn

    def getGn(self):
        return self.gn

    def setHn(self, hn):
        self.hn = hn

    def getHn(self):
        return self.hn

    def setFn(self, fn):
        self.fn = fn

    def getFn(self):
        return self.fn

    def getParent(self):
        return self.parent

    def __lt__(self, otherNode):
        return self.fn < otherNode.fn


class Problem:
    # Define and stores utility function for the puzzle game such as initial state, number of nodes visited, and
    # also to expand the current node to its valid unvisited child nodes

    def __init__(self, initialState):
        global directionList
        self.initialState = initialState
        self.nodeVisitedCount = 0
        self.attemptList = {hash(str(self.initialState))}

    def initialState(self):
        # Retrives the initial state of the board game
        return self.initialState

    def getVisitedCount(self):
        # Returns the number of expanded nodes
        return self.nodeVisitedCount

    def expandNode(self, currNode):
        # Expands current node to its valid children nodes which have not been expanded to before
        self.nodeVisitedCount += 1
        currState = currNode.getState()
        newNodesList = list()
        xoC, yoC = getBlankPosition(currState)
        for xnC, ynC in directionList:
            if 0 <= xoC + xnC < 3 and 0 <= yoC + ynC < 3:
                tempNode = deepcopy(currState)
                tempNode[xoC + xnC][yoC + ynC], tempNode[xoC][yoC] = currState[xoC][yoC], currState[xoC + xnC][
                    yoC + ynC]
                hashValTemp = hash(str(tempNode))
                if hashValTemp not in self.attemptList:
                    self.attemptList.add(hashValTemp)
                    newNode = Node(tempNode, currNode.getGn() + 1, 0, 0, currNode)
                    newNodesList.append(newNode)
        return newNodesList


def getBlankPosition(currNode):
    # Return the row, column coordinate of the blank space denoted by 0 in the current node state
    for i in range(len(currNode)):
        for j in range(len(currNode[0])):
            if currNode[i][j] == 0:
                return i, j


def printPuzzle(puzzle):
    # Prints the puzzle to the terminal
    for i in range(0, 3):
        print(puzzle[i])
    print()


def solved(currNode):
    # Verifies if the current node is equal to the final state
    global finalState
    return True if currNode == finalState else False

# Manhanttan and Misplaced Tile Heuristics


getManhattanDistance = lambda currNode: sum(
    [abs(i - mhnDict.get(currNode[i][j])[0]) + abs(j - mhnDict.get(currNode[i][j])[1]) if currNode[i][j] != 0 else 0
     for i in range(3) for j in range(3)])

mptDis = lambda currNode: sum(
    [1 if mhnDict.get(currNode[i][j]) != (i, j) and currNode[i][j] != 0 else 0 for i in range(3) for j in range(3)])


def traceback(node: Node):
    # Utility function for tracing back to the initial state
    tracbackList = [node.getState()]
    tempNode = node
    while tempNode.getParent() is not None:
        tempNode = tempNode.getParent()
        tracbackList.append(tempNode.getState())
    return tracbackList


def generalSearch(problem, queueingFunction):
    # General search function  keeps on updating the queue by and pops the node from queue as per heuristics until
    # the final state is found
    # Exits if the priority queue becomes empty before reaching a solution
    
    initialNode = Node(problem.initialState, 0, 0, 0, None)
    activeQueue = queue.PriorityQueue()
    activeQueue.put(initialNode)
    print("\nExpanding state\n")
    printPuzzle(initialNode.getState())
    maxQueueSize = activeQueue.qsize()

    start = time.time()
    while True:
        if activeQueue.empty():
            end = time.time()
            print("\nTime to finish: ", end - start, " seconds", sep=" ")
            return "No Solutions Found !!!"

        maxQueueSize = max(activeQueue.qsize(), maxQueueSize)
        currentNode = activeQueue.get()
        currentNodeState = currentNode.getState()

        if solved(currentNodeState):
            print("Goal state found")
            printPuzzle(currentNodeState)
            print("Solution depth is: ", currentNode.getGn(), "\nNumber of nodes expanded: ", problem.getVisitedCount(),
                  "\nMax queue size: ", maxQueueSize)
            end = time.time()
            print("Time to finish: ", end - start, " seconds\n", sep=" ")
            print("Traceback from goal to Initial Puzzle state\n")
            for node in traceback(currentNode):
                printPuzzle(node)
            break
        else:
            print("The best state to expand with a g(n) = ", currentNode.getGn(), " and h(n) = ", currentNode.getHn(),
                  " is...")
            printPuzzle(currentNodeState)

        # Populating new nodes depending on the queueing Function
        newNodes = problem.expandNode(currentNode)
        if queueingFunction == 1:
            for node in newNodes:
                node.setHn(0)
                node.setFn(node.getGn())
                activeQueue.put(node)
        elif queueingFunction == 2:
            for node in newNodes:
                node.setHn(mptDis(node.getState()))
                node.setFn(node.getGn() + node.getHn())
                activeQueue.put(node)
        elif queueingFunction == 3:
            for node in newNodes:
                node.setHn(getManhattanDistance(node.getState()))
                node.setFn(node.getGn() + node.getHn())
                activeQueue.put(node)

    return "Terminating..."


if __name__ == '__main__':
    main()
