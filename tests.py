#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import math

# Assumes SolidPython is in site-packages
from solid2 import *
# from solid2.utils import *

def kochSnowflake(diameter=100, iterations=3):
    rad = diameter/2
    xrad = rad*math.sqrt(3)/2
    yrad = rad/2
    # Make an equilateral triangle with circumradius=rad
    koch = [polygon([(0,rad), (-xrad, -yrad), (xrad, -yrad)])]
    # Rotate triangle and union to make hexagram
    hexagram = union()(koch[0], rotate(60)(koch[0]))
    koch.append(hexagram)
    if iterations < 2:
        return koch[iterations]
    for level in range(1, iterations):  # indicates level we are building from
        shape = koch[level]
        for i in range(6):
            shape = union()(
                rotate(60)(shape),
                translate([0,rad*2/3,0])(scale(1/3)(koch[level])),
                )
        koch.append(shape)
    return koch[-1]

def kochLamp(
        top_diameter=100,        # Diameter of tree at widest point
        height=150,         # Total height of tree
        base_diameter=100,   # Diameter of base Koch snowflake
        twist_per_100=10,       # Twist of tree base
        slices_per_100=100,      # Slices of base extrusion
        koch_iterations=3,  # iterations of Koch Snowflake
        wall_thickness=2,  # Thickness of walls
        ):

    chamfer_r = -2
    _fn = 72

    base_shape = kochSnowflake(diameter=base_diameter, iterations=koch_iterations)
    # base_shape = square(base_diameter, center=True)
    inner_shape = offset(r=-wall_thickness, _fn=_fn)(base_shape)

    body = linear_extrude(
            height=height,
            scale=top_diameter/base_diameter,
            twist=twist_per_100*height/100,
            slices=slices_per_100*height/100,
    )(base_shape)

    body_floor = linear_extrude(
            height=wall_thickness,
            scale=top_diameter/base_diameter,
            twist=twist_per_100*wall_thickness/100,
            slices=slices_per_100*wall_thickness/100,
    )(base_shape)

    inner_height = height + 2
    inner_body = linear_extrude(
            height=inner_height,
            scale=top_diameter/base_diameter,
            twist=twist_per_100*inner_height/100,
            slices=slices_per_100*inner_height/100,
    )(inner_shape)


    inner_body = color("red")(inner_body)

    result = body-inner_body
    result += body_floor



    return result


if __name__ == '__main__':
    fractalLamp = kochLamp()
    # print(scad_render(fractalChrismasTree))

    # save your model for use in OpenSCAD
    fractalLamp.save_as_scad()
