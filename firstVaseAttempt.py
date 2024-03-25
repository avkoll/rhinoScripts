import rhinoscriptsyntax as rs
import random

origin = (0, 0, 0)
edge = (200, 200, 200)
baseRadius = 8
height = 100
numberOfFins = 40
widthScale = baseRadius * 1 # value is distance that fins stick out from base
twist = 0 #degree of twist in degrees
curvesToLoft = [] #array that will hold the curves that will be loft to create the walls of the vase
isLumpy = True #true adds curves between top and bottom at intervals == numberOfLumps
numberOfLumps = 6 #number of extra rings between top and bottom to create wavy effect



def createBase():
    base = rs.AddCircle(origin, baseRadius)
    outerCurve = rs.OffsetCurve(base, edge, widthScale)

    divideBase = rs.DivideCurve(base, numberOfFins)
    divideOuterCurve = rs.DivideCurve(outerCurve, numberOfFins)
    pointsArray = []
    
    rs.DeleteObjects([base, outerCurve])
    
    for i in range(0, len(divideBase)):
        b = rs.AddPoint(divideBase[i])
        oc = rs.AddPoint(divideOuterCurve[i])
        pointsArray.append(b)
        pointsArray.append(oc)

    pointsArray.append(pointsArray[0])

    wavyBase = rs.AddCurve(pointsArray)
    rs.DeleteObjects(pointsArray)
    curvesToLoft.append(wavyBase) #add curves between top and bottom below this one and before the top is added i.e. if there ends up being a twist

def createTop(lumpy = False):
    if lumpy == True:
        for i in range(0, numberOfLumps):
            midCurves = rs.CopyObject(curvesToLoft[i], [0, 0, (height / numberOfLumps)])
            curvesToLoft.append(midCurves)
    else:
        wavyTop = rs.CopyObject(curvesToLoft[0], [0, 0, height])
        rs.RotateObject(wavyTop, origin, twist)
        curvesToLoft.append(wavyTop)
    return

def loftAndCap():
    shell = rs.AddLoftSrf(curvesToLoft)
    rs.CapPlanarHoles(shell)

createBase()
createTop(isLumpy)
loftAndCap()
