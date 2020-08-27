from copy import deepcopy

def project_2D(original_points):
    
    points = deepcopy(original_points)

    # Special case 1D
    if (len(points[0]) == 1):
        points[0].append(0)
        points[1].append(0)

    # Convert points to 2D
    while len(points[0]) != 2:
        for point in points:
            scale_factor = 1 / (2 - point[-1])
            for scaling_component in range(0, len(point) - 1):
                point[scaling_component] *= scale_factor
            del point[-1]
    
    return points