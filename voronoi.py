import matplotlib.pyplot as plt
import numpy as np
import math

class Voronoi:
    def __init__(self, points, colors):
        if len(colors) != len(points):
            raise ValueError("The length of colors must "
                             "be equal to number of "
                             "specific values!")
        self._x = np.random.rand(100000)
        self._y = np.random.rand(100000)
        self.points = points
        self.colors = []
        self.color_map = dict(zip(self.points, colors))

    # euclidean distance for finding distances between points
    def euclidean_distance(self, p_x, p_y, q_x, q_y):
        return math.sqrt((q_x - p_x) ** 2 + (q_y - p_y) ** 2)

    # a naive implementation for computing voronoi diagrams
    def naive_voronoi(self):
        for i, j in zip(self._x, self._y):
            min_distance = self.euclidean_distance(i, j, self.points[0][0], self.points[0][1])
            min_point = self.points[0]
            for point in self.points:
                if self.euclidean_distance(i, j, point[0], point[1]) < min_distance:
                    min_distance = self.euclidean_distance(i, j, point[0], point[1])
                    min_point = point
            self.colors.append(self.color_map[min_point])

    # plot the voronoi diagram
    def plot(self):
        plt.scatter(self._x, self._y, c=self.colors, s=10, label='Initial Scatter Plot')
        plt.scatter([point[0] for point in self.points], [point[1] for point in self.points], c='black', s=200, marker='*', label='Specific Points')

        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Voronoi Diagram with n = ' + str(len(self.points)))
        plt.legend()

        plt.show()

# Testing out voronoi with n = 6!
voronoi = Voronoi([(0.3, 0.7), (0.6, 0.2), (0.4, 0.5), (0.8, 0.9), (0.2, 0.3), (0.9, 0.6)],
             ["blue", "red", "yellow", "purple", "green", "orange"])
voronoi.naive_voronoi()
voronoi.plot()

