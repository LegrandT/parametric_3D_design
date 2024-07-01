from solid2 import *
# from solid.utils import *
import math

# Function to create a Koch curve segment
def koch_curve(p1, p2, depth):
    if depth == 0:
        return [p1, p2]

    x1, y1 = p1
    x2, y2 = p2

    # Calculate points for the new segments
    dx = x2 - x1
    dy = y2 - y1

    s = (x1 + dx / 3, y1 + dy / 3)
    t = (x1 + 2 * dx / 3, y1 + 2 * dy / 3)

    ux = x1 + dx / 2 - math.sqrt(3) * dy / 6
    uy = y1 + dy / 2 + math.sqrt(3) * dx / 6
    u = (ux, uy)

    # Recursively generate segments
    return koch_curve(p1, s, depth - 1)[:-1] + koch_curve(s, u, depth - 1)[:-1] + koch_curve(u, t, depth - 1)[:-1] + koch_curve(t, p2, depth - 1)

# Function to create the Koch snowflake
def koch_snowflake(depth):
    size = 100
    height = math.sqrt(3) / 2 * size
    p1 = (0, 0)
    p2 = (size, 0)
    p3 = (size / 2, height)

    curve1 = koch_curve(p1, p2, depth)
    curve2 = koch_curve(p2, p3, depth)
    curve3 = koch_curve(p3, p1, depth)

    return curve1[:-1] + curve2[:-1] + curve3[:-1]

# Function to convert points to OpenSCAD polygon format
def points_to_polygon(points):
    return polygon(points)

# Function to extrude the Koch snowflake to create a 3D lamp
def koch_lamp(depth):
    points = koch_snowflake(depth)
    snowflake = points_to_polygon(points)
    lamp = linear_extrude(height=10)(snowflake)
    return lamp

if __name__ == '__main__':
    depth = 3  # Set the depth of the Koch snowflake
    lamp = koch_lamp(depth)
    scad_render_to_file(lamp, 'koch_lamp.scad')
