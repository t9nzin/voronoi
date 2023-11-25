from typing import List, Tuple
from helper import determinant
import math

#TODO: combine point & edge classes into Delauney class
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point: (x={self.x}, y={self.y})"

class Edge(Point):
    def __init__(self, start, end):
        super().__init__(start.x, start.y)
        self.end = Point(end.x, end.y)

    def __str__(self):
        return f"Edge: (x1, y1)=({self.x}, {self.y}), " \
               f"(x2, y2)=({self.end.x}, {self.end.y})"

class Triangle:
    def __init__(self, vertices: List[Tuple[float, float]]):
        if len(vertices) != 3:
            raise ValueError("Triangle must have 3 vertices")

        for vertice in vertices:
            if type(vertice) is not tuple:
                raise TypeError("Enter vertices as list of tuples")

        self.v1, self.v2, self.v3 = vertices
        if not self.is_ccw(vertices):
            vertices[1], vertices[2] = vertices[2], vertices[1]
        self.vertices = vertices
        self.edges = [(self.v1, self.v2), (self.v2, self.v3), (self.v3, self.v1)]

    def __str__(self):
        return f"Triangle: (v1={self.v1}, v2={self.v2}, v3={self.v3})"

    def circumcircle(self):
        # Get the circumcenter and circumradius of the
        # circumcircle for a given triangle

        #TODO: look into fixing this .self reassignment
        v1 = self.v1
        v2 = self.v2
        v3 = self.v3

        a = determinant([[v1[0], v1[1], 1],
                         [v2[0], v2[1], 1],
                         [v3[0], v3[1], 1]])

        bx = determinant([[v1[0]**2 + v1[1]**2, v1[1], 1],
                          [v2[0]**2 + v2[1]**2, v2[1], 1],
                          [v3[0]**2 + v3[1]**2, v3[1], 1]])

        by = determinant([[v1[0]**2 + v1[1]**2, v1[0], 1],
                          [v2[0]**2 + v2[1]**2, v2[0], 1],
                          [v3[0]**2 + v3[1]**2, v3[0], 1]])

        c = determinant([[v1[0]**2 + v1[1]**2, v1[0], v1[1]],
                              [v2[0]**2 + v2[1]**2, v2[0], v2[1]],
                              [v3[0]**2 + v3[1]**2, v3[0], v3[1]]])

        # ux, uy are the circumcenter coordinates
        ux = bx / (2*a)
        uy = -1 * (by / (2*a))
        circumradius = math.sqrt(bx**2 + by**2 + 4*a*c)/ (2 * abs(a))
        print("d")
        return (ux, uy), circumradius

    def in_circumcircle(self, point):
        # Check if a given point is within
        # the circumcircle of a given point
        a, b, c = self.vertices

        ax, ay = a
        bx, by = b
        cx, cy = c
        dx, dy = point

        det = determinant([[ax - dx, ay - dy, (ax - dx)**2 + (ay - dy)**2],
                           [bx - dx, by - dy, (bx - dx)**2 + (by - dy)**2],
                           [cx - dx, cy - dy, (cx - dx)**2 + (cy - dy)**2]])

        # if det equal 0 then d is on C
        # if det > 0 then d is inside C
        if det >= 0:
            return True
        # if det < 0 then d is outside C
        else:
            return False

    def is_ccw(self, points):
        # Checks if points is ordered counter-clockwise
        (ax, ay), (bx, by), (cx, cy) = points
        return (bx - ax) * (cy - ay) - (cx - ax) * (by - ay) >= 0

    def contains_point(self, point):
        # Check if the given point is a vertex
        if point in self.vertices:
            return True
        else:
            return False

    def share_point(self, triangle):
        # Check if two triangles share a vertice
        for vertex in self.vertices:
            if vertex in triangle.vertices:
                return True
        return False

class Delauney:
    def __init__(self, points):
        self.points = points
        self.triangulation = []
        self.super_triangle = self.super_triangle()

    def super_triangle(self):
        d = 1500
        x = [point[0] for point in self.points]
        y = [point[1] for point in self.points]

        min_x = min(x)
        max_x = max(x)
        min_y = min(y)
        max_y = max(y)

        v1 = (min_x - abs(max_x - min_x) - d, min_y - d)
        v2 = (max_x + d, min_y - d)
        v3 = (max_x + d, max_y + abs(max_y - min_y) + d)

        super_triangle = Triangle([v1, v2, v3])
        self.triangulation.append(super_triangle)

        return super_triangle

    def triangulate(self):
        # add all the points one at a time to the triangulation
        # for each point in pointList do
        for point in self.points:
            # badTriangles := empty set
            bad_triangles = []

            # first find all the triangles that are no longer valid due to the insertion
            # for each triangle in triangulation do
            for triangle in self.triangulation:
                # if point is inside circumcircle of triangle
                # add triangle to badTriangles
                if triangle.in_circumcircle(point):  # check if point inside circumcircle
                    bad_triangles.append(triangle)  # if so, add to bad triangles

            # polygon := empty set
            polygon = []

            # find the boundary of the polygonal hole
            # for each triangle in badTriangles do
            for triangle in bad_triangles:
                # for each edge in triangle do
                for edge in triangle.edges:
                    # if edge is not shared by any other triangles in badTriangles
                    other_edges = [e for t in bad_triangles if t != triangle for e in t.edges]
                    if edge not in other_edges and edge[::-1] not in other_edges:
                        # add edge to polygon
                        polygon.append(edge)

            # remove them from the data structure
            # for each triangle in badTriangles do
            for triangle in bad_triangles:
                # remove triangle from triangulation
                self.triangulation.remove(triangle)

            # re-triangulate the polygonal hole
            # for each edge in polygon do
            for edge in polygon:
                # newTri := form a triangle from edge to point
                new_triangle = Triangle([edge[0], edge[1], point])
                # add newTri to triangulation
                self.triangulation.append(new_triangle)

        # done inserting points, now clean up
        to_remove = []
        # for each triangle in triangulation
        for triangle in self.triangulation:
            # if triangle contains a vertex from original super-triangle
            if triangle.share_point(self.super_triangle):
                to_remove.append(triangle)

        # remove triangle from triangulation
        for triangle in to_remove:
            self.triangulation.remove(triangle)

        # return triangulation
        return self.triangulation


# function BowyerWatson (pointList)
# pointList is a set of coordinates defining the points to be triangulated
point_list = [(303, 447),
(136, 316),
(83, 491),
(401, 83),
(374, 510),
(559, 205),
(587, 507),
(408, 273),
(643, 111),
(618, 492),
(476, 120),
(461, 599),
(557, 615),
(566, 60),
(446, 444),
(360, 63),
(672, 668),
(265, 105),
(90, 648),
(68, 631),
(216, 71),
(592, 547),
(644, 524)]

d = Delauney(point_list)
d.triangulate()