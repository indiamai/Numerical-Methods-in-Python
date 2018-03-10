##-----------GRAPHS-------------      
import turtle

def plotgraph(valuestoplot,turtle1,number):#function to plot graph, with the values, turtle to plot it with and the number denoting the colour to use as parameters
    colours=["black","red","blue"]#list of possible colours
    turtle1.hideturtle()#do not animate drawing the graph
    turtle1.speed(0)#draw at top speed
    turtle1.home()#start at 0,0
    size=180#display size
    setupaxis(size,turtle1)#draw axis
    turtle1.color(colours[number])#change turtle to specified colour
    xscale,yscale=getscale(size,valuestoplot)#calculate required values for axis scale
    labelaxis(size,xscale,yscale,turtle1)#draw on axis scale
    plotpoints(valuestoplot,xscale,yscale,turtle1)#plot the points onto the axis
    turtle1.penup()#stop drawing

def setupaxis(size,turtle1):#function to draw axes
    turtle1.color("black")#ensure colour is black
    turtle1.pendown()#start drawing
    turtle1.forward(size)#positive x axis
    turtle1.backward(2*size)#negative x axis
    turtle1.home()#back to centre
    turtle1.left(90)#turn
    turtle1.forward(size)#positive y axis
    turtle1.backward(2*size)#negative y axis
    turtle1.home()#return to centre
    turtle1.penup()#stop drawing
                

def getscale(size,valuestoplot):#function to calculate scale
    xscale=int(size/len(valuestoplot))#the whole number divisor of the size of the graph by the number of values
    highest=abs(valuestoplot[0])
    for i in range(0, len(valuestoplot)-1):#calculating highest value in list
        if abs(valuestoplot[i])>highest:
            highest=abs(valuestoplot[i])          
    yscale=abs(int(size/highest))#the whole number divisor of the size of the graph by the highest value
    return xscale,yscale

def labelaxis(size,xscale,yscale,turtle1):#function to label the axis
    turtle1.home()#return to centre
    xlabel=1#set spacing between labels to one
    ylabel=1
    if int(size/xscale)>15:#unless there are a lot of labels, in which case do every 15th label
        xlabel=15
    if int(size/yscale)>15:
        ylabel=15
    for i in range(0,int(size/xscale),xlabel):#from one to the number of points we need on the scale, skipping values if xlabel is not one
        turtle1.home()
        turtle1.forward(xscale*i)#move forward the number of pixels per interval
        turtle1.write(str(i))#draw the value
    for i in range(0,int(size/yscale),ylabel):#from zero to the number of scale points, skipping values if ylabel is not one
        turtle1.home()#return to centre
        turtle1.left(90)#turn
        turtle1.forward(yscale*i)#move forward the number of pixels for the scale value we're at
        turtle1.write(str(i))#draw the value

    for i in range(0,int(size/yscale),ylabel):#from 0 to the number of scale points, skipping values if y label is not one
        turtle1.home()#return to centre
        turtle1.right(90)#turn
        turtle1.forward(yscale*i)#move forward the number of pixels for the current scale value
        turtle1.write(str(-i))#draw the (negative) value
    turtle1.home()#return to centre
    turtle1.right(180)#turn
    for i in range(0,int(size/xscale),xlabel):#from 1 to the number of points on the scale, skipping values if xlabel is not one
        turtle1.home()
        turtle1.left(180)
        turtle1.forward(xscale*i)#move forward the number of pixels per interval
        turtle1.write(str(-i))#draw the (negative) value



def plotpoints(valuestoplot,xscale,yscale,turtle1):# plot the values on the axis
    for i in range(1,len(valuestoplot)+1):#for the number of points to plot
        turtle1.home()#return to centre
        turtle1.forward(xscale*i)#move forward to the iteration number we're at
        turtle1.left(90)#turn
        turtle1.forward(yscale*valuestoplot[i-1])#move up the required height
        turtle1.dot()#drawdot


