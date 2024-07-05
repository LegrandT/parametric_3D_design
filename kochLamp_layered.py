#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import math
import json
from solid2 import *

# Load the configuration file
# config = configparser.ConfigParser()
# config.read('config.ini')

# # Get the values from the configuration file
# height = config.getint('Lamp', 'height')
# base_diameter = config.getint('Lamp', 'base_diameter')
# koch_iterations = config.getint('Lamp', 'koch_iterations')
# wall_thickness = config.getfloat('Lamp', 'wall_thickness')
# height_per_layer = config.getfloat('Lamp', 'height_per_layer')
# chamfer_r = config.getfloat('Lamp', 'chamfer_r')

# Rest of your code...

# Load the configuration from a JSON file
with open('config.json', 'r') as f:
    config = json.load(f)


class KochSnowflake_creator:
    def __init__(self, diameter=100, iterations=3):
        self.diameter = diameter
        self.iterations = iterations
        self.wall_thickness=0.4,  # Thickness of walls
        self.height_per_layer=2,  # Height of each layer
        self.chamfer_r = 0
        self.body = None
        self.num_layers = int(height/height_per_layer)
        self.floor_layer = int(wall_thickness/height_per_layer)

    def get_config(self):
        return config

    def set_config(self, config_dict):
        self.height = config_dict['height']
        self.base_diameter = config_dict['base_diameter']
        self.koch_iterations = config_dict['koch_iterations']
        self.wall_thickness = config_dict['wall_thickness']
        self.height_per_layer = config_dict['height_per_layer']
        self.chamfer_r = config_dict['chamfer_r']


    def switch_config(self, config_name):
        # Get the values from the configuration
        self.height = config[config_name]['height']
        self.base_diameter = config[config_name]['base_diameter']
        self.koch_iterations = config[config_name]['koch_iterations']
        self.wall_thickness = config[config_name]['wall_thickness']
        self.height_per_layer = config[config_name]['height_per_layer']
        self.chamfer_r = config[config_name]['chamfer_r']

    def get_sin_cos(self, function='sin', amplitude=1, period=1, phase=0):
        if function == 'sin':
            return [amplitude * math.sin(2 * math.pi * i / period + phase) for i in range(self.num_layers)]
        elif function == 'cos':
            return [amplitude * math.cos(2 * math.pi * i / period + phase) for i in range(self.num_layers)]
        else:
            return None

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


    def create(self):
        num_layers = int(height/height_per_layer)
        floor_layer = int(wall_thickness/height_per_layer)


        _fn = 72

        shape = self.kochSnowflake(diameter=base_diameter, iterations=koch_iterations)
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
        amplitude = 2 # height of the curve
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

        self.body = body

    def save_as_scad(self, filename=None):
        if self.body is None:
            print("No object to save")
            return
        if filename is None:
            fractalLamp.save_as_scad(filename)
        else:
            scad_render_to_file(fractalLamp, 'filename')

def get_config():

    return config

# Get the values from the configuration
height = config['Lamp']['height']
base_diameter = config['Lamp']['base_diameter']
koch_iterations = config['Lamp']['koch_iterations']
wall_thickness = config['Lamp']['wall_thickness']
height_per_layer = config['Lamp']['height_per_layer']
chamfer_r = config['Lamp']['chamfer_r']


# def kochSnowflake(diameter=100, iterations=3):
#     rad = diameter/2
#     xrad = rad*math.sqrt(3)/2
#     yrad = rad/2
#     # Make an equilateral triangle with circumradius=rad
#     koch = [polygon([(0,rad), (-xrad, -yrad), (xrad, -yrad)])]
#     # Rotate triangle and union to make hexagram
#     hexagram = union()(koch[0], rotate(60)(koch[0]))
#     koch.append(hexagram)
#     if iterations < 2:
#         return koch[iterations]
#     for level in range(1, iterations):  # indicates level we are building from
#         shape = koch[level]
#         for i in range(6):
#             shape = union()(
#                 rotate(60)(shape),
#                 translate([0,rad*2/3,0])(scale(1/3)(koch[level])),
#                 )
#         koch.append(shape)
#     return koch[-1]

