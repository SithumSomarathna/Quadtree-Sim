# Quadtree-Sim

Shows the manipulation of quad tree boundaries in real time to store the coordinate positions of moving points. The point closest to the mouse position is also identified.

## Method

A quad tree data structure is used to store the positions of each moving point. When a point moves outside the boundary of its quad tree, the tree re-inserts the point and rearranges itself. The quad tree implementation allows for efficient checking of point collisions as well as identifying the closes point to the mouse

## Usage

Run visualiser.py. Click to spawn points

## Visualisation

The green boxes represent the boundaries of current quad trees. A red line will go from the mouse to the nearest point.