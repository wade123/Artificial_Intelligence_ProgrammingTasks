'''an equation simplifier using A* search algorithm'''

#!/usr/bin/python
import eqparser
import search
from copy import deepcopy
from math import *
     
def segment(Node):
    eq_string = calculate(Node)
    n = eq_string.find("=")
    eq_left = eq_string[0:n+1]
    eq_right = eq_string[n+1:]
    if eq_right[0] != '(':
        eq_right = '('+eq_right+')'
    left_pre_pos = findall(eq_right,"(")
    right_pre_pos = findall(eq_right,")")
    N = len(left_pre_pos)
    for j in range(N):
        N_left = left_pre_pos[-1]
        N_right = right_pre_pos[0]
        seg_str = eq_right[N_left:N_right+1]
        seg_str_sim = simplifier(seg_str)  #simplifying here
        eq_right = eq_right.replace(seg_str,seg_str_sim)   
        left_pre_pos = findall(eq_right,"(")
        right_pre_pos = findall(eq_right,")")
        #M = len(eq_right)
        #if left_pre_pos == [0] and right_pre_pos==[M-1]: break
    return eq_left+eq_right

def findall(s,c):
        result = []
        p = s.find(c,0)
        while p!= -1:
                result.append(p)
                p=s.find(c,p+1)
        return result

symbols = ["=","1","2","3","4","5","6","7","8","9","0","^",".","+","-","*","/","(",")"]
Nums = ["1","2","3","4","5","6","7","8","9","0"]
operations_lev1 = ["+","-"]
operations_lev2 = ["*","/","^"]

def simplifier(s):
    s=s[1:-1]
    if not contain_var(s):
        ex = s.replace("^","**")
        val = str(eval(ex))
        return val
    else:
        for i in find_var(s):
            if i==0:
                [x,j] = right_combine(i,s)
                if j==len(s):
                        s=s[j:]
                        s = s+x
            else:
                [x1,j1] = right_combine(i,s)
                [x2,j2] = left_combine(i,s)
                x=s[j2:j1]
                if j1==len(s): continue
                elif j2==0:
                    s = s[j1:]
                    s = s+x
                else:
                    s=s[0:j2]+s[j1:]
                    s = s+x
    N_var = find_var(s)
    if N_var[0] == 0: return s
    else:
        [x,j] = left_combine(N_var[0],s)
        val = s[0:j]
        val=val.replace("^","**")
        val = str(eval(val))
        s = val+s[j:]
    return s

def left_combine(i,s):
    x=s[i]
    for j in range(i-1,0,-1):
        if s[j] in operations_lev2+Nums:
            x=s[j]+x
        else:
            x=s[j]+x
            return [x,j]
    return [x,j]

def right_combine(i,s):
    x=""
    for j in range(i,len(s),1):
        if s[j] in operations_lev2+Nums:
            x=x+s[j]
        else:
            return [x,j+1]
    return [x,j+1]            

def find_var(s):
    results = []
    for i in range(len(s)):
            if s[i] not in symbols:
                  results.append(i)
    return results

def contain_var(s):
    N=0
    N_s = len(s)
    for c in s:
        if c in symbols:
            N=N+1
    if N==N_s: return False
    else: return True
        
    
def calculate(Node):	
    if type(Node.children) != list: 
        if type(Node.children) == None: return str(Node.leaf)
        else:
	    if Node.type == "UNARYOP" or Node.type == "UNARYFUNCTION":
                    return str(Node.leaf)+"("+calculate(Node.children)+")"
            return str(Node.leaf)+calculate(Node.children)
    if len(Node.children) == 0 or Node.children == None: return str(Node.leaf)
    if len(Node.children) == 1:
        if Node.type == "UNARYOP" or Node.type == "UNARYFUNCTION":
            return str(Node.leaf)+"("+calculate(Node.children)+")"
            if len(Node.children.children) != 0: 
                return str(Node.leaf)+"("+calculate(Node.children)+")"
            return str(Node.leaf)+calculate(Node.children)
    if len(Node.children) == 2:
        if len(Node.children[0].children)!= 0 and len(Node.children[1].children) !=0: 
            return "("+calculate(Node.children[0])+")"+str(Node.leaf)+"("+calculate(Node.children[1])+")"
        if len(Node.children[0].children) != 0:
            return "("+calculate(Node.children[0])+")"+str(Node.leaf)+calculate(Node.children[1])
        if len(Node.children[1].children) != 0:
            return calculate(Node.children[0])+str(Node.leaf)+"("+calculate(Node.children[1])+")"
        return calculate(Node.children[0])+str(Node.leaf)+calculate(Node.children[1])

def HFunction(p, goal, r):
	if(p.type == 'VARIABLENAME' and p.leaf == goal):
		return r 
	elif(p.type == 'BINARYOP' or p.type == 'EQUALS'):
		l = HFunction(p.children[0], goal, r + 1) 
		r = HFunction(p.children[1], goal, r + 1) 
		if(l != -1 and r != -1):
			return min(l, r)
		elif(l == -1 and r != -1):
			return r
		elif(l != -1 and r == -1):
			return l 
		else:
			return -1 ;
	elif(p.type == 'UNARYFUNCTION' or p.type == 'UNARYOP'):
		return HFunction(p.children, goal, r+1) 
	else:
		return -1

