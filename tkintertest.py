import tkinter as tk       
import graphs
import structure
import turtle
from structure import equation

class Application(tk.Frame): #application class             
    def __init__(self, master=None):#constructor
        tk.Frame.__init__(self, master,bg="#b7d7e8") #create a frame  
        self.grid() #place it on the grid                      
        self.createWidgets()#run the create widgets function to set up the application
        self.equationslist=[]#define the lists of equations and methods
        self.methodslist=[]
        


    def createWidgets(self):#create widgets and sets up application
        self.title=tk.Label(self,text="Calculation and Comparison of Numerical Methods",bg="#b7d7e8",font=('Cambria', '16',"bold"),width=42)#title
        self.title.grid(row=1,column=1,pady=5)
        self.SetUpIntro()#this creates the changing frame, which has an introductory paragraph to explain the usage of the program to start with
        self.inputeq=tk.Button(self,text="INPUT EQUATION",command=self.CreateEquation,width=20,font=('Cambria', '10'),bg="#ccccff")#button to open page to create equation object
        self.inputeq.grid(row=2,column=0,padx=10)
        self.method=tk.Button(self,text="NEW METHOD",command=self.Method,width=20,font=('Cambria', '10'),bg="#ccccff")#button to open page to create + run methods
        self.method.grid(row=3,column=0,padx=10)
        self.comparison=tk.Button(self,text="COMPARE METHODS",command=self.Compare,width=20,font=('Cambria', '10'),bg="#ccccff")#button to open page to compare two methods
        self.comparison.grid(row=4,column=0,padx=10)
        self.info=tk.Button(self,text="SAVE/LOAD DATA",command=self.SaveorLoad,width=20,font=('Cambria', '10'),bg="#ccccff")#button to open page to save and load
        self.info.grid(row=5,column=0,padx=10)
        #all these buttons remain constant throughout the program, they do not move
 

    def SetUpIntro(self):
        self.introframe=tk.Frame(self,width=500,height=600)#creates secondary frame of defined size
        self.introframe.grid_propagate(False)#sets up how the widgets within it interact
        self.introframe.grid(column=1,row=2,rowspan=5)
        self.introcan=tk.Canvas(self.introframe,bd=1,bg="#daebe8",relief="sunken",width=500,height=600)#creates a canvas within the frame
        self.intro=self.introcan.create_text(200,20,text="This is the introduction to my program")#puts some text on it
        self.introcan.grid()

    def recreateframe(self):#clears secondary frame and sets it up again empty
        self.introframe.grid_forget()#clear
        self.introframe=tk.Frame(self,width=500,height=600)#recreate
        self.introframe.grid(column=1,row=2,rowspan=5)
        self.introframe.grid_propagate(False)#defines widget interaction
        
    def CreateEquation(self):#this is run when the 'input equation' button is pressed
        self.recreateframe()#clears secondary frame
        self.equation=tk.StringVar()
        self.inputtext=tk.Entry(self.introframe,textvariable=self.equation,bg="#ffffff")#entry widget for the equation
        self.inputtext.grid(row=1)
        tk.Label(self.introframe,text="Please enter your equation:").grid(row=0)#label for entry widget
        self.angletype=tk.StringVar()
        self.Radio1=tk.Radiobutton(self.introframe,text="Radians",variable=self.angletype,value="r")#first radio button option
        self.Radio1.grid(row=1,column=1)
        self.Radio1.select()
        self.Radio2=tk.Radiobutton(self.introframe,text="Degrees",variable=self.angletype,value="d")#second radio button option
        self.Radio2.grid(row=2,column=1)
        self.inputgo=tk.Button(self.introframe,text="GO",command=self.geteqinput)#get user input data button, runs geteqinput()
        self.inputgo.grid(row=1,column=2)
        self.eqdescription=tk.Canvas(self.introframe,bd=1,width=500,height=400)
        self.intro=self.eqdescription.create_text(200,150,text="This program accepts equations in terms of x solely \n Please use this notation: \n Addition: + \n Subtraction: - \n Division: / \n Multiplication: * \n Exponents: ^ \n \n Supported constants: \n Pi: 3.141592659, use 'p' \n E: 2.718281828, use 'e'  \n \n Supported functions: \n sin(x) cos(x) \n tan(x) ln(x) \n \n Please only use lowercase letters. ")
        self.eqdescription.grid(row=6,columnspan=3)#the text above explains which notation the program accepts, so the users can input the equation

        
        
    def geteqinput(self):
        self.eqinput=self.inputtext.get()#retrives the user input
        self.boundinp=self.angletype.get()
        self.equation=structure.equation(self.eqinput,self.boundinp)#creates the equation object with the user input
        if self.equation.getsuccess()==False:
            self.recreateframe()#clear frame
            tk.Label(self.introframe,text="Error-Equation could not be processed \n please ensure it is correct and try again.").grid(row=1)#give error message
            self.okay=tk.Button(self.introframe,text="Continue",command=self.CreateEquation)#confirm they are okay to try again
            self.okay.grid(row=2)
        else:
            self.display=tk.Label(self.introframe,text=self.equation.printequation())#displays the equation and its differential
            self.display2=tk.Label(self.introframe,text=self.equation.printdiff())
            self.display.grid(row=2)
            self.display2.grid(row=3)
            self.equationslist.append(self.equation)#adds the equation to the list of equations

    def Method(self):#runs when the create method button is selected 
        self.recreateframe()#clears the secondary frame
        self.methodchosen=tk.StringVar()
        tk.Label(self.introframe,text="Please choose your method:").grid(row=0)#label to instruct the user
        self.Method1=tk.Radiobutton(self.introframe,width=20,text="Linear Interpolation",variable=self.methodchosen,value="li",command=self.getbounds)#radio buttons for the different method types
        self.Method2=tk.Radiobutton(self.introframe,width=20,text="Interval Bisection",variable=self.methodchosen,value="ib",command=self.getbounds)#when one is selected, the user input is retrieved
        self.Method3=tk.Radiobutton(self.introframe,width=20,text="Newton-Raphson procedure",variable=self.methodchosen,value="nr",command=self.getbounds)
        self.Method1.grid(row=1,column=1)
        self.Method2.grid(row=2,column=1)
        self.Method3.grid(row=3,column=1)
 

    def getbounds(self):#when a method type is chosen this is run to get the rest of the information about the method
        self.methodchoice=self.methodchosen.get()#gets the inputted method type
        self.bound1=tk.StringVar()
        self.bound2=tk.StringVar()
        self.getbound1=tk.Entry(self.introframe,textvariable=self.bound1,bg="#ffffff")#sets up entry fields
        self.getbound2=tk.Entry(self.introframe,textvariable=self.bound2,bg="#ffffff")
        tk.Label(self.introframe,text="Please enter the bound(s)").grid(row=4)
        if self.methodchoice=="li" or self.methodchoice=="ib":#if the method is interval bisection or linear interpolation, grid both bound entry boxes
            self.getbound1.grid(row=5,column=1)
            self.getbound2.grid(row=6,column=1)
        else:#if it is newton raphson, only grid one as newton raphson only takes one bound
            self.getbound1.grid(row=5,column=1)
        tk.Label(self.introframe,text="Please enter the accuracy (dp):").grid(row=7)#label for accuracy
        self.accuracyinput=tk.Scale(self.introframe,from_=1,to=10)#a scale choice, limited to integers between one and ten ensures only valid data can be input for the accuracy
        self.accuracyinput.grid(row=8,column=1)
        tk.Label(self.introframe,text="Please choose the equation you wish to use:").grid(row=9)#label for accuracy
        self.list=tk.Listbox(self.introframe)#creates a listbox for the equations
        for i in range(len(self.equationslist)):#loops through the equation list
            self.list.insert(i,self.equationslist[i].printequation())#creates an entry in the listbox for each equation in the list
        self.list.grid(row=10,column=1)
        self.inputgo=tk.Button(self.introframe,text="GO",command=self.runmethod)#button to get user input and run method, runs runmethod function
        self.inputgo.grid(row=11,column=1)
        
    def runmethod(self):
        self.accuracy=self.accuracyinput.get()#gets user input
        self.equation=self.equationslist[self.list.index("active")]#selects the correct equation object for the corresponding entry in the listbox
        self.boundA=self.bound1.get()
        self.boundB=self.bound2.get()
        #print(self.boundA)
        self.method=structure.runningmethod(self.methodchoice,self.equation,self.boundA,self.boundB,self.accuracy)#runs method function from structure
        #print(self.boundB)
        if self.method.isroot()==True:#if it successfully found a root
            self.recreateframe()#clear frame
            self.graph= tk.Canvas(self.introframe,bg="#77a7e1",height=450,width=450)#create a canvas for the graph
            self.DrawGraph(self.method.getvalues(),0)#draw the graph using the found values
 #           self.method.savegraph(self.graph)#store the graph
            self.methodslist.append(self.method)#adds completed  method to list of methods
            self.finalprint="Final Value: "+str(self.method.getvalues()[len(self.method.getvalues())-1])#outputs the final value the program reached
            tk.Label(self.introframe,text=self.finalprint).grid(row=2)
            self.finalprint="Number of iterations: "+str(len(self.method.getvalues()))#outputs the number of iterations
            tk.Label(self.introframe,text=self.finalprint).grid(row=3)
            self.finalprint="Time taken: "+str(self.method.printtime())#outputs the time taken
            tk.Label(self.introframe,text=self.finalprint).grid(row=4)
        else:#if no root was found
            self.recreateframe()#clear frame
            tk.Label(self.introframe,text="Error-no root in interval,please try again.").grid(row=1)#give error message
            self.okay=tk.Button(self.introframe,text="Continue",command=self.Method)#confirm they are okay to try again
            self.okay.grid(row=2)
            

    def Compare(self):#run when 'compare methods' button is selected
        self.recreateframe()#clear frame
        tk.Label(self.introframe,text="Please choose the two methods you wish to compare:").grid(row=1)#label for methods listbox
        self.list=tk.Listbox(self.introframe,width=40,selectmode="multiple")#create list box
        for i in range(len(self.methodslist)):
            self.output=self.methodslist[i].getequation().printequation() + " - " + self.methodslist[i].gettype()#display the type of method and equation used to identify the method
            self.list.insert(i,self.output)
        self.list.grid(row=2)
        self.inputgo=tk.Button(self.introframe,text="GO",command=self.runcompare)#gets users select when selected(runcompare function)
        self.inputgo.grid(row=3)
 
    def runcompare(self):#gets user selection+ outputs comparison
        selected=self.list.curselection()#gets the selected methods
        if len(selected) != 2:#checks the user has selected two methods, no more no less
            self.recreateframe()#clears frame
            tk.Label(self.introframe,text="Error-incorrect number of methods selected").grid(row=1)#displays error message
            self.okay=tk.Button(self.introframe,text="Continue",command=self.Compare)
            self.okay.grid(row=2)
        else:#if correct number of methods selected
            self.recreateframe()#clear frame
            self.graph= tk.Canvas(self.introframe,bg="#77a7e1",height=400,width=450)#create canvas for graphs
            self.DrawGraph(self.methodslist[selected[0]].getvalues(),1)#draw graphs on the same canvas in two different colours
            self.DrawGraph(self.methodslist[selected[1]].getvalues(),2)
            self.text="Red: " + self.methodslist[selected[0]].getequation().printequation() + " - " + self.methodslist[selected[0]].gettype()#outputs the first method with its colour
            tk.Label(self.introframe,text=self.text).grid(row=2,column=0)
            self.finalprint="Final Value: "+str(self.methodslist[selected[0]].getvalues()[len(self.methodslist[selected[0]].getvalues())-1])#gives its results as before
            tk.Label(self.introframe,text=self.finalprint).grid(row=3)
            self.finalprint="Number of iterations: "+str(len(self.methodslist[selected[0]].getvalues()))
            tk.Label(self.introframe,text=self.finalprint).grid(row=4)
            self.finalprint="Time taken: "+str(self.methodslist[selected[0]].printtime())
            tk.Label(self.introframe,text=self.finalprint).grid(row=5)

            self.text="Blue: " + self.methodslist[selected[1]].getequation().printequation() + " - " + self.methodslist[selected[1]].gettype()#same again for the second method
            tk.Label(self.introframe,text=self.text).grid(row=7)
            self.finalprint="Final Value: "+str(self.methodslist[selected[1]].getvalues()[len(self.methodslist[selected[1]].getvalues())-1])
            tk.Label(self.introframe,text=self.finalprint).grid(row=8)
            self.finalprint="Number of iterations: "+str(len(self.methodslist[selected[1]].getvalues()))
            tk.Label(self.introframe,text=self.finalprint).grid(row=9)
            self.finalprint="Time taken: "+str(self.methodslist[selected[1]].printtime())
            tk.Label(self.introframe,text=self.finalprint).grid(row=10)
        
    def SaveorLoad(self):#allows the user to select if they would like to save data or load saved data
        self.recreateframe()#clears frame
        tk.Label(self.introframe,text="What would you like to do?").grid(row=0)#label
        self.Radio1=tk.Radiobutton(self.introframe,width=20,text="Save",command=self.save)#radio buttons that trigger their respective functions
        self.Radio2=tk.Radiobutton(self.introframe,width=20,text="Load",command=self.load)
        self.Radio3=tk.Radiobutton(self.introframe,width=20,text="Clear files",command=self.clearfiles)
        self.Radio1.grid(row=1,column=0)
        self.Radio2.grid(row=2,column=0)
        self.Radio3.grid(row=3,column=0)

    def save(self):#gets the user to select equations or methods to save from the currently loaded ones, and saves them into a file
        tk.Label(self.introframe,text="Please select the methods and/or equations you would like to save.").grid(row=3)
        self.list=tk.Listbox(self.introframe,width=40,selectmode="multiple",exportselection=0)#multiple selection listbox
        for i in range(len(self.methodslist)):
            self.output=self.methodslist[i].getequation().printequation() + " - " + self.methodslist[i].gettype()#displays all methods avaliable in a listbox
            self.list.insert(i,self.output)
        self.list.grid(row=4,column=0)
        self.list2=tk.Listbox(self.introframe,width=40,selectmode="multiple",exportselection=0)
        for i in range(len(self.equationslist)):
            self.list2.insert(i,self.equationslist[i].printequation())#displays all equations avaliable in another listbox
        self.list2.grid(row=5,column=0)
        self.inputgo=tk.Button(self.introframe,text="GO",command=self.runsave)#runs the saving of the equations and methods when selected
        self.inputgo.grid(row=6)

    def runsave(self):
        selectedmethods=self.list.curselection()#gets the selected methods and equations
        selectedequations=self.list2.curselection()
        methodfile=open("methods.txt","a")#opens the file to be written to
        for value in selectedmethods:
            record=self.methodslist[value].gettype()+"|"+self.methodslist[value].getequation().printequation()+"|"+str(self.methodslist[value].getvalues())+"|"+str(self.methodslist[value].printtime())+"|"+str(self.methodslist[value].getaccuracy())+"\n"
            methodfile.write(record)#formats the essential values needed to recreate the method object into a line of text and adds it to the file
        methodfile.close()#closes the method file
        equationfile=open("equations.txt","a")#opens the equation file to be written to 
        for value in selectedequations:
            record=self.equationslist[value].printequation()+"|"+self.equationslist[value].printboundtype()+"\n"#formats the equation information
            equationfile.write(record)#adds it to the file
        equationfile.close()
        tk.Label(self.introframe,text="Your equations and/or methods have now been saved").grid(row=7)#confirms saving
            

    def load(self):#function to get the equations and methods to load into current use
        self.tempmethodlist=[]
        methodfile=open("methods.txt","r")#open methods file for reading
        self.list=tk.Listbox(self.introframe,width=40,selectmode="multiple",exportselection=0)#create listbox to display the options
        i=0
        for line in methodfile:#for each line(method in the 
            iden,equation,values,time,accuracy=line.split("|")#split it into the individual components of the method
