from typing import List
import matplotlib.pyplot as plt
from src.delauney.helper import Triangle, Point

"""
TODO:

# 1 Add a readme to explain the specific math
# 2 Add dependencies
# Add complimentary test files test_delauney.py and
test voronoi.py 
"""

class Delauney:
    """
    computes the Delauney triangulation for a given set of points
    """
    def __init__(self, points: List[Point]):
        self.points = points
        self.triangulation = []
        self.super_triangle = self.create_super_triangle()

    def create_super_triangle(self) -> Triangle:
        """
        instantiates the super triangle used in the
        Bowyer Watson algorithm
        """
        d = 1500
        x = [point.x for point in self.points]
        y = [point.y for point in self.points]

        min_x = min(x)
        max_x = max(x)
        min_y = min(y)
        max_y = max(y)

        v1 = Point(min_x - abs(max_x - min_x) - d, min_y - d)
        v2 = Point(max_x + d, min_y - d)
        v3 = Point(max_x + d, max_y + abs(max_y - min_y) + d)

        new_super_triangle = Triangle([v1, v2, v3])
        self.triangulation.append(new_super_triangle)

        return new_super_triangle

    def triangulate(self) -> List[Triangle]:
        """
        implementation of the Bowyer-Watson algorithm
        for computing the Delauney triangulation
        """
        # add all the points one at a time to the triangulation
        for point in self.points:
            bad_triangles = []

            for triangle in self.triangulation:
                if triangle.in_circumcircle(point):
                    bad_triangles.append(triangle)

            polygon = []

            # find the boundary of the polygonal hole
            for triangle in bad_triangles:
                for edge in triangle.edges:
                    # if edge is not shared by any other triangles in badTriangles
                    other_edges = [e for t in bad_triangles if t != triangle for e in t.edges]
                    if edge not in other_edges and edge.reversed() not in other_edges:
                        polygon.append(edge)

            for triangle in bad_triangles:
                self.triangulation.remove(triangle)

            # re-triangulate the polygonal hole
            for edge in polygon:
                new_triangle = Triangle([edge.point_1, edge.point_2, point])
                self.triangulation.append(new_triangle)

        # done inserting points, now clean up
        to_remove = []
        for triangle in self.triangulation:
            if triangle.share_point(self.super_triangle):
                to_remove.append(triangle)

        for triangle in to_remove:
            self.triangulation.remove(triangle)

        return self.triangulation

    def visualize(self):
        """
        visual representation of the
        Delauney triangulation
        """
        for triangle in self.triangulation:
            for edge in triangle.edges:
                plt.plot([edge.point_1.x, edge.point_1.y, edge.point_2.x, edge.point_2.y])

        plt.show()

if __name__ == "__main__":
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

    points = []

    for point in point_list:
        points.append(Point(point[0], point[1]))

    d = Delauney(points)
    d.triangulate()
    d.visualize()

    print(len(d.triangulation))