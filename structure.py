from math import sin,cos,tan,pi,log,e
import graphs
import differentiation
import datetime


class equation():#class for equations

    def __init__(self,inputeq,boundtype):
        try:
            self.equationinp=inputeq#sets attribute to hold the equation string
            self.equationlist=differentiation.equationtolist(self.equationinp)#converts the string into a list
            self.success1=equation.checkvalid(self.equationlist)
            self.equationtorun=differentiation.converttopython(self.equationlist)#converts the inputted string into python-runable equations
            self.equationtorun=equation.makestring(self.equationtorun)#puts it back into a string
            self.equation=compile(self.equationtorun,"x","eval")#ast object that can be evaluated
            self.diff,self.success2=differentiation.run(self.equationinp)#calculation of the derivative
            self.difflist=differentiation.equationtolist(self.diff)#converts the string into a list
            self.difflist=differentiation.converttopython(self.difflist)#converts the differential into python runable equations
            self.difftorun=equation.makestring(self.difflist)#puts it back into a string
            self.differential=compile(self.difftorun,"x","eval")#ast object that can be evaluated
            self.typeofangle=boundtype#bounds in radians or degrees(needed for evaluation)
            self.success=self.success1 and self.success2
        except:
            self.success=False
        #print(self.equationval(1))

    def checkvalid(equation):
        equation=differentiation.functionnames(differentiation.operator(),equation,"infix")
        success=True
        for item in equation:
            if item not in [" ","x","e","p","sin","cos","tan","ln","(",")","+","-","/","*","^"] and not item.isnumeric():
                success=False
        return success

    def makestring(equation):#combines all elements of the list into one string
        final=""
        for item in equation:
            final+=item
        return final
    #accessing attributes
    def printequation(self):
        return self.equationinp

    def printdiff(self):
        return self.diff

    def printboundtype(self):
        return self.typeofangle

    def getsuccess(self):
        return self.success

    def equationval(self,x):#returns value of equation at the passed value of x
        x=float(x)
        if self.typeofangle=="d":#if bound in degrees
            x=(x/180)*pi#convert to radians
        value=eval(self.equation)#evaluate the equation at that value of x
        return value#return the value

    def differentialval(self,x):#returns value of differential at the passed value of x
        x=float(x)
        if self.typeofangle=="d":#if bound in degrees
            x=(x/180)*pi#convert to radians
        value=eval(self.differential)#evaluate the differential at the passed value of x
        return value#return the value


class method():#abstract class for all methods
    def __init__(self,accuracy):
        self.accuracy=accuracy
        self.itervals=[]
        self.iternum=0
        self.identifier=""

    def gettype(self):#methods to return various attributes
        return self.identifier

    def getvalues(self):
        return self.itervals

##    def savegraph(self,graph):
##        self.graph=graph

    def printtime(self):
        return self.time

    def isroot(self):
        return self.root

    def getequation(self):
        return self.equation

    def getaccuracy(self):
        return self.accuracy

    def resetup(self,newequation,values,time):#function to set the attributes to loaded values
        self.equation=equation(newequation,"r")
        self.itervals=values
        self.time=time

    def run(self,equation,boundA,boundB):#getting the values for the passed equation using this particular method
        self.equation=equation
        start=datetime.datetime.now()
        repeat=True
        self.root=True
        f_a=equation.equationval(boundA)#get value of equation at bounds
        f_b=equation.equationval(boundB)
        if not ((equation.equationval(boundA)>0 and equation.equationval(boundB)<0) or (equation.equationval(boundA)<0 and equation.equationval(boundB)>0)):
            #check if value of equation includes both positive and negative values, confirming root in interval
            self.root=False
            repeat=False
        current=0
        while repeat:
            repeat,boundA,boundB,current=self.iteration(boundA,boundB,equation,current)#run interval
            self.itervals.append(current)#add most recent value to list
            self.iternum+=1#increase number of iterations
            if self.iternum==100:#if it is taking too long to find a root, stop iteration
                repeat=False#do not repeat
        self.finalval=round(current,self.accuracy)#gets the rounded value
        self.itervals.append(self.finalval)#adds it to the list of values
        end=datetime.datetime.now()#finds the final time
        self.time=end-start#calculates the time taken for the method to run
        print(self.itervals)
        return self.root


    def iteration(self,boundA,boundB,equation,current):#each individual iteration
        f_a=equation.equationval(boundA)#get value of equations at each bound
        f_b=equation.equationval(boundB)
        boundC=self.GetBoundC(boundA,boundB,f_a,f_b)#get the new bound (this varies by method)
        f_c=equation.equationval(boundC)#get value of equation at new bound
        repeatbounds=True
        if f_a==0:#If the value of the equation at any of the bounds is zero, do not repeat and return that value as the root.
            repeatbounds=False
            boundC=boundA
        elif f_b==0:
            repeatbounds=False
            boundC=boundB
        elif f_c==0:
            repeatbounds=False
        elif f_c>0 and f_a>0:#if both the new bound and bound A values of the equation are greater than 0
            boundA=boundC#replace bound A with the new bound
        elif f_c>0 :#if the value of the equation at the new bound is greater than 0 (as if the value at bound A isn't the value at bound b is)
            boundB=boundC#replace bound B with the new bound
        elif f_a<0 :#(now f_c>0) if the value of the equation at bound A is less than 0
            boundA=boundC#replace bound A with the new bound
        else:#only possiblity left
            boundB=boundC#replace bound B with the new bound
        if repeatbounds==True:#check if another iteration should be done
            repeatbounds=self.repeatcheck(boundC,current)
        current=boundC
        return repeatbounds,boundA,boundB,current#return all bounds and if another iteration should be done


    def repeatcheck(self,bound1,bound2):
        val1=round(bound1,self.accuracy)#round bounds to specified accuracy
        val2=round(bound2,self.accuracy)
        print(val1," ",val2)
        if val1==val2:#if they are equal, the program should stop iterating
            return False
        elif round(self.equation.equationval(val1),10)==0:
            return False
        else:#otherwise keep going
            return True




