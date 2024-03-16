from quadTree import QuadTree, Point
from collections import deque
import math

def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def furthestCornerDist(x, y, qt: QuadTree):
    return max(dist(x, y, qt.x1, qt.y1), dist(x, y, qt.x1, qt.y2), dist(x, y, qt.x2, qt.y1), dist(x, y, qt.x2, qt.y2))

def closestCornerDist(x, y, qt: QuadTree):
    if x < qt.x1 or x > qt.x2 or y < qt.y1 or y > qt.y2:
        return min(dist(x, y, qt.x1, qt.y1), dist(x, y, qt.x1, qt.y2), dist(x, y, qt.x2, qt.y1), dist(x, y, qt.x2, qt.y2))
    else:
        return 0

def findNearest(x, y, root: QuadTree):
    searchRadius = furthestCornerDist(x, y, root)
    count = 0
    q = deque()
    q.append(root)
    while(count != len(q)):
        qt: QuadTree = q.popleft()
        if qt.hasChildren:
            count = 0
            for child in qt.children:
                if (child.hasChildren or len(child.points) > 0) and closestCornerDist(x, y, child) <= searchRadius:
                    q.append(child)
                    searchRadius = min(searchRadius, furthestCornerDist(x, y, child))
        else:
            if closestCornerDist(x, y, qt) <= searchRadius:
                count += 1
                q.append(qt)
            else:
                count = 0

    # Queue should now only have leaf quadtrees with at least one point
    minDist = math.inf
    minPoint = None
    while(len(q) > 0):
        qt: QuadTree = q.popleft()
        for point in qt.points:
            d = dist(x, y, point.x, point.y)
            if d < minDist:
                minDist = d
                minPoint = point
    
    return minPoint
