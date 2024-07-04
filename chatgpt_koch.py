from solid2 import *
import math
import numpy as np

degs60 = np.pi / 3
cos60 = np.cos(degs60)
sin60 = np.sin(degs60)

def koch_line(start, end, factor):
    """
    Segments a line to Koch line, creating fractals.


    :param tuple start:  (x, y) coordinates of the starting point
    :param tuple end: (x, y) coordinates of the end point
    :param float factor: the multiple of sixty degrees to rotate
    :returns tuple: tuple of all points of segmentation
    https://nostarch.com/download/PythonPlayground_SampleChapter1.pdf
    """

    # coordinates of the start
    x1, y1 = start[0], start[1]

    # coordinates of the end
    x2, y2 = end[0], end[1]

    # the length of the line
    l = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # first point: same as the start
    a = (x1, y1)

    # second point: one third in each direction from the first point
    b = (x1 + (x2 - x1)/3., y1 + (y2 - y1)/3.)

    # third point: rotation for multiple of 60 degrees
    c = (b[0] + l/3. * np.cos(factor * np.pi/3.), b[1] + l/3. * np.sin(factor * np.pi/3.))

    # fourth point: two thirds in each direction from the first point
    d = (x1 + 2. * (x2 - x1)/3., y1 + 2. * (y2 - y1)/3.)

    # the last point
    e = end

    return {'a': a, 'b': b, 'c': c, 'd' : d, 'e' : e, 'factor' : factor}

def koch_snowflake(degree, d=5.0):
    """Generates all lines for a Koch Snowflake with a given degree.

    :param int degree: how deep to go in the branching process
    :param float s: the length of the initial equilateral triangle
    :returns list: list of all lines that form the snowflake
    """
    # all lines of the snowflake
    lines = []

    # vertices of the initial equilateral triangle
    # A = (0., 0.)
    # B = (s, 0.)
    # C = (s * cos60, s * sin60)
    # https://math.stackexchange.com/questions/3786698/find-the-two-points-for-an-equilateral-triangle-inscribed-inside-a-circle
    A = ( -d * sin60, -d/2)
    B = (d * sin60, -d/2)
    C = (0, d)



    # set the initial lines
    if degree == 0:
        lines.append(koch_line(A, B, 0))
        lines.append(koch_line(B, C, 2))
        lines.append(koch_line(C, A, 4))
    else:
        lines.append(koch_line(A, B, 5))
        lines.append(koch_line(B, C, 1))
        lines.append(koch_line(C, A, 3))

    for i in range(1, degree):
        # every lines produce 4 more lines
        for _ in range(3*4**(i - 1)):
            line = lines.pop(0)
            factor = line['factor']

            lines.append(koch_line(line['a'], line['b'], factor % 6))  # a to b
            lines.append(koch_line(line['b'], line['c'], (factor - 1) % 6))  # b to c
            lines.append(koch_line(line['c'], line['d'], (factor + 1) % 6))  # d to c
            lines.append(koch_line(line['d'], line['e'], factor % 6))  # d to e

    return lines


def snowflakes_lines(degree, diameter, height):
    lines = koch_snowflake(degree=degree, d=diameter)
    # extract the line coordinates
    x, y, z = [], [], []
    for l in lines:
        x.extend([l['a'][0], l['b'][0], l['c'][0], l['d'][0], l['e'][0]])
        y.extend([l['a'][1], l['b'][1], l['c'][1], l['d'][1], l['e'][1]])
    z = [height] * len(x)

    return [(x_, y_, z_) for x_, y_, z_ in zip(x, y, z)]

def cumsum(num_list):
    # Cumulative sum of a list
    return [0]+[sum(num_list[:i+1]) for i in range(len(num_list))]

def cummult(num_list):
    # Cumulative multiplication of a list
    return [1]+[np.prod(num_list[:i+1]) for i in range(len(num_list))]


