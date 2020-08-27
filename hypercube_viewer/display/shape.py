from math import pi, cos, sin
from copy import deepcopy

class Shape():
    def __init__(self, dimensions, rotations):
        self.create_shape(dimensions)
        self.rotations = rotations
    
    def create_shape(self, dimensions):

        self.dimensions = dimensions

        # Create shape vertices
        self.points = [[-0.5], [0.5]] # Start at 1D
        for i in range(1, dimensions):

            # Double points
            for point in range(0, 2 ** i):
                self.points.append(self.points[point].copy())
            
            # Add new component
            for point in range(0, len(self.points)):
                if point < len(self.points) / 2:
                    self.points[point].append(-0.5)
                else:
                    self.points[point].append(0.5)
        
        # Create shape edges
        self.edges = []
        for first_point in range(0, len(self.points) - 1):
            for second_point in range(first_point + 1, len(self.points)):
                differences = 0
                for component in range(0, len(self.points[first_point])):
                    if self.points[first_point][component] != self.points[second_point][component]:
                        differences += 1
                if differences == 1:
                    self.edges.append([first_point, second_point])
    
    def rotate(self):
        for rotation in self.rotations:
            for point in self.points:
                new_axis1 = (point[rotation[0][0]] * cos(rotation[1])) + (point[rotation[0][1]] * sin(rotation[1]))
                new_axis2 = (point[rotation[0][0]] * -sin(rotation[1])) + (point[rotation[0][1]] * cos(rotation[1]))
                point[rotation[0][0]] = new_axis1
                point[rotation[0][1]] = new_axis2