class LinearInterpolation(method):#class for Linear Interpolation inheriting from method class
    def __init__(self,accuracy):
        method.__init__(self,accuracy)#sets up class using the constructor from the method class
        self.identifier="Linear Interpolation"#sets method type identifier

    def GetBoundC(self,boundA,boundB,f_a,f_b):#method for finding new bound used in Linear Interpolation
        boundC=(abs(f_a)*boundB + abs(f_b)*boundA)/(abs(f_a)+abs(f_b))
        return boundC


class IntervalBisection(method):#class for Interval Bisection inheriting from method class
    def __init__(self,accuracy):
        method.__init__(self,accuracy)#sets up class using the constructor from the method class
        self.identifier="Interval Bisection"#sets method type identifier

    def GetBoundC(self,boundA,boundB,f_a,f_b):#method for finding new bound used in Interval bisection
        boundC=(boundA+boundB)/2
        return boundC

class NewtonRaphson(method):#class for Newton Raphson process inheriting from method class
    def __init__(self,accuracy):
        method.__init__(self,accuracy)#sets up class using the constructor from the method class
        self.identifier="Newton Raphson"#sets method type identifier
        self.root=True#since newton raphson only has one initial bound, there will always be a root, as it is not a interval


    def run(self,equation,boundA):#overriding run procedure from method class as the newton raphson requires a different approach
        self.equation=equation
        start=datetime.datetime.now()#start timer
        boundB=None#there is no bound b to start with
        repeat=True#always repeat at the start
        self.iternum=0#there has not yet been any iterations
        while repeat:#while the loop should be repeated
            repeat,current,boundA,boundB=self.iteration(boundA,boundB,equation)#run the iteration, get values from it
            self.itervals.append(current)#add current value to list of values
            self.iternum+=1#one iteration has occured
            if self.iternum==100:#if it is taking too long to find a root, stop iteration
                repeat=False#do not repeat
        self.finalval=round(current,self.accuracy)#set current value rounded to specific accuracy as the final value
        self.itervals.append(self.finalval)#add the final value to the list of values
        end=datetime.datetime.now()#stop timer
        self.time=end-start#calculate time taken
        print(self.itervals)
        return self.root


    def iteration(self,boundA,boundB,equation):#run an iteration
        repeat=True#repeat to start
        if not boundB==None:#if boundb has a value
            boundA=boundB#replace bounda with boundb
        f_A=equation.equationval(boundA)#calculate the value of the equation at boundA
        df_A=equation.differentialval(boundA)#calculate the value of the differential at boundA
        if df_A==0:#if the differential is zero at bounda
            df_A=1#make it one, to avoid division by 0
        boundB=boundA-(f_A/df_A)#calculate new bound
        if not repeat==False:
            repeat=self.repeatcheck(boundA,boundB)#check if another iteration needs to be done

        return repeat,boundB,boundA,boundB#return values



def getequation(inputeq,boundtype):#create the equation object
    eq1=equation(inputeq,boundtype)
    return eq1


def resetup(identifier,newequation,values,time,accuracy):#recreate method objects from loaded data
    if identifier=="Linear Interpolation":#if the data is of type linear interpolation
        method=LinearInterpolation(accuracy)#create li method object
    elif identifier=="Interval Bisection":#the the data is of type interval bisection
        method=IntervalBisection(accuracy)#create ib method object
    else:#otherwise the data is of type newton raphson
        method=NewtonRaphson(accuracy)#create nr method object
    method.resetup(newequation,values,time)#set attributes of created method to the loaded values
    return method#return the method


def runningmethod(typemethod,equation,boundA,boundB,accuracy):#run the method
    boundA=float(boundA)#convert the bound to float data type
    if not typemethod=="nr":#if the type of method is not newton raphson
        boundB=float(boundB)#convert the second bound to float data type
    if typemethod=="li":#if the method is linear interpolation
        method1=LinearInterpolation(accuracy)#create li method
        method1.run(equation,boundA,boundB)#run the method's run procedure
    elif typemethod=="ib":#if the method is interval bisection
        method1=IntervalBisection(accuracy)#create ib method
        method1.run(equation,boundA,boundB)#run the methods run procedure
    else:#otherwise the method will be newton raphson
        method1=NewtonRaphson(accuracy)#create the nr method
        method1.run(equation,boundA)#run the methods run procedure
    return method1#return the method object


