import pygame
from quadTree import QuadTree, Point
from collisions import checkWallCollisions, checkPointCollisions
from nearest import findNearest

pygame.init()

c_white = (255,255,255)
c_red = (255,0,0)
c_green = (0,255,0)
c_transparent = (0,0,0)

width, height = 800, 800
screen = pygame.display.set_mode((width, height), pygame.SRCALPHA)
point_radius = 4

qt = QuadTree(0, 0, width, height, None)
points = []

points_surface = pygame.Surface((width, height))
quadtree_surface = pygame.Surface((width, height), pygame.SRCALPHA)
quadtree_surface.fill(c_transparent)
quadtree_surface.set_colorkey(c_transparent)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            newPoint = Point(mouse_x, mouse_y)
            points.append(newPoint)
            qt.insert(newPoint)
            
    if len(points) > 0:
        points_surface.fill(c_transparent)
        for point in points:
            point.move()
            if point.outsideBoundary():
                point.exitTree()
                qt.insert(point)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        nearest = findNearest(mouse_x, mouse_y, qt)
        pygame.draw.circle(points_surface, c_red, (nearest.x, nearest.y), point_radius * 1.5)
        pygame.draw.line(points_surface, c_red, (nearest.x, nearest.y), (mouse_x, mouse_y), round(1.5 * point_radius))

        for point in points:
            checkWallCollisions(point, point_radius, width, height)
            checkPointCollisions(point, point_radius, qt)
            pygame.draw.circle(points_surface, c_white, (point.x, point.y), point_radius)
            
        screen.blit(points_surface, (0, 0))
    
    quadtree_surface.fill(c_transparent)
    for box in qt.getBoxes():
        pygame.draw.rect(quadtree_surface, c_green, pygame.Rect(box[0], box[1], box[2], box[3]), 2)
    screen.blit(quadtree_surface, (0, 0))
    
    pygame.display.update()
