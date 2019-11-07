#! /usr/bin/env python3
import numpy as np
import math


def none(dummy):
    return dummy



def pythagoras(elements):
    square=[pow(num,2) for num in elements]
    total=sum(square)
    return pow(total,0.5)

class Polar3D():
    #chain are carthesian based
    #the following method calculate the tip of the vector, relative to the origin
    #this method is pretty useful in the chain manager
    def absolute(self):
        coord=[]
        for couple in zip(self.carthesian(),self.origin):
            coord.append(sum(couple))
        return coord

    

    def __init__(self,origin=((0,0,0))):
        self.origin=origin
        self.previous=None

    #print vector directly now lead to full info dump
    def __str__(self):
        return "<vector> carthesian ({}),\npolar (module:{},angles:{})".format(self.carthesian(),self.module,self.polar())


    #let's make a simple object sum method (it only works with + operand...for now)
    def __add__(self,other):
        coord=[]
        for couple in zip(self.carthesian(),other.carthesian()):
            coord.append(sum(couple))
        #this add method return a vector with origin = self.origin
        vect=Polar3D(self.origin)
        vect.carthesian_input(coord)
        return vect

    #make the previous method working with builtin functions (sum, map...)
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def carthesian_input(self,coordinates=(0,0,0)):
        self.coordinates=coordinates
        self.build_polar()


    def polar_input(self,module,angles,degree=False):
        if degree:
            angles=list(map(math.radians,angles))
        self.module=module
        self.angles=angles
        self.degrees=[math.degrees(x) for x in self.angles]
        self.build_carthesian()

        
    def carthesian(self):
        return self.coordinates

    def build_carthesian(self):
        self.coordinates=[]
        base=self.module*math.sin(self.angles[1])
        print(base)
        self.coordinates.append(base*math.cos(self.angles[0]))
        self.coordinates.append(base*math.sin(self.angles[0]))
        self.coordinates.append(self.module*math.cos(self.angles[1]))

    def polar(self,verbose=0):
        if verbose:
            return self.degrees
        else:
            return self.angles
    
    def build_polar(self):
        self.module=pythagoras(self.coordinates)
        self.angles=[math.atan2(self.coordinates[1],self.coordinates[0])]
        self.angles.append((math.pi/2)-math.atan2(self.coordinates[2],pythagoras([self.coordinates[1],self.coordinates[0]])))
        self.degrees=[math.degrees(el) for el in self.angles]
    
    def length(self):
        return self.module

    def update_angles(self,angles):
        self.angles=angles
        self.degrees=[math.degrees(x) for x in self.angles]
        self.build_carthesian()

