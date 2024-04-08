import rhinoscriptsyntax as rs
import random
#import universalBase

origin = (0, 0, 0)
edge = (200, 200, 200)
socketHeight = 0.75 # *IMPORTANT* socketHeight needs to be < BottomThickness in the slicer or printer will make spagheto
baseRadius = 45 #lamp hole is 35mm wide
height = 125
numberOfFins = 20 # has to be greater than 2 or 12 if baseInterpolated, higher = slower generation time but will complete.
widthScale = baseRadius * 0.1 # value is distance that fins stick out from base
baseInterpolated = False # decide if the curve at base should be control point or interpolated
isLargeBase = False # offset base so bottom is wider than original curve

curvesToLoft = [] #array that will hold the curves that will be loft to create the walls of the vase
midCurveList = [] #ay ay ay if i delete this in the createWalls function it breaks...

isLumpy = True #true adds curves between top and bottom at intervals == numberOfLumps
numberOfLumps = 22 #number of extra rings between top and bottom to create wavy effect
lumpScale = 0.10 #not 0
twist = 90 #degree of twist in degrees

isBackForth = True #do you want it to switch directions in the rotation?

#inner wall gap thickness scale, used in loft and cap function
shellThickness = 0.75

# change positive and negative values here to weight in either direction
def generatePosOrNeg(n, p):
    localRandom = 1
    while True:
        localRandom = random.randint(n, p) 
        if localRandom != 0:
            localRandom = localRandom / abs(localRandom)
            return localRandom

def createBase(interp=False):
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
    
    if interp:
        wavyBase = rs.AddInterpCurve(pointsArray)
    else:
        wavyBase = rs.AddCurve(pointsArray)
        
    rs.DeleteObjects(pointsArray)
    curvesToLoft.append(wavyBase) #add curves between top and bottom below this one and before the top is added i.e. if there ends up being a twist
    return wavyBase

def createWalls(lumpy = False, backForth = False, largeBase = False):
    midCurveList.append(curvesToLoft[0])
    

    
    if lumpy == True:

        backForthDir = 1
        for i in range(0, numberOfLumps):
            localLumpScale = random.uniform(1.00, 1.07) # this variable affects the lumpiness of the object. <1 makes it narrow to top >1 makes it funnel/lampshade like.
            
            if backForth:
                backForthDir = generatePosOrNeg(-1,2)

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
    
    ## offset and replace bottom
    #TODO standardize base size with this if statement
    if largeBase == True:
        standardBase = rs.AddCircle([0, 0, 0], baseRadius * 1.10)
        midCurveList[0] = standardBase
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
    socketBase = rs.ScaleObject(socketBase, origin, [shellThickness * 1.01, shellThickness * 1.01, 1])
    rs.CapPlanarHoles(socketBase)
    socketBaseCutter = rs.AddCylinder([0, 0, socketHeight], [0, 0, 200], 200)
    socketBase = rs.BooleanDifference([socketBase], [socketBaseCutter], True)
    shell = rs.BooleanUnion([shell, socketBase])
    
    return shell
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

# diameter of silver socket: 42mm
# diameter of plastic socket: 35mm
# diameter for clip light: 32mm
def cutHole(toCut, baseHeight):
    cylindar = rs.AddCylinder(origin, baseHeight, 22.5)
    toCut = rs.BooleanDifference(toCut, cylindar)


#TODO: add arch on top of shade so it is not just open but has top layer taht can be printed

bottom = createBase(baseInterpolated)
createWalls(isLumpy, isBackForth, isLargeBase)
shade = loftAndCap()
cutHole(shade, socketHeight)

deleteAllCurves()

#socket = universalBase.createSocket()
