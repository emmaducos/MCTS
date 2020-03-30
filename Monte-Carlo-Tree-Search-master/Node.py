import State
import random as rnd
import numpy as np


class Node:
    ID = -1

    def __init__(self, state=None, parent=None, node=None, childArray=None):
        Node.ID += 1
        if state is not None and parent is not None and childArray is not None and node is None:
            # State,parent and childArray are given
            self.state = state
            self.parent = parent
            self.childArray = childArray
            self.ID = Node.ID
        elif state is not None and parent is None and childArray is None and node is None:
            # Only state is given
            self.state = state
            self.childArray = []
            self.ID = Node.ID
        elif state is None and parent is None and childArray is None and node is None:
            # No data given
            self.state = State.State()
            self.childArray = []
            self.ID = Node.ID
        elif state is not None and parent is None and childArray is None and node is None:
            # State is given
            self.state = state
            self.childArray = []
            self.ID = Node.ID
        elif state is None and parent is None and childArray is None and node is not None:
            ## Node is given
            self.childArray = []
            self.state = State.State(state=node.getState())
            self.ID = Node.ID
            if (hasattr(node, 'parent')):
                self.parent = node.getParent()
            childArray = node.getChildArray()
            for child in childArray:
                self.childArray.add(Node(node=child))

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def getParent(self):
        return self.parent

    def setParent(self, parent=None):
        self.parent = parent

    def getChildArray(self):
        return self.childArray

    def setChildArray(self, childArray):
        self.childArray = childArray

    def getRandomChildNode(self):
        length = len(self.childArray)
        rand = rnd.randint(0, length - 1)
        return self.childArray[rand]

    def getChildWithMaxScore(self):
        winScore = []
        visitCounts = []
        if (len(self.childArray) <= 0):
            return self

        for child in self.childArray:
            # Score is based on visitCount
            visitCount = child.getState().getVisitCount()
            score = child.getState().getWinScore()
            winScore.append(score)
            visitCounts.append(visitCount)

        try:
            result = np.where(visitCounts == np.amax(visitCounts))
            idx = rnd.randint(0, len(result[0]) - 1)
            result2 = np.where(winScore == np.amax(winScore))
            idx2 = rnd.randint(0, len(result[0]) - 1)
            if (self.childArray[result[0][idx]] == None):
                print("None")
            return self.childArray[result[0][idx]]

        except Exception as e:
            print(e)
