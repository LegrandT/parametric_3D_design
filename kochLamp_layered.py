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
        height=100,         # Total height of tree
        base_diameter=50,   # Diameter of base Koch snowflake
        koch_iterations=3,  # iterations of Koch Snowflake
        wall_thickness=0.4,  # Thickness of walls
        height_per_layer=2,  # Height of each layer
        chamfer_r = 0
        ):

    num_layers = int(height/height_per_layer)
    floor_layer = int(wall_thickness/height_per_layer)


    _fn = 72

    shape = kochSnowflake(diameter=base_diameter, iterations=koch_iterations)
    shape = offset(r=-chamfer_r, _fn=_fn)(shape)
    shape = offset(r=chamfer_r*2, _fn=_fn)(shape)
    shape = offset(r=-chamfer_r, _fn=_fn)(shape)

    body = None
    # # rota_list = [2]*(num_layers)
    # rota_list = [2 * math.sin(math.pi * i / num_layers) for i in range(num_layers)]


    # # Parameters
    # amplitude = 10 # hight of the curve
    # period = 10 # width of the curve
    # frequency = 2 * math.pi / period # frequency of the curve
    # phase = 0 # shift the curve to the right
        # rota_list = [2]*(num_layers)

    # TODO add scale with layer
    # Parameters
    amplitude = 2 # hight of the curve
    period = 100/height_per_layer # width of the curve
    frequency = 2 * math.pi / period # frequency of the curve
    phase = 0 # shift the curve to the right
    rota_list = [amplitude * math.sin(frequency * i + phase) for i in range(num_layers)]

    # Parameters
    amplitude = 5 # hight of the curve
    period = 100/height_per_layer # width of the curve
    frequency = 2 * math.pi / period # frequency of the curve
    phase = 0 # shift the curve to the right
    scaling = [1.00]*(num_layers)
    scaling = [amplitude * math.cos(frequency * x + phase) for x in range(num_layers+1)]
    scaling = [(base_diameter+scaling[i]*2)/(base_diameter+scaling[i+1]*2) for i in range(num_layers)]

    hollow = False
    for i in range(num_layers):
        if i>floor_layer and not hollow:
            if chamfer_r > 0:
                inner_shape = offset(r=-wall_thickness, _fn=_fn)(shape)
            else:
                inner_shape = offset(delta=-wall_thickness, _fn=_fn)(shape)
            # inner_shape = offset(r=-wall_thickness, _fn=_fn)(shape)
            shape = shape-inner_shape
            hollow = True
        layer = linear_extrude(
            height=height_per_layer,
            scale=scaling[i],
            twist=-rota_list[i],
            slices=1,
        )(shape)
        layer = translate([0,0,height_per_layer*i])(layer)
        if body:
            body += layer
        else:
            body = layer

        if i!=num_layers-1:
            shape = rotate([0,0,rota_list[i]])(shape)
            shape = scale([scaling[i], scaling[i], 1])(shape)

    result = body

    return result


if __name__ == '__main__':
    fractalLamp = kochLamp()
    # print(scad_render(fractalChrismasTree))

    # save your model for use in OpenSCAD
    fractalLamp.save_as_scad()
