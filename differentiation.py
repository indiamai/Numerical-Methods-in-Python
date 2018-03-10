

operators=[["^",2],["**",2],["sin",2],["cos",2],["tan",2],["ln",2],["/",3,],["*",4,],["+",5,],["-",6,]]#list of possible operators, and their corresponding precedences. Multidimensional array
functions=["sin","cos","tan","ln",]#list of functions(they are also operators)

class tree():#definition of a tree structure as a class
    def __init__(self, rootval):#constructor to set up root, and set nodes to empty
        self.left=None#empty nodes
        self.right=None
        self.root=rootval#root as passed value
    def insertrightnode(self,nodeval):#inserting a right node
        if self.right ==None:#if empty
            self.right=nodeval#value is the right node
        else:
            self.right.insertrightnode(nodeval)#otherwise, the value is the right node of the tree in the right node
    def insertleftnode(self,nodeval):#same as for the right node
        if self.left ==None:
            self.left=nodeval
        else:
            self.left.insertleftnode(nodeval)
    def outputroot(self):#for testing
        print(self.root)
    def getroot(self):#returns root of tree
        return self.root
    def getleft(self):#returns left node of tree
        return self.left
    def getright(self):#returns right node of tree
        return self.right
    
        
def findoperator(operators,value):#checks if a passed value is in the operators list
    for i in range(0,len(operators)):#for each value in the operators list
        if operators[i][0]==value:#if the value is equal to the passed value
            return True#the function returns true
    return False##otherwise it is false

def findfunction(functions,value):#checks if a passed value is in the functions list
    for i in range(0,len(functions)):#for each value in the function list
        if functions[i]==value:#if the value is equal to the passed value
            return True#the function returns true
    return False#the function returns false

def compress(nremove,fromval,mylist):#function to remove values from a list
    for i in range(1,nremove+1):
        mylist.pop(fromval-i)
    return mylist

def getprecedence(operators,value):#takes finds an operator in the list and returns its corresponding precedence value
    for pair in operators:
        if pair[0]==value:#if correct value found
            return pair[1]#returns precedence

def shuntingyard(equationlist,operators,functions):#converts infix notation to rpn
    stack=[]
    queue=[]
    for i in range(len(equationlist)):#reading a token
        if (equationlist[i] in ["e","x","p"]) or equationlist[i].isnumeric(): #if token is a number or the variable
            queue.append(equationlist[i])#add to queue
        elif findfunction(functions,equationlist[i]):#else if token is in the list of functions
            stack.append(equationlist[i])#add to stack
        elif equationlist[i]=="(":#else if token is open brackets
            stack.append(equationlist[i])#add to stack
        elif equationlist[i]==")":#else if token is close brackets
            stacklen=len(stack)#get size of stack
            while stack[stacklen-1]!="(":#while the last item of the stack is not open brackets
                queue.append(stack.pop())#add the last item of the stack to the queue
                stacklen=len(stack)#get new size of stack
            stack.pop()#remove the last item of the stack
        elif findoperator(operators,equationlist[i]):#else if token is in the list of operators
            stacklen=len(stack)#get the size of the stack
            try:#try-except loop
                while findoperator(operators,stack[stacklen-1]) and (getprecedence(operators,equationlist[i])>=getprecedence(operators,stack[stacklen-1])):
                    #while the last item of the stack is an operator and has greater or equal precedence than that of the token
                    queue.append(stack.pop())#add the  last item of the stack to the queue
                    stacklen=len(stack)#get new size of the stack
            except:
                None  #if there is an error, move on
            stack.append(equationlist[i])#add the token to the stack
    while len(stack)>0:#while the stack contains values
        queue.append(stack.pop())#add the last value of the stack to the queue
    return queue#return the queue

