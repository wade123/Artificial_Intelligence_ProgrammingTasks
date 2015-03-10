#Moore Machine
from ABPruning import GTree, GNode

def genMoNode_Act(n):
    act = 0
    myTree = GTree(n)
    for i in [myTree.root.left, myTree.root.mid, myTree.root.right]:
        if i != None and myTree.root.utl == i.utl:
            act = myTree.root.n - i.n
    return act

def genMoNode(n):
    for i in xrange(1, n+1):
        print "\tN" + str(i) + "[label = \"" + str(n+1-i) + "/" + str(genMoNode_Act(n+1-i))+"\"];"
    return

def genMoEdge(n):
    for i in xrange(1,n+1):
        if n+1-i >= 4:
            print "\tN" + str(i) + " -> N" + str(i+1) + "[label = \"1\"];"
            print "\tN" + str(i) + " -> N" + str(i+2) + "[label = \"2\"];"
            print "\tN" + str(i) + " -> N" + str(i+3) + "[label = \"3\"];"
        elif n+1-i == 3:
            print "\tN" + str(i) + " -> N" + str(i+1) + "[label = \"1\"];"
            print "\tN" + str(i) + " -> N" + str(i+2) + "[label = \"2\"];"
        elif n+1-i == 2:
            print "\tN" + str(i) + " -> N" + str(i+1) + "[label = \"1\"];"
    return
            
if __name__ == "__main__":
    print "digraph MoGraph{"    
    node_n = genMoNode(21)
    edge_n = genMoEdge(21)        
    print "}"
