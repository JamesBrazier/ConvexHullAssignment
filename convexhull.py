"""
   Convex Hull Assignment: COSC262 (2018)
   Student Name: James Brazier
   Usercode: jbr185
"""

def readDataPts(filename, N):
    """Reads the first N lines of data from the input file
       and returns a list of N tuples
       [(x0,y0), (x1, y1), ...]
    """
    file = open(filename, "r")
    file = file.readlines()
    listPts = []
    for num in range(len(file)):
        file[num] = file[num].split()
        listPts.append((float(file[num][0]), float(file[num][1])))
    return listPts

#Giftwrap

def giftwrap(listPts):
    """Returns the convex hull vertices computed using the
       giftwrap algorithm as a list of m tuples
       [(u0,v0), (u1,v1), ...]    
    """
    k = lowestY(listPts)
    i = 0
    v = 0
    listPts.append(listPts[k])
    while k != (len(listPts) - 1):
        listPts[k], listPts[i] = listPts[i], listPts[k]
        minAngle = 361
        for j in range(i+1, len(listPts)):
            angle = theta(listPts[i], listPts[j])
            if angle < minAngle and angle > v and listPts[j] != listPts[i]:
                minAngle = angle
                k = j
        i += 1
        v = minAngle
    return listPts[:i]

def lowestY(listPts):
    """Searches through the list of points taking the point with the 
       lowest Y value in the list, in case of ties the point with the 
       highest X value is returned
    """
    lowestIndex = 0
    lowestPt = listPts[lowestIndex]
    for index, point in enumerate(listPts):
        if point[1] < lowestPt[1]:
            lowestIndex = index
            lowestPt = listPts[lowestIndex]
        elif point[1] == lowestPt[1]:
            if point[0] > lowestPt[0]:
                lowestIndex = index
                lowestPt = listPts[lowestIndex]
    return lowestIndex

def theta(pointA, pointB):
    """Makes an approximantion of the angle of the line between two points
       through the difference between the X and Y coordinates of the points
    """
    dx = pointB[0] - pointA[0]
    dy = pointB[1] - pointA[1]
    if abs(dx) < 1.e-6 and abs(dy) < 1.e-6:
        return 0
    else:
        t = dy / (abs(dx) + abs(dy))
    if dx < 0:
        t = 2 - t
    elif dy <= 0:
        t = 4 + t
    return t*90

#Grahamscan

def grahamscan(listPts):
    """Returns the convex hull vertices computed using the
       Graham-scan algorithm as a list of m tuples
       [(u0,v0), (u1,v1), ...]  
    """
    k = lowestY(listPts)
    p0 = listPts[k]
    listPts.sort(key=lambda x : theta(p0, x))
    stack = listPts[:3]
    n = len(listPts)
    for i in range(3, n):
        while not isCCW(stack[-2], stack[-1], listPts[i]):
            stack.pop()
        stack.append(listPts[i])
    return stack

def lineFn(ptA, ptB, ptC):
    """Returns a value which can be used to determine whether the point C
       is on or to the left or right of the line between points A & B
    """
    return (
        (ptB[0] - ptA[0]) * (ptC[1] - ptA[1]) -
        (ptB[1] - ptA[1]) * (ptC[0] - ptA[0]) )

def isCCW(ptA, ptB, ptC):
    """Returns true if the points A, B & C make a counter clock-wise turn
    """
    return lineFn(ptA, ptB, ptC) > 0

#Quick Hull (quicksort for convex hulls)

def amethod(listPts):
    #QuickHull
    """returns the points of the convex hull of the set of points
       through spliting the set into equal subsets of half the points
       recursively similar to quicksort
    """
    chull = []
    minX = listPts[lowestX(listPts)]
    maxX = listPts[highestX(listPts)]
    chull.append(minX)
    chull.append(maxX)
    abovePts = []
    belowPts = []
    abovePts = aboveLn(minX, maxX, listPts)
    belowPts = aboveLn(maxX, minX, listPts) 
    findHull(minX, maxX, abovePts, chull)
    findHull(maxX, minX, belowPts, chull)
    return chull
             
def findHull(A, B, listPts, chull):
    """The recursive function of quick hull
    """
    if len(listPts) == 0:
        return
    else:
        maxDist = 0
        maxPt = None
        for point in listPts:
            dist = abs(lineFn(A, B, point))
            if dist >= maxDist:
                maxDist = dist
                maxPt = point
        if lineFn(A, B, maxPt) != 0:      
            chull.append(maxPt)
        abovePts = aboveLn(A, maxPt, listPts)
        belowPts = aboveLn(maxPt, B, listPts) 
        findHull(A, maxPt, abovePts, chull)
        findHull(maxPt, B, belowPts, chull)
    
def lowestX(listPts):
    """Returns the point with the lowest X value
    """
    lowestIndex = 0
    lowestPt = listPts[lowestIndex]
    for index, point in enumerate(listPts):
        if point[1] < lowestPt[1]:
            lowestIndex = index
            lowestPt = listPts[lowestIndex]
    return lowestIndex

def highestX(listPts):
    """Returns the point with the highest X value
    """    
    highestIndex = 0
    highestPt = listPts[highestIndex]
    for index, point in enumerate(listPts):
        if point[1] > highestPt[1]:
            highestIndex = index
            highestPt = listPts[highestIndex]
    return highestIndex
    
def aboveLn(ptA, ptB, listPts):
    """Returns a list of the points above a line between points
       A & B
    """
    aboveLn = []
    for point in listPts:
        if isCCW(ptA, ptB, point):
            aboveLn.append(point) 
    return aboveLn  

#Main

def main():
    listPts = readDataPts('Points data\A_3000.dat', 3000)
    print(giftwrap(listPts.copy())) 
    print(grahamscan(listPts.copy()))
    print(amethod(listPts.copy()))       

if __name__  ==  "__main__":
    main()
    
  