# def kochLamp(
#         height=100,         # Total height of tree
#         base_diameter=50,   # Diameter of base Koch snowflake
#         koch_iterations=3,  # iterations of Koch Snowflake
#         wall_thickness=0.4,  # Thickness of walls
#         height_per_layer=2,  # Height of each layer
#         chamfer_r = 0
#         ):

#     num_layers = int(height/height_per_layer)
#     floor_layer = int(wall_thickness/height_per_layer)


#     _fn = 72

#     shape = kochSnowflake(diameter=base_diameter, iterations=koch_iterations)
#     shape = offset(r=-chamfer_r, _fn=_fn)(shape)
#     shape = offset(r=chamfer_r*2, _fn=_fn)(shape)
#     shape = offset(r=-chamfer_r, _fn=_fn)(shape)

#     body = None
#     # # rota_list = [2]*(num_layers)
#     # rota_list = [2 * math.sin(math.pi * i / num_layers) for i in range(num_layers)]


#     # # Parameters
#     # amplitude = 10 # hight of the curve
#     # period = 10 # width of the curve
#     # frequency = 2 * math.pi / period # frequency of the curve
#     # phase = 0 # shift the curve to the right
#         # rota_list = [2]*(num_layers)

#     # TODO add scale with layer
#     # Parameters
#     amplitude = 2 # hight of the curve
#     period = 100/height_per_layer # width of the curve
#     frequency = 2 * math.pi / period # frequency of the curve
#     phase = 0 # shift the curve to the right
#     rota_list = [amplitude * math.sin(frequency * i + phase) for i in range(num_layers)]

#     # Parameters
#     amplitude = 5 # hight of the curve
#     period = 100/height_per_layer # width of the curve
#     frequency = 2 * math.pi / period # frequency of the curve
#     phase = 0 # shift the curve to the right
#     scaling = [1.00]*(num_layers)
#     scaling = [amplitude * math.cos(frequency * x + phase) for x in range(num_layers+1)]
#     scaling = [(base_diameter+scaling[i]*2)/(base_diameter+scaling[i+1]*2) for i in range(num_layers)]

#     hollow = False
#     for i in range(num_layers):
#         if i>floor_layer and not hollow:
#             if chamfer_r > 0:
#                 inner_shape = offset(r=-wall_thickness, _fn=_fn)(shape)
#             else:
#                 inner_shape = offset(delta=-wall_thickness, _fn=_fn)(shape)
#             # inner_shape = offset(r=-wall_thickness, _fn=_fn)(shape)
#             shape = shape-inner_shape
#             hollow = True
#         layer = linear_extrude(
#             height=height_per_layer,
#             scale=scaling[i],
#             twist=-rota_list[i],
#             slices=1,
#         )(shape)
#         layer = translate([0,0,height_per_layer*i])(layer)
#         if body:
#             body += layer
#         else:
#             body = layer

#         if i!=num_layers-1:
#             shape = rotate([0,0,rota_list[i]])(shape)
#             shape = scale([scaling[i], scaling[i], 1])(shape)

#     result = body

#     return result


if __name__ == '__main__':
    # fractalLamp = kochLamp(
    #     height=height,
    #     base_diameter=base_diameter,
    #     koch_iterations=koch_iterations,
    #     wall_thickness=wall_thickness,
    #     height_per_layer=height_per_layer,
    #     chamfer_r=chamfer_r
    #     )
    creator = KochSnowflake_creator()

    creator.create()
    creator.save_as_scad()
    # print(scad_render(fractalChrismasTree))

    # save your model for use in OpenSCAD
    # fractalLamp.save_as_scad()
