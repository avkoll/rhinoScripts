### This is supposed to make branches come off of a base of a certain shape
import rhinoscriptsyntax as rs
import math

origin = (0, 0, 0)
edge = (200, 200, 200)
height = 100
lumpNumber = 4
pointsToMove = [] # will hold spinePoints

#offsetSpine variables
offsetAmount = 10

#drawTube variables
interp = True
thickness = 10

def deleteAllCurvesAndPoints():
    # find all curves in doc that are not in locked layer
    curves = rs.ObjectsByType(4) #4 is type for curves
    points = rs.ObjectsByType(1) #1 is points
    #check if any found
    if curves or points:
        rs.DeleteObjects(curves)
        rs.DeleteObjects(points)
    else:
        print("No curves found")

def generateSpine(center, spineHeight, lumps):
    #draw points and line from origin -> height
    spineBottom = rs.AddPoint(center)
    spineTop = rs.CopyObject(spineBottom, [0, 0, spineHeight])
    spine = rs.AddLine(spineBottom, spineTop)
    
    #divide spine and offset points
    spinePoints = rs.DivideCurve(spine, lumps, True)
    
    return spinePoints

# create a list of 4 vectors to offset the points on spine
def createOffsetList(offsetAmount):
    offsetList = []
    offsetList.append([1.0 * offsetAmount, 0.0, 0.0])  #x+
    offsetList.append([0.0, -1.0 * offsetAmount, 0.0]) #y-
    offsetList.append([-1.0 * offsetAmount, 0.0, 0.0]) #x-
    offsetList.append([0.0, 1.0 * offsetAmount, 0.0])  #y+
    
    return offsetList

#applies vectors passed through points vector and draws a curve with thosepoints
def drawCurve(points, scale, interp=False):
    offsetValues = []
    offsetValues.append(rs.MoveObject(points[0], [0, 0, 0]))
    
    #iterate through points and move based on vectors given in scale[]
    for i in range(1, len(points)):
        if i % 4 == 1:
            offsetValues.append(rs.MoveObject(points[i], scale[0]))
        elif i % 4 == 2:
            offsetValues.append(rs.MoveObject(points[i], scale[1]))
        elif i % 4 == 3:
            offsetValues.append(rs.MoveObject(points[i], scale[2]))
        elif i % 4 == 0:
            offsetValues.append(rs.MoveObject(points[i], scale[3]))
    
    #check type of curve
    if interp:
        curve = rs.AddCurve(offsetValues)
    else:
        curve = rs.AddInterpCurve(offsetValues)
    
    return curve

# returns plane that is normal to the curve passed through, to be used for drawing shapes normal to origin of curve
def estimatePlane(curve):
    points = rs.DivideCurve(curve, 100)
    planarCurve = rs.AddCurve([points[0], points[1]])
    plane = rs.CurvePlane(planarCurve)
    plane = rs.RotatePlane(plane, 90, plane.YAxis)
    
    return plane


def sweepShape(interp, curve, radius):
    plane = estimatePlane(curve)
    shape = rs.AddCircle(plane, radius)
    tube = rs.AddSweep1(curve, [shape])
    
    return tube 


def drawTube( origin=[0,0,0], 
              height=100, 
              lumpNumber=4,
              offsetAmount=10,
              interp=True,
              thickness=10):
    points = generateSpine(origin, height, lumpNumber)
    offsetVectors = createOffsetList(offsetAmount)
    spiralCurve = drawCurve(points, offsetVectors, interp)
    tube = sweepShape(interp, spiralCurve, thickness)
    rs.CapPlanarHoles(tube)
    
    return tube
    
drawTube(origin, height, lumpNumber, offsetAmount, interp, thickness)

drawTube([0, 0, 50], height, lumpNumber, offsetAmount, interp, thickness)



deleteAllCurvesAndPoints()
