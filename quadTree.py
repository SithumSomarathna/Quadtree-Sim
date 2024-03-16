import random
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = (random.random() * 2 - 1) * math.pi
        self.velocity = 1
        self.quadtree: QuadTree = None

    def move(self):
        self.x += math.cos(self.angle) * self.velocity
        self.y -= math.sin(self.angle) * self.velocity

    def outsideBoundary(self):
        return (self.x < self.quadtree.x1 or
                self.x >= self.quadtree.x2 or
                self.y < self.quadtree.y1 or 
                self.y >= self.quadtree.y2)

    def exitTree(self):
        if len(self.quadtree.parent.children) == 0: print("Ah")
        self.quadtree.points.remove(self)
        self.quadtree.reshape()
        self.quadtree = None

class QuadTree:
    def __init__(self, x1, y1, x2, y2, parent):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = x2 - x1
        self.height = y2 - y1
        self.hasChildren = False
        self.capacity = 4
        self.points = []
        self.children = []
        self.parent = parent

    def insert(self, newPoint: Point):
        if len(self.points) == self.capacity:
            self.subdivide()
        self.points.append(newPoint)
        newPoint.quadtree = self
        if self.hasChildren:
            for point in self.points:
                if point.x <= self.x1 + self.width / 2 and point.y <= self.y1 + self.height / 2: self.children[0].insert(point)
                elif point.x > self.x1 + self.width / 2 and point.y <= self.y1 + self.height / 2: self.children[1].insert(point)
                elif point.x <= self.x1 + self.width / 2 and point.y > self.y1 + self.height / 2: self.children[2].insert(point)
                elif point.x > self.x1 + self.width / 2 and point.y > self.y1 + self.height / 2: self.children[3].insert(point)
                else: print("Error: Point does not lie within the bounds of this QuadTree")
            self.points = []

    def subdivide(self):
        self.children = [
            QuadTree(self.x1, self.y1, self.x1 + self.width / 2, self.y1 + self.height / 2, self),
            QuadTree(self.x1 + self.width / 2, self.y1, self.x2, self.y1 + self.height / 2, self),
            QuadTree(self.x1, self.y1 + self.height / 2, self.x1 + self.width / 2, self.y2, self),
            QuadTree(self.x1 + self.width / 2, self.y1 + self.height / 2, self.x2, self.y2, self)
        ]
        self.hasChildren = True

    def reshape(self):
        par = self.parent
        if par is None or par.children[0].hasChildren or par.children[1].hasChildren or par.children[2].hasChildren or par.children[3].hasChildren: return
        numPoints = sum(len(child.points) for child in par.children)
        if numPoints <= par.capacity:
            par.points += par.children[0].points + par.children[1].points + par.children[2].points + par.children[3].points
            for point in par.points: point.quadtree = par
            par.children = []
            par.hasChildren = False
            par.reshape()

    def findPoints(self, x1, y1, x2, y2):
        points = []
        if self.hasChildren:
            for child in self.children:
                if not (x2 < child.x1 or x1 > child.x2 or y1 > child.y2 or y2 < child.y1):
                    points += child.findPoints(x1, y1, x2, y2)
            return points
        else:
            return self.points

    def getBoxes(self):
        boxes = [(self.x1, self.y1, self.width, self.height)]
        if self.hasChildren:
            boxes += self.children[0].getBoxes() + self.children[1].getBoxes() + self.children[2].getBoxes() + self.children[3].getBoxes()
        return boxes
        