def postfixtotree(postfix,operators,functions):# a function to convert rpn notation into a binary tree
    stack=[]
    for i in range(len(postfix)):#for each letter in the equation
        if postfix[i].isnumeric() or postfix[i] in ["e","x","p"]:#if the value is a number or a constant
            tree1 = tree(postfix[i])#create a tree with that root
            stack.append(tree1)#add tree to stack
        elif findfunction(functions,postfix[i]):#if the value is a function
            operand=stack.pop()#remove most recent tree from the stack
            tree3=tree(postfix[i])#create a tree with the function as the root
            tree3.insertrightnode(operand)#insert the removed tree as the right node
            tree3.insertleftnode(None)#insert a none type object as the left node, as functions only have one operand
            stack.append(tree3)#add new tree to the stack
        else:#otherwise the value is an operator
            operand1=stack.pop()#remove the two most recent trees from the stack
            operand2=stack.pop()
            tree2 = tree(postfix[i])#create a new tree with the operator as the root
            tree2.insertleftnode(operand1)#insert first tree as left
            tree2.insertrightnode(operand2)#and the second as right
            stack.append(tree2)#add the new tree to the stack
    return stack[0]#return the final tree, which is the first (and only) value in the stack


def postfixtoinfix(postfix,operators,functions):#function to convert postfix notation to infix
    stack=[]
    success=True
    for value in postfix:#for each value in the equation
        if not findoperator(operators,value):#if the value is not an operator(or a function as all functions are operators
            stack.append(value)#add to the stack
        elif findfunction(functions,value):#if the value is a function
            if len(stack)<1:#if there are no values in the stack
                success=False#the equation is wrong ####CHANGE THIS TO BE RETURNED TO INTERFACE
            else:#otherwise the equation works
                op1=str(stack.pop())#remove the most recent value from the stack and make it a string value
                value=str(value)#make the current value string
                equation="("+value+"("+op1+")"+")"#concatenate string, in form (function(operand)), eg (sin(x))
                stack.append(equation)#add equation to stack
        else:#otherwise the value is an operator
            if len(stack)<2:#if there are fewer than two values in the stack
                success=False#the equation is wrong
            else:#otherwise it is right
                op1=str(stack.pop())#remove two most recent values from stack and turn to string
                op2=str(stack.pop())
                value=str(value)#make value string
                equation="("+op2+value+op1+")"#concatenate string in form (operand1 operator operand2), eg (2+x)
                stack.append(equation)#add equation to stack
    return stack,success#return the final equation in the stack
        

def differentiate(tree,operators,functions):
    result=[]
    differentiated=None
    if not tree==None:#if the tree contains values
        if findoperator(operators,tree.getroot()) or findfunction(functions,tree.getroot()):#if the root is an operator or a function
            dv,v=differentiate(tree.getleft(),operators,functions)#getting the operands and their derivative
            du,u=differentiate(tree.getright(),operators,functions)
            #each rule creates a new equation list, which is the result in postfix notation
            if tree.getroot()=="+":#addition rule-simply just the two differentials added together
                result.extend(du)
                result.extend(dv)
                result.extend("+")
            elif tree.getroot()=="-":#subtraction rule-same as addition
                result.extend(du)
                result.extend(dv)
                result.extend("-")
            elif tree.getroot()=="/":#quotient rule
                result.extend(u)
                result.extend(dv)
                result.extend("*")
                result.extend(v)
                result.extend(du)
                result.extend("*")
                result.extend("-")
                result.extend(v)
                result.extend(["2"])
                result.append("^")
                result.extend("/")
            elif tree.getroot()=="*":#product rule
                result.extend(u)
                result.extend(dv)
                result.extend("*")
                result.extend(v)
                result.extend(du)
                result.extend("*")
                result.extend("+")
            elif tree.getroot()=="^" and u==["e"]:#exponentials
                result.extend(dv)
                result.extend(u)
                result.extend(v)
                result.extend("^")
                result.extend("*")
            elif tree.getroot()=="^":#chain rule
                result.extend(du)
                result.extend(v)
                result.extend("*")
                result.extend(u)
                result.extend([str(int(v[0])-1)])
                result.append("^")
                result.extend("*")
            elif tree.getroot()=="sin":#differentiation of sin
                result.extend(du)
                result.extend(u)
                result.extend("cos")
                result.extend("*")
            elif tree.getroot()=="cos":#differentiation of cos
                result.extend(["0"])
                result.extend(du)
                result.extend(u)
                result.extend("sin")
                result.extend("*")
                result.extend("-")
            elif tree.getroot()=="tan":#differentiation of tan
                result.extend(du)
                result.extend(["1"])
                result.extend(u)
                result.extend("cos")
                result.extend("/")
                result.extend(["2"])
                result.append("^")
                result.extend("*")
            elif tree.getroot()=="ln":#differentiation of natural logs
                result.extend(du)
                result.extend(u)
                result.extend("/")
            
        elif tree.getroot()=="x":#if the root of the tree is x
            result=["1"]#the derivative
        elif tree.getroot() in ["e","p"] or tree.getroot().isnumeric():#if the root of the tree is a number or constant
            result=["0"]#the derivative
        #print(result)
        differentiated= []#empty list for recording the differentiated function
        try:
            differentiated.extend(u)#if there are operands (values for u and v) they are added to the list
            differentiated.extend(v)
        except:#otherwise, nothing
            None
        differentiated.append(tree.getroot())#the root of the tree is added to the list, yielding the differentiated function in RPN
        #print(differentiated)
    return result,differentiated#the function and its derivative are returned.


    
