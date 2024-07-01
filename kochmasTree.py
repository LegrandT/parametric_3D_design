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

def kochmasTree(
        diameter=100,        # Diameter of tree at widest point
        height=150,         # Total height of tree
        top_twist=180,      # Rotation in top part of tree
        base_diameter=50,   # Diameter of base Koch snowflake
        base_height=25,     # Height of tree base
        base_twist=0,       # Twist of tree base
        top_slices=100,     # Slices of top of tree extrusion
        base_slices=2,      # Slices of base extrusion
        koch_iterations=3,  # iterations of Koch Snowflake
        ):
    snowflake = kochSnowflake(diameter=diameter, iterations=koch_iterations)
    base_snowflake = kochSnowflake(diameter=base_diameter, iterations=koch_iterations)
    trunk = linear_extrude(
                height=base_height,
                scale=diameter/base_diameter,
                twist=base_twist,
                slices=base_slices,
                )(base_snowflake)
    top = linear_extrude(
                height=height-base_height,
                scale=0,  # Ends in a point
                slices=top_slices,
                twist=top_twist,
                )(snowflake)
    top = translate([0,0,base_height])(top)  # Put top over base

    tree = union()(top, trunk)
    return tree

if __name__ == '__main__':
    fractalChrismasTree = kochmasTree()
    # print(scad_render(fractalChrismasTree))

    # save your model for use in OpenSCAD
    fractalChrismasTree.save_as_scad()
