import rhinoscriptsyntax as rs
import random

origin = (0, 0, 0)
edge = (200, 200, 200)
socketHeight = 5
baseRadius = 37.5
height = 100
numberOfFins = 32 # has to be greater than 2 or crash, higher = slower generation time but will complete.
widthScale = baseRadius * 0.5 # value is distance that fins stick out from base

curvesToLoft = [] #array that will hold the curves that will be loft to create the walls of the vase
midCurveList = [] #ay ay ay if i delete this in the createWalls function it breaks...

isLumpy = True #true adds curves between top and bottom at intervals == numberOfLumps
numberOfLumps = 8 #number of extra rings between top and bottom to create wavy effect
lumpScale = 1.5 #not 0
twist = 90 #degree of twist in degrees

isBackForth = True #do you want it to switch directions in the rotation?

#inner wall gap thickness scale, used in loft and cap function
shellThickness = 0.9


def generatePosOrNeg(n, p):# change positive and negative values here to weight in either direction
    localRandom = 1
    while True:
        localRandom = random.randint(n, p) 
        if localRandom != 0:
            localRandom = localRandom / abs(localRandom)
            return localRandom


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
    return wavyBase

def createWalls(lumpy = False, backForth = False):
    midCurveList.append(curvesToLoft[0])
    
    if lumpy == True:

        backForthDir = 1
        for i in range(0, numberOfLumps):
            localLumpScale = random.uniform(0.75, 1.25) # this variable affects the lumpiness of the object. <1 makes it narrow to top >1 makes it funnel/lampshade like.
            
            if backForth:
                backForthDir = generatePosOrNeg(-1,4)

            #raise curve below it
            midCurve = rs.CopyObject(midCurveList[i], [0, 0, (height / numberOfLumps)])
            #widen curve then rotate it
            #midCurveOffset = rs.OffsetCurve(midCurve, edge, (random.randint(1,10) * lumpScale))
            midCurveOffset = rs.ScaleObject(midCurve, origin, [localLumpScale, localLumpScale, 1])
            midCurveOffset = rs.RotateObject(midCurve, origin, (twist / numberOfLumps * backForthDir))
            #add the two curves to a list
            midCurveList.append(midCurve)
            curvesToLoft.append(midCurveOffset)

    else:
        wavyTop = rs.CopyObject(curvesToLoft[0], [0, 0, height])
        rs.RotateObject(wavyTop, origin, twist)
        midCurveList.append(wavyTop)
    return

def loftAndCap():
    # Create shell and generate solid with wall thickness based on the value of shellThickness variable -> percentage of radius of inner shell
    shell = rs.AddLoftSrf(midCurveList)
    innerShell = rs.CopyObject(shell)
    innerShell = rs.ScaleObject(innerShell, origin, [shellThickness, shellThickness, 1])
    rs.CapPlanarHoles(shell)
    shell = rs.BooleanIntersection([shell], [innerShell])
    
    # Add base with thickness of height of socketHeight
    # this generates a base with height of (Height / numberOfLumps) then cuts top off at height of socketHeight
    socketBase = rs.AddLoftSrf([midCurveList[0], midCurveList[1]])
    socketBase = rs.ScaleObject(socketBase, origin, [shellThickness * 1, shellThickness * 1, 1])
    rs.CapPlanarHoles(socketBase)
    socketBaseCutter = rs.AddCylinder([0, 0, socketHeight], [0, 0, 200], 200)
    socketBase = rs.BooleanDifference([socketBase], [socketBaseCutter], True)
    shell = rs.BooleanUnion([shell, socketBase])
    #TODO redo above code so it fucking works...
    #truncate and generate solid from what has already been generated as shell

def deleteAllCurves():
    # find all curves in doc that are not in locked layer
    curves = rs.ObjectsByType(4) #4 is type for curves
    
    #check if any found
    if curves:
        rs.DeleteObjects(curves)
    else:
        print("No curves found")

bottom = createBase()
createWalls(isLumpy, isBackForth)
loftAndCap()
deleteAllCurves()
