from StereoPolar import Polar3D
from StereoPolar import pythagoras as pt
from Plotter import Plotter
from errors import *
import tinyik

class Chain():
     
    
    def __init__(self):
        self.elements=[None]
        self.assignement={'x':0,'y':1,'z':2}
        self.hasRevolute=False

    def __str__(self):
        message="<Chain object> container\nVector"
        message=message+"{}\n"*(len(self.elements[1:]))
        #create a vector that we unpack 
        message=message.format(*[vect.__str__() for vect in self.elements[1:]])
        return message
    #warning:
    #warning:
    #the first vector is a None type (base)
    #keep in mind that the self.elements array does not 
    #ignore the base vector (dummy)
    #I'm lazy

    #this function add a new vector(or list of vector)
    #the chain is created in the same order of inserting 
    #next step (implement a branched system)
    def newVect(self,vector_list):
        for index in range(len(vector_list)):
            vector_list[index].previous=self.elements[len(self.elements)-1]
            if vector_list[index].previous is not None :
                vector_list[index].origin=vector_list[index].previous.absolute()
                vector_list[index]
            self.elements.append(vector_list[index]) 
    
    #return an oriented vector that connect the first origin to the last tip
    def resultant(self):
        return sum(self.elements[1:])

#this is the non-wrapped function to generate an
#actuator obj from the tiniyik class 
#an actuator is an abstract chain
    def toActuator(self):
        if(not self.hasRevolute):
            print("revolute is not setted")
            raise RevoluteError
        structure=[]
        self.toHomogeneus()
        for i in range(len(self.revolute)):
            structure.append(self.revolute[i])
            structure.append(list(self.hChain.elements[i+1].carthesian()))
            #print(structure)
        actuator=tinyik.Actuator(structure)
        return actuator

    def addRevolute(self,revolute):
        if len(revolute)!=len(self.elements)-1:
            print ("expected {} joints, {} given".format(len(self.elements)-1,len(revolute)))
            #raise RevoluteError
        #we don't need that else here...but, i will keep it
        else:
            self.hasRevolute=True
            self.revolute=revolute

        
#all this functions eventually returns the object
#but the main scope is to finally compute it
#to keep it into the class
    def createActuator(self):
        self.actuator=self.toActuator()
        return self.actuator

    #this is a so-called, non elegant solution
    #to work on a nice and clean set of vectors, i created
    #this method, that built a zeroed version of the chain
    #(alla angles at 0, to make sure to have a clear starting point)
    def toHomogeneus(self):
        if(not self.hasRevolute):
            print("revolute is not setted")
            raise RevoluteError
        newChain=Chain()
        newvect=[]
        for index,element in enumerate(self.elements[1:]):
            vect=Polar3D()
            significant=self.assignement[self.revolute[index]]
            cord=[0,0,0]
            cord[significant]=element.length()
            vect.carthesian_input(cord)
            newvect.append(vect)
        newChain.newVect(newvect)
        #the chain we will work on will be an homogeneous copy
        #of the original one (angle is 0)
        self.hChain=newChain
        self.effector=newChain
        return newChain
    
    def showHomogeneous(self,color=(0,0,0),resultant=False,resultant_color=(1,0,0)):
       self.hChain.show(color,resultant=resultant,resultant_color=resultant_color)
    
    def writeAngle(self,angles):
        if len(angles)==len(self.effector.elements[1:]):
            self.actuator.angles=angles


    def writePosition(self,position):
        if len(position)<=3 and len(position)>=2:
            self.actuator.ee=position

    def update(self):
        for i in range(len(self.effector.elements[1:])):
            #grab the significant angle
            #rem: each motor can only revolute around one axis
            buffer=[0,0]                                            
            if(self.revolute[i]=='z'):
                index=0
            elif(self.revolute[i]=='x'):
                index=1
            else:
                index=1
                buffer[0]=np.pi/2

            if(self.elements[i+1].previous is not None):
                buffer=self.elements[i+1].previous.angles
            buffer[index]+=self.actuator.angles[i]
            self.effector.elements[i+1].update_angles(buffer)
        tmp=Chain()
        tmp.newVect(self.effector.elements[1:])
        self.effector=tmp
   
    def showEffector(self,color=(0,0,0),resultant=False,resultant_color=(1,0,0)):
       self.effector.show(color,resultant=resultant,resultant_color=resultant_color)
    
    def show(self,color=(0,0,0),resultant=False,resultant_color=(1,0,0)):
        plot=Plotter(self.resultant().length())
        for el in self.elements[1:]:
            plot.add_line(el)
        plot.show()
#recall toHomogeneous,toactuator and create actuator 
#will overwrite previous recorded data

        

    