def outPut(self):
    if self.error == 0: 
	    print "x = undefined"
            return
    print self.calculate(self.result)


class Problem(object):
    def __init__(self, initial, goal=None):
        self.initial = initial
	self.goal = goal

    def actions(self, state):
	actions = []
        actions.append("AC1") 
    	if(state.children[0].leaf == '-'):
		if (state.children[0].type == 'BINARYOP'):
    			actions.append("AC2")
		elif (state.children[0].type == 'UNARYOP'):
			actions.append("AC3")
	elif(state.children[0].leaf == '+'):
		actions.append("AC4")
		actions.append("AC5")
	elif(state.children[0].leaf == '/'):
		actions.append("AC6")
	elif(state.children[0].leaf == '*'):
		actions.append("AC7")
		actions.append("AC8")
	elif(state.children[0].leaf == '^' and state.children[0].children[1].leaf == 2):
		actions.append("AC9")
	if(state.children[0].leaf == 'ln'):
		actions.append("AC10")
	if(state.children[0].leaf == 'sqrt'):
		actions.append("AC11")
	return actions
		

    def result(self, state, action):
	if action == "AC1":
		leftchild = deepcopy(state.children[1])
		rightchild = deepcopy(state.children[0])
		New_state = eqparser.Node('EQUALS', [leftchild, rightchild], '=')
        if action == "AC2":
                leftchild = deepcopy(state.children[0].children[0])
                rightchild = eqparser.Node('BINARYOP', [deepcopy(state.children[1]), deepcopy(state.children[0].children[1] )], '+')
		New_state = eqparser.Node('EQUALS', [leftchild, rightchild], '=')
	if action == "AC3":
                leftchild = deepcopy(state.children[0].children)
                rightchild = eqparser.Node('UNARYOP', deepcopy(state.children[1]) ,'-')
		New_state = eqparser.Node('EQUALS', [leftchild, rightchild], '=')
	if action == "AC4":
                leftchild = deepcopy(state.children[0].children[0])
                rightchild = eqparser.Node('BINARYOP', [deepcopy(state.children[1]), deepcopy(state.children[0].children[1] )], '-')
        	New_state = eqparser.Node('EQUALS', [leftchild, rightchild], '=')
	if action == "AC5":
                leftchild = deepcopy(state.children[0].children[1])
                rightchild = eqparser.Node('BINARYOP', [deepcopy(state.children[1]), deepcopy(state.children[0].children[0] )], '-')
		New_state = eqparser.Node('EQUALS', [leftchild, rightchild], '=')
	if action == "AC6":
                leftchild = deepcopy(state.children[0].children[0])
                rightchild = eqparser.Node('BINARYOP', [deepcopy(state.children[1]), deepcopy(state.children[0].children[1] )], '*')
		New_state = eqparser.Node('EQUALS', [leftchild, rightchild], '=')
	if action == "AC7":
                leftchild = deepcopy(state.children[0].children[0])
                rightchild = eqparser.Node('BINARYOP', [deepcopy(state.children[1]), deepcopy(state.children[0].children[1] )], '/')
		New_state = eqparser.Node('EQUALS', [leftchild, rightchild], '=')
	if action == "AC8":
                leftchild = deepcopy(state.children[0].children[1])
                rightchild = eqparser.Node('BINARYOP', [deepcopy(state.children[1]), deepcopy(state.children[0].children[0] )], '/')
		New_state = eqparser.Node('EQUALS', [leftchild, rightchild], '=')
	if action == "AC9":
                leftchild = deepcopy(state.children[0].children[0])
                rightchild = eqparser.Node('UNARYFUNCTION' , deepcopy(state.children[1]),'sqrt')
		New_state = eqparser.Node('EQUALS', [leftchild, rightchild], '=')	
	if action == "AC10":
                leftchild = deepcopy(state.children[0])
                rightchild = eqparser.Node('BINARYOP', [eqparser.Node('SYMBOL', [], 'e'), deepcopy(state.children[1])], '^')
		New_state = eqparser.Node('EQUALS', [leftchild, rightchild], '=')
	if action == "AC11":
                leftchild = deepcopy(state.children[0].children)
                rightchild = eqparser.Node('BINARYOP', [deepcopy(state.children[1]),eqparser.Node('INT',[], 2)],'^')
		New_state = eqparser.Node('EQUALS', [leftchild, rightchild], '=')
	return New_state
	

    def goal_test(self, state):
        if(state.type == 'EQUALS' and state.children[0].leaf == self.goal):
		return True
	else:
		return False

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        return 0


while 1:
    try:
        s = raw_input('eq > ')   # use input() on Python 3
	var = raw_input('var > ')
    except EOFError:
        print
        break
    p = eqparser.parse(s)
    problem =Problem(p,var)
    result = search.astar_search(problem, lambda n: HFunction(n.state, var, -1) ).state 
    s = segment(result)
    print s
    #print "In infix form: " + str(p)
        

