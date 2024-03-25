import rhinoscriptsyntax as rs
import random

origin = (0, 0, 0)
edge = (200, 200, 200)
baseRadius = 12
height = 100
numberOfFins = 40
widthScale = baseRadius * 3 # value is distance that fins stick out from base

curvesToLoft = [] #array that will hold the curves that will be loft to create the walls of the vase
midCurveList = [] #ay ay ay if i delete this in the createWalls function it breaks...

isLumpy = True #true adds curves between top and bottom at intervals == numberOfLumps
numberOfLumps = 6 #number of extra rings between top and bottom to create wavy effect
lumpScale = 1 #not 0
twist = 120 #degree of twist in degrees

switchBack = False #do you want it to switch directions in the rotation?


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
    if lumpy == True:
        midCurveList.append(curvesToLoft[0])
        
        for i in range(0, numberOfLumps):
            localReversedAmount = 1
            if backForth:
                #this applies a random direction to the rotate function. 
                while True:
                    randomValue = random.randint(-1, 4) # change positive and negative values here to weight in either direction
                    if randomValue != 0:
                        localReversedAmount = randomValue / abs(randomValue)
                        break

            #raise curve below it
            midCurve = rs.CopyObject(midCurveList[i], [0, 0, (height / numberOfLumps)])
            #widen curve then rotate it
            midCurveOffset = rs.OffsetCurve(midCurve, edge, (random.randint(1,10) * lumpScale))
            midCurveOffset = rs.RotateObject(midCurve, origin, (twist / numberOfLumps) * localReversedAmount)
            #add the two curves to a list
            midCurveList.append(midCurve)
            curvesToLoft.append(midCurveOffset)


        #for i in range(1, len(midCurveList)):
            #curvesToLoft.append(midCurveList[i])
            #rs.DeleteObject(midCurve)

    else:
        wavyTop = rs.CopyObject(curvesToLoft[0], [0, 0, height])
        rs.RotateObject(wavyTop, origin, twist)
        curvesToLoft.append(wavyTop)
    return

def loftAndCap():
    shell = rs.AddLoftSrf(midCurveList)
    rs.CapPlanarHoles(shell)

def deleteAllCurves():
    # find all curves in doc that are not in locked layer
    curves = rs.ObjectsByType(4) #4 is type for curves
    
    #check if any found
    if curves:
        rs.DeleteObjects(curves)
    else:
        print("No curves found")

bottom = createBase()
createWalls(isLumpy, switchBack)
loftAndCap()
#deleteAllCurves()
