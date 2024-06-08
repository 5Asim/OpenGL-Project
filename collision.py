from math import *
import sys

OO = 1000000000
class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Collosion:
    def line_polygon_intersect(self,line, vertices):
        """
        We use SAT here to check collision
        """
        lstOfVertices = line.get_vertices()
        if self.two_polygon_intersect(lstOfVertices, vertices):
            return True
        return False
    
            

    def projectVertices(self,vertices,axis):
        """
        This function project a list of vertices on axis by using dot product 
        Then return the max point and min point on axis
        """
        minA, maxA = OO, -OO
        # to project point on axis , just do dot product
        for v in vertices:
            proj = axis[0]*v[0] + axis[1]*v[1]
            if proj < minA:
                minA = proj
            if proj > maxA:
                maxA = proj
        return (minA,maxA)
    
    def get_unit_normal_vector(self,p1,p2):
        """"
        return unit normal vector of edge p1p2
        """
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        magnitude = sqrt(dx**2 + dy**2)
        if magnitude != 0:  # To avoid division by zero
            dx = dx/magnitude
            dy = dy/magnitude
        return [-dy,dx]

col = Collosion()

def test_car_walls(carModel, walls):
    """
    this method use SAT to check car & walls collision
    """
    vertices = carModel.get_vertices()
    for i in walls:
        if col.line_polygon_intersect(i,vertices):
            return True
    return False