def functionnames(operators,equationlist,infixorpost):
    for j in range(len(equationlist)-1,0,-1):#from the end of the list, look through each item in the list
        try:
            if equationlist[j]=="n" and equationlist[j-1]=="l":#if the next two values are l and n(natural log)
                equationlist[j]=equationlist[j-1]+equationlist[j]#combine them
                equationlist=compress(1,j,equationlist)#remove surplus value
            elif equationlist[j]=="n" or equationlist[j]=="s" :#if the letter is the last letter of a trigonmetric function
                equationlist[j]=equationlist[j-2]+equationlist[j-1]+equationlist[j]#combine the three
                equationlist=compress(2,j,equationlist)#remove surplus values
            if infixorpost=="infix":#if it is in infix notation(this is the first run of function names)
                if equationlist[j].isnumeric():#if a value is number
                    i=1
                    while equationlist[j-i].isdigit():#while the next value is also a number
                        equationlist[j]=equationlist[j-i]+equationlist[j]#combine them
                        equationlist=compress(1,j,equationlist)#remove the next value
                        j-=1
                        i+=1
                    
        except:
            None
    return equationlist
def operator():
    return operators

def converttopython(equation):#function to convert user inputted expression to python notation
    for j in range(len(equation)-1):#for each value in the equation
        if equation[j]=="^":#if it is a non python accepted character
            equation[j]="**"#change it for the equivalent python character
        if equation[j]=="p":
            equation[j]="pi"
        if equation[j]=="ln":
            equation[j]="log"
    return equation#return the new equation

def equationtolist(equation):#put the string into a list of individual values
    equationlist=[]
    for value in equation:#for every value
        equationlist.append(value)#add it to the list as a new value
    return equationlist#return the list

def run(equationlist):#combines all the functions to manipulate and differentiate the equation
    success=True
    equationlist=equationtolist(equationlist)#convert to list
    equationlist=functionnames(operators,equationlist,"infix")#combine multiple character items into one index in the array
    postfix=shuntingyard(equationlist,operators,functions)#convert to rpn
    finaltree = postfixtotree(postfix,operators,functions)#convert to tree
    differential,original=differentiate(finaltree,operators,functions)#differentiate, returning both the original equation and the differential in rpn
    differential=functionnames(operators,differential,"postfix")#combine multiple character items into one index in the array(for rpn version)
    differential=converttopython(differential)#convert non pythonic characters to python characters
    infix,success=postfixtoinfix(differential,operators,functions)#convert to infix
    print(infix)
    return infix[0],success#return the differentiated equation

#equation=input("Equation entered:")
#print(run(equation))
##equation=equationtolist(equation)
##equation=functionnames(operators,equation,"infix")
##equation=shuntingyard(equation,operators,functions)
##finaltree = postfixtotree(equation,operators,functions)
##differential,original=differentiate(finaltree,operators,functions)
##differential=functionnames(operators,differential,"postfix")
##print(differential)
                            
