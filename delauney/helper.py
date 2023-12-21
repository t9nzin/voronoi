from typing import List, Tuple
import math

class Point:
    """
    an (x, y) coordinate point
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point: (x={self.x}, y={self.y})"

    def __eq__(self, other):
        if {self.x, self.y} == {other.x, other.y}:
            return True
        else:
            return False

class Edge:
    """
    an edge is the connection between two points
    """
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2

    def __str__(self):
        return f"Edge: point_1={self.point_1}, " \
               f"point_2={self.point_2}"

    def __eq__(self, other):
        if {self.point_1, self.point_2} == {other.point_1, other.point_2}:
            return True
        else:
            return False

    # necessary for comparison of edges
    # because order of points does not matter
    def reversed(self):
        return Edge(self.point_2, self.point_1)

class Triangle:
    """
    a triangle is made up of 3 points
    """
    def __init__(self, vertices: List[Point]):
        if len(vertices) != 3:
            raise ValueError("Triangle must have 3 vertices")

        self.v1, self.v2, self.v3 = vertices

        if not self.is_ccw(vertices):
            vertices[1], vertices[2] = vertices[2], vertices[1]

        self.vertices = vertices
        self.edges = [Edge(self.v1, self.v2), Edge(self.v2, self.v3), Edge(self.v3, self.v1)]
        self.circumcircle = self.get_circumcircle()

    def __str__(self):
        return f"Triangle: (v1={self.v1}, v2={self.v2}, v3={self.v3})"


    def get_circumcircle(self) -> (Tuple[float, float], float):
        """
        gets the circumcenter and circumradius of
        the circumcircle for a given triangle
        """
        a = determinant([[self.v1[0], self.v1[1], 1],
                         [self.v2[0], self.v2[1], 1],
                         [self.v3[0], self.v3[1], 1]])

        bx = determinant([[self.v1[0]**2 + self.v1[1]**2, self.v1[1], 1],
                          [self.v2[0]**2 + self.v2[1]**2, self.v2[1], 1],
                          [self.v3[0]**2 + self.v3[1]**2, self.v3[1], 1]])

        by = determinant([[self.v1[0]**2 + self.v1[1]**2, self.v1[0], 1],
                          [self.v2[0]**2 + self.v2[1]**2, self.v2[0], 1],
                          [self.v3[0]**2 + self.v3[1]**2, self.v3[0], 1]])

        c = determinant([[self.v1[0]**2 + self.v1[1]**2, self.v1[0], self.v1[1]],
                              [self.v2[0]**2 + self.v2[1]**2, self.v2[0], self.v2[1]],
                              [self.v3[0]**2 + self.v3[1]**2, self.v3[0], self.v3[1]]])

        # ux, uy are the circumcenter coordinates
        ux = bx / (2*a)
        uy = -1 * (by / (2*a))
        circumradius = math.sqrt(bx**2 + by**2 + 4*a*c)/ (2 * abs(a))

        return (ux, uy), circumradius

    def in_circumcircle(self, d: Point) -> bool:
        # Check if a given point is within
        # the circumcircle of a given point
        a, b, c = self.vertices

        det = determinant([[a.x - d.x, a.y - d.y, (a.x - d.x)**2 + (a.y - d.y)**2],
                           [b.x - d.x, b.y - d.y, (b.x - d.x)**2 + (b.y - d.y)**2],
                           [c.x - d.x, c.y - d.y, (c.x - d.x)**2 + (c.y - d.y)**2]])

        # if det equal 0 then d is on C
        # if det > 0 then d is inside C
        if det >= 0:
            return True
        # if det < 0 then d is outside C
        else:
            return False

    def is_ccw(self, points: List[Point]) -> bool:
        """
        checks if points are ordered counter-clockwise
        """
        # points must be arranged counter clockwise for
        # determination of whether a point is within the
        # circumcircle to be accurate
        a, b, c = points
        return (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y) >= 0

    def contains_point(self, point: Point) -> bool:
        # Check if the given point is a vertice
        if point in self.vertices:
            return True
        else:
            return False

    def share_point(self, triangle) -> bool:
        # Check if two triangles share a vertice
        for vertex in self.vertices:
            if vertex in triangle.vertices:
                return True
        return False


def determinant(m: List[List[int]]) -> float:
    """
    calculates the determinant of
    an n by n matrix m
    """
    if len(m) == 1 and len(m[0]) == 1:
        return m[0][0]

    if len(m) == 2 and len(m[0]) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    det = 0
    for i in range(len(m[0])):
        submatrix = [row[:i] + row[i + 1:] for row in m[1:]]
        det += ((-1) ** i) * m[0][i] * determinant(submatrix)

    return det