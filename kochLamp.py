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
        diameter=150,        # Diameter of tree at widest point
        height=150,         # Total height of tree
        base_diameter=100,   # Diameter of base Koch snowflake
        twist=90,       # Twist of tree base
        base_slices=200,      # Slices of base extrusion
        koch_iterations=3,  # iterations of Koch Snowflake
        ):

    snowflake = kochSnowflake(diameter=diameter, iterations=koch_iterations)
    body = linear_extrude(
                height=height,
                scale=diameter/base_diameter,
                twist=twist,
                slices=base_slices,
                convexity = 10,
                )(snowflake)

    inner_body = linear_extrude(
                height=height,
                scale=(diameter)/(base_diameter),
                twist=twist,
                slices=base_slices,
                convexity = 10,
                )(snowflake)

    inner_body = scale([0.7,0.7,1])(inner_body)


    result = body - inner_body

    cut = cylinder(d=diameter*2, h=5)
    cut = translate([0,0,height-5])(cut)

    result = result -cut

    return result

if __name__ == '__main__':
    fractalLamp = kochLamp()
    # print(scad_render(fractalChrismasTree))

    # save your model for use in OpenSCAD
    fractalLamp.save_as_scad()
