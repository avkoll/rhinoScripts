## Make base function
## this script will make a base that the shade will be able to lock into
## it will have a standard mount for the shade and can be reshaped depending 
## on bulb shape/size
## calling this will replace the other createBase function in firstVaseAttempt.py
## maybe have like 3 different diameters depending on socket type. 
## first will be for 

import rhinoscriptsyntax as rs


## creates socket with threads at standard dimensions in mm
def createSocket(center=(0,0,0)):
    threadBase = rs.AddCylinder(center, 10.0, 20.0)
    threads = rs.AddCylinder(center, (10.0 + 25.0), 17.5)
    socket = rs.BooleanUnion([threadBase, threads])
    return socket

# function to create the universal base. 
def createUBase():
    
