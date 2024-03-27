### This is supposed to make branches come off of a base of a certain shape
import rhinoscriptsyntax as rs
import math

origin = (0, 0, 0)
edge = (200, 200, 200)
height = 100
lumpNumber = 10
pointsToMove = [] # will hold spinePoints

#offsetSpine variables
offsetAmount = 6


def generateSpine(center, spineHeight, lumps):
    #draw points and line from origin -> height
    spineBottom = rs.AddPoint(center)
    spineTop = rs.CopyObject(spineBottom, [0, 0, spineHeight])
    spine = rs.AddLine(spineBottom, spineTop)
    
    #divide spine and offset points
    spinePoints = rs.DivideCurve(spine, lumps, True)
    
    return spinePoints


# create a list of 4 vectors to offset the points on spine
# 
def createOffsetList(offsetAmount):
    offsetList = []
    offsetList.append([1.0 * offsetAmount, 0.0, 0.0])  #x+
    offsetList.append([0.0, -1.0 * offsetAmount, 0.0]) #y-
    offsetList.append([-1.0 * offsetAmount, 0.0, 0.0]) #x-
    offsetList.append([0.0, 1.0 * offsetAmount, 0.0])  #y+
    
    return offsetList

#applies vectors passes through points vector
def offsetSpine(points, scale):
    
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
    
    return offsetValues


pointsToMove = generateSpine(origin, height, lumpNumber)
offsetScaleList = createOffsetList(offsetAmount)

offsetValues = offsetSpine(pointsToMove, offsetScaleList)

rs.AddCurve(offsetValues)

# generate straight line
# Divide center curve into segments
# generate points at segments
# move points in different directions



# generate mid curve rising from origin
# divide center curve into segments
# create ellipse around curve at origin
# 
