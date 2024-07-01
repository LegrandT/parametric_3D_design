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

def koch_snowflake(degree, s=5.0):
    """Generates all lines for a Koch Snowflake with a given degree.

    :param int degree: how deep to go in the branching process
    :param float s: the length of the initial equilateral triangle
    :returns list: list of all lines that form the snowflake
    """
    # all lines of the snowflake
    lines = []

    # vertices of the initial equilateral triangle
    A = (0., 0.)
    B = (s, 0.)
    C = (s * cos60, s * sin60)

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

def snowflakes_lines(degree, height, s=5):
    lines = koch_snowflake(degree=degree, s=s)
    # extract the line coordinates
    x, y, z = [], [], []
    for l in lines:
        x.extend([l['a'][0], l['b'][0], l['c'][0], l['d'][0], l['e'][0]])
        y.extend([l['a'][1], l['b'][1], l['c'][1], l['d'][1], l['e'][1]])
    z = [height] * len(x)

    return [(x_, y_, z_) for x_, y_, z_ in zip(x, y, z)]



def koch_snowflake_tower(depth, diameter, num_layers, height_per_layer):

    print("Generating Koch Snowflake Tower...")
    # Generate the Koch snowflake
    line_length = np.sqrt(3) * diameter / 2
    snowflake = snowflakes_lines(depth, diameter, s=line_length)
    snowflake_points = len(snowflake)

    vertices, faces = [], []
    for i in range(num_layers):
        # Generate the vertices for the current layer
        for j, (x, y, z) in enumerate(snowflake):
            vertices.append((x, y, z + i * height_per_layer))

        # Generate the faces for the current layer
        for j in range(snowflake_points - 1):
            faces.append([j + i * snowflake_points, j + 1 + i * snowflake_points, j + snowflake_points + i * snowflake_points])
            faces.append([j + snowflake_points + i * snowflake_points, j + 1 + snowflake_points + i * snowflake_points, j + 1 + i * snowflake_points])
        faces.append([snowflake_points - 1 + i * snowflake_points, i * snowflake_points, snowflake_points + i * snowflake_points])
        faces.append([snowflake_points + i * snowflake_points, i * snowflake_points, i * snowflake_points + snowflake_points - 1])

    # vertices = [
    #     (0, 0, 0),  # bottom center point
    #     (100, 0, 0),  # bottom right point
    #     (100, 100, 0),  # bottom front point
    #     (0, 100, 0),  # bottom left point
    #     (50, 50, 100)  # top point
    # ]

    # faces = [
    #     [0, 1, 2],  # bottom face
    #     [2, 3, 0],  # bottom face
    #     [0, 1, 4],  # side face
    #     [1, 2, 4],  # side face
    #     [2, 3, 4],  # side face
    #     [3, 0, 4],  # side face
    # ]

    return polyhedron(points=vertices, faces=faces)

if __name__ == '__main__':
    depth = 3  # Set the depth of the Koch snowflake
    num_layers = 10  # Number of layers in the tower
    height_per_layer = 10  # Height of each layer
    diameter = 100  # Diameter of the Koch snowflake

    tower = koch_snowflake_tower(depth, diameter, num_layers, height_per_layer)
    tower.save_as_scad()
    # scad_render_to_file(tower, 'koch_snowflake_tower.scad')
