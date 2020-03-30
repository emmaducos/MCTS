# References
Thankful to this article https://www.baeldung.com/java-monte-carlo-tree-search which helped me greatly in implementing the code and understanding MCTS

The python package used can be found here: https://pydigger.com/pypi/python-shogi
However I've done few modifications to the original package as per my requirements. You can find the modified package in the repo.

__________________
The current implementation isnt very good and there's always room for improvement. Feel free to let me know if you have any suggestions.
__________________
# Monte-Carlo-Tree-Search
Implementation for Monte Carlo Tree Search for the game Shogi

Shogi_MC.py is the main program which runs the algorithm against the random agent. <br/>
In MonteCarloTreeSearch.py, all the four phases of the algorithm are defined. <br/>
To implement the tree structure, Tree.py and Nodee.py classes are used. <br/>
State.py is used for storing the state of the game. <br/>
UCT.py helps in calculating the UCB-1 values in the selection phase of MCTS. <br/>