def rotate_layer(layer, i):
    # Rotate the layer by i degrees
    angle = i
    return [(x * np.cos(np.radians(angle)) - y * np.sin(np.radians(angle)), x * np.sin(np.radians(angle)) + y * np.cos(np.radians(angle)), z) for x, y, z in layer]

def scale_layer(layer, scale):
    # Scale the layer by scale
    return [(x * scale, y * scale, z) for x, y, z in layer]

def offset_layer(coordinates, distance):
    coordinates = iter(coordinates)
    x1, y1, z1 = coordinates.__next__()
    z = distance
    points = []
    for x2, y2, z1 in coordinates:
        # tangential slope approximation
        if x1 == x2:
            continue
        slope = (y2 - y1) / (x2 - x1)
        pslope = -1/slope
        # try:
        #     slope = (y2 - y1) / (x2 - x1)
        #     # perpendicular slope
        #     pslope = -1/slope  # (might be 1/slope depending on direction of travel)
        # except ZeroDivisionError:
        #     continue
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2

        sign = ((pslope > 0) == (x1 > x2)) * 2 - 1

        # if z is the distance to your parallel curve,
        # then your delta-x and delta-y calculations are:
        #   z**2 = x**2 + y**2
        #   y = pslope * x
        #   z**2 = x**2 + (pslope * x)**2
        #   z**2 = x**2 + pslope**2 * x**2
        #   z**2 = (1 + pslope**2) * x**2
        #   z**2 / (1 + pslope**2) = x**2
        #   z / (1 + pslope**2)**0.5 = x

        delta_x = sign * z / ((1 + pslope**2)**0.5)
        print(pslope, delta_x)
        delta_y = pslope * delta_x


        points.append((mid_x + delta_x, mid_y + delta_y, z1))
        x1, y1 = x2, y2
    return points



def koch_snowflake_tower(depth, diameter, heigth, num_layers, height_per_layer, wall_thickness=2):

    print("Generating Koch Snowflake Tower...")
    # Generate the Koch snowflake
    snowflake = snowflakes_lines(depth, diameter, height=heigth)
    snowflake_points = len(snowflake)

    curve_line = [0.5]*(num_layers)
    curve_line = cumsum(curve_line)
    scale_line = [1.00]*(num_layers)
    scale_line = cummult(scale_line)
    offset_line = [0]*(num_layers)
    offset_line = cumsum(offset_line)



    vertices, faces = [], []
    for i in range(num_layers+1):
        # Generate the vertices for the current layer
        layer = [(x, y, z + i * height_per_layer) for j, (x, y, z) in enumerate(snowflake)]
        layer = rotate_layer(layer, curve_line[i])
        layer = scale_layer(layer, scale_line[i])
        # layer = offset_layer(layer, offset_line[i])
        vertices += layer

        # Generate the faces for the current layer
        for j in range(snowflake_points - 1):
            faces.append([j + i * snowflake_points, j + 1 + i * snowflake_points, j + snowflake_points + i * snowflake_points])
            faces.append([j + snowflake_points + i * snowflake_points, j + 1 + snowflake_points + i * snowflake_points, j + 1 + i * snowflake_points])
        faces.append([snowflake_points - 1 + i * snowflake_points, i * snowflake_points, snowflake_points + i * snowflake_points])
        faces.append([snowflake_points + i * snowflake_points, i * snowflake_points, i * snowflake_points + snowflake_points - 1])



    return polyhedron(points=vertices, faces=faces)

if __name__ == '__main__':
    depth = 2  # Set the depth of the Koch snowflake
    diameter = 50  # Diameter of the Koch snowflake
    height = 100  # Height of the tower
    height_per_layer = 1  # Number of layers in the tower
    bottom_height = 0 # Height of the bottom part of the tower
    wall_thickness = 2  # Thickness of the walls

    num_layers = int(height/height_per_layer)

    print(f"Number of layers: {num_layers}")

    tower = koch_snowflake_tower(depth, diameter, bottom_height, num_layers, height_per_layer)

    tower.save_as_scad()
    # scad_render_to_file(tower, 'koch_snowflake_tower.scad')
