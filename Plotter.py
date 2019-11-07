#! /usr/bin/env python3


import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as plt3d
import numpy as np



class Plotter():

    def __init__(self,side=30):
        tolerance=10
        side=side+(side*tolerance/100)
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        # self.ax.axis('equal') Deprecated
        #first attempt:
        #let's make the plot static (dimensions)
        #next step, resize with maxlen=len resultant
        self.ax.set_xlim(0,side)
        self.ax.set_ylim(0,side)
        self.ax.set_zlim(0,side)

        self.ax.view_init(azim=120)
        
    def add_line(self,vector,color=(0,0,0)):
        components=[]
        for elements in zip(vector.origin,vector.absolute()):
            components.append(elements)
        line = plt3d.art3d.Line3D(components[0],components[1],components[2],color=color)
        self.ax.scatter(vector.origin[0],vector.origin[1],vector.origin[2])
        self.ax.scatter(vector.absolute()[0],vector.absolute()[1],vector.absolute()[2])
        self.ax.add_line(line)

    def show(self):
        plt.show()
    


