from quadTree import QuadTree, Point
import math

def movingAway(point: Point, norm):
    theta = abs(norm - point.angle)
    if theta > math.pi: theta = 2 * math.pi - theta
    return theta <= math.pi / 2

def deflect(point: Point, norm):
    theta = point.angle + math.pi
    if theta > math.pi: theta -= 2 * math.pi
    angle = norm - theta + norm
    if angle <= -math.pi: angle += 2 * math.pi
    elif angle > math.pi: angle -= 2 * math.pi
    return angle

def checkWallCollisions(point: Point, radius, width, height):
    norm = None
    if point.x - radius <= 0: norm = 0
    elif point.x + radius >= width: norm = -math.pi
    elif point.y - radius <= 0: norm = -math.pi/2
    elif point.y + radius >= height: norm = math.pi/2
    if norm is not None and not movingAway(point, norm):
        # print(point.angle, deflect(point, norm))
        point.angle = deflect(point, norm)
        # print(point.angle, norm)

def dist(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def checkPointCollisions(point: Point, radius, qt: QuadTree):
    nears = qt.findPoints(point.x - radius * 2, point.y - radius * 2, point.x + radius * 2, point.y + radius * 2)
    for p in nears:
        if p != point and dist(point, p) <= radius * 2:
            norm = math.atan2(-(point.y - p.y), point.x - p.x)
            if not movingAway(point, norm):
                point.angle = deflect(point, norm)
                break
