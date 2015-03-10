#definition of node in the game tree
class GNode:
    def __init__(self, n = None, left = None, mid = None, right = None, utl = None):
        self.n = n
        self.left = left
        self.mid = mid
        self.right = right
        self.utl = utl
        self.order = 0
#------------------------------------------------------------------------------------
#generate the game tree
class GTree:
    def __init__(self,n):
        if n < 1:
            self.root = None
        elif n == 1:
            self.root = GNode(1)
        else:
            self.gen(n)
        self.ABPrun(self.root, 1)      
    
    def gen(self, n):       
        if n == 1:
            self.root = GNode(1)
        elif n == 2:
            leftchild = GNode(1)
            midchild = rightchild = None
            self.root = GNode(2, leftchild, midchild, rightchild, 0)            
        elif n == 3:
            leftchild = GTree(2).root
            midchild = GNode(1)
            rightchild = None
            self.root = GNode(3, leftchild, midchild, rightchild, 0)            
        else:
            leftchild = GTree(n-1).root
            midchild = GTree(n-2).root
            rightchild = GTree(n-3).root
            self.root = GNode(n, leftchild, midchild, rightchild, 0)
#--------------------------------------------------------------------------
#alpha-beta Pruning algorithm is used to calculate the utilities
    def ABPrun(self, GNode, player):
        if player == 1:
            player_next = 0
        if player == 0:
            player_next = 1

        if GNode is None:
            if player == 1:
                return 1
            else:
                return -1
        elif GNode.n == 1:
            if player == 1:
                GNode.utl = -1
            else:
                GNode.utl = 1
        else:
            if player == 1:
                if GNode.left != None and self.ABPrun(GNode.left, player_next)==1:
                    GNode.mid = GNode.right = None
                    GNode.utl = 1
                elif GNode.mid != None and self.ABPrun(GNode.mid, player_next)==1:
                    GNode.right = None
                    GNode.utl = 1
                elif GNode.right != None and self.ABPrun(GNode.right, player_next)==1:
                    GNode.utl = 1
                else:
                    GNode.utl = -1
            else:
                if GNode.left != None and self.ABPrun(GNode.left, player_next)==-1:
                    GNode.mid = GNode.right = None
                    GNode.utl = -1
                elif GNode.mid != None and self.ABPrun(GNode.mid, player_next)==-1:
                    GNode.right = None
                    GNode.utl = -1
                elif GNode.right != None and self.ABPrun(GNode.right, player_next)==-1:
                    GNode.utl = -1
                else:
                    GNode.utl = 1
        return GNode.utl
#------------------------------------------------------------------------------------
#generate dot file used in GraphViz to visualize the game tree
def genNode(GNode):
    if GNode is None:
        return
    genNode.order += 1
    GNode.order = genNode.order        
    print "\tN" + str(genNode.order) + "[label = \"" + str(GNode.n) + ":utl=" + str(GNode.utl) + "\"];"
    genNode(GNode.left)
    genNode(GNode.mid)
    genNode(GNode.right)
def genEdge(GNode):
    if GNode is None:
        return
    if GNode.left != None:
        print "\tN" + str(GNode.order) + " -> N" + str(GNode.left.order) + "[label = \"act:1\"];"
    if GNode.mid != None:
        print "\tN" + str(GNode.order) + " -> N" + str(GNode.mid.order) + "[label = \"act:2\"];"
    if GNode.right != None:
        print "\tN" + str(GNode.order) + " -> N" + str(GNode.right.order) + "[label = \"act:3\"];"
    genEdge(GNode.left)
    genEdge(GNode.mid)
    genEdge(GNode.right)
def genDotFile(GNode):   
    print "digraph GameTree{"    
    genNode(GNode)
    genEdge(GNode)        
    print "}"
#-----------------------------------------------------------------------------
#run the above codes
if __name__ == "__main__":
    genNode.order = 0
    GameTree = GTree(15)
    genDotFile(GameTree.root)
    print GameTree.root