##            print(iden,equation,values,time,accuracy)
            values=eval(values)
##            print(values[len(values)-1])
            tempmethod=structure.resetup(iden,equation,values,time,accuracy)#temporarily recreate the method
            self.tempmethodlist.append(tempmethod)#add to temp list
            ##create method with split data then add to list.
            record=iden+"-"+equation#create display name
            self.list.insert(i,record)#put in listbox
            i+=1
        self.list.grid(row=4,column=0)
        methodfile.close()#close file
        self.tempeqlist=[]
        equationfile=open("equations.txt","r")#open equation file to be read
        self.list2=tk.Listbox(self.introframe,width=40,selectmode="multiple",exportselection=0)#create another listbox
        i=0
        for line in equationfile:#for each line(equation) in the file
            equation,boundid=line.split("|")#split it into the individual components
            tempeq=structure.equation(equation,boundid)#recreate the equation
            self.tempeqlist.append(tempeq)#add to temporary list
            self.list2.insert(i,equation)#add to listbox
            i+=1
        self.list2.grid(row=5,column=0)
        equationfile.close()#close file
        self.inputgo=tk.Button(self.introframe,text="GO",command=self.loadin)#button to get user selection and actually load in data
        self.inputgo.grid(row=6)
            
    def loadin(self):#gets selection and adds the data to current usage
        selectedmethods=self.list.curselection()#retrieve selection
        selectedequations=self.list2.curselection()
        for value in selectedmethods:#for each method selected
            self.methodslist.append(self.tempmethodlist[value])#retrieve it from the temp list and add it to the main list
        for value in selectedequations:#for each equation selected
            self.equationslist.append(self.tempeqlist[value])#retrieve it from the temp list and add it to the main list
        tk.Label(self.introframe,text="Your equations and/or methods have now been loaded").grid(row=7)#confirm loading of the data

    def clearfiles(self):
        open("equations.txt","w").close()
        open("methods.txt","w").close()
        tk.Label(self.introframe,text="Your files have now been cleared").grid(row=5)
        
    def DrawGraph(self,valuestoplot,number):#function to plot a graph, parameters are the values and a number denoting the colour to use
        turtle1 =turtle.RawTurtle(self.graph)#create a turtle object that draws on the correct canvas
        graphs.plotgraph(valuestoplot,turtle1,number)#run the plot graph function from the graphs file
        self.graph.grid(row=1)
        

app = Application()                       #create the application object
app.master.title('Calculation and Comparison of Numerical Methods') #window header   
app.mainloop()           #run the program
