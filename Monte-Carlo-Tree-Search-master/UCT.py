import numpy as np
import math
import random as rnd
import MonteCarloTreeSearch
from operator import attrgetter
  
class UCT:
    
   
    def findBestNodeWithUCT(self,node=None, root = None):
        parentVisit = node.getState().getVisitCount();
        children = node.getChildArray()
        childrenScore = []
        for child in children:
            childScore = UCT.UCTValue(parentVisit,child.getState().getWinScore(), child.getState().getVisitCount())
            childrenScore.append(childScore)
            
        result = np.where(childrenScore == np.amax(childrenScore))
        idx = rnd.randint(0,len(result[0])-1)
        
        if(children[result[0][idx]].getParent().ID != root.ID):
                print("a")
        return children[result[0][idx]]
        
    def UCTValue(totalVisit, nodeWinScore, nodeVisit):
        if (nodeVisit == 0):
            return MonteCarloTreeSearch.MonteCarloTreeSearch.Int_Max_Value
        return (nodeWinScore/nodeVisit) + math.sqrt(math.log(2*totalVisit)/nodeVisit)
