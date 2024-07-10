#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import math
import json
from solid2 import *
import numpy as np

# Load the configuration from a JSON file
with open('config.json', 'r') as f:
    config = json.load(f)


class KochSnowflake_creator:
    def __init__(self, config_dict=None):
        self.chamfer_r = 0
        self.body = None
        self.set_config(config_dict)

    def set_config(self, config_dict=None):
        if config_dict is None:
            config_dict = {"height": 100, "base_diameter": 50, "koch_iterations": 3, "wall_thickness": 0.4, "height_per_layer": 2, "chamfer_r": 0}
        self.height = config_dict['height']
        self.base_diameter = config_dict['base_diameter']
        self.koch_iterations = config_dict['koch_iterations']
        self.wall_thickness = config_dict['wall_thickness']
        self.height_per_layer = config_dict['height_per_layer']
        self.chamfer_r = config_dict['chamfer_r']
        self.twists_list = []
        if "twists_list" in config_dict:
            self.twists_list = config_dict['twists_list']
        self.scaling_list = []
        if "scaling_list" in config_dict:
            self.scaling_list = config_dict['scaling_list']
        self.num_layers = int(self.height/self.height_per_layer)
        self.floor_layer = int(self.wall_thickness/self.height_per_layer)
        self._fn = 72

    def switch_config(self, config_name):
        self.set_config(config[config_name])

    def save_config(self, filename='config.json'):
        current_config = {
            "height": self.height,
            "base_diameter": self.base_diameter,
            "koch_iterations": self.koch_iterations,
            "wall_thickness": self.wall_thickness,
            "height_per_layer": self.height_per_layer,
            "chamfer_r": self.chamfer_r,
            "twists_list": self.twists_list,
            "scaling_list": self.scaling_list
        }
        with open(filename, 'a') as f:
            json.dump(current_config, f)

    def save_as_scad(self, filename=None):
        if self.body is None:
            print("No object to save")
            return
        if filename is None:
            self.body.save_as_scad(filename)
        else:
            scad_render_to_file(self.body, 'filename')

    def save_as_stl(self, filename=None):
        if self.body is None:
            print("No object to save")
            return
        if filename is not None:
            self.body.save_as_stl(filename)
        else:
            print("No filename provided")

    def get_sin_cos(self, function='sin', amplitude=1, period=1, phase=0, n_points=100, way = 'twist'):
        scaled_period = period/self.height_per_layer
        scaled_phase = phase/self.height_per_layer
        if way == 'twist':
            amplitude = amplitude*self.height_per_layer
        if way == 'scale':
            amplitude = amplitude*self.base_diameter/100
            n_points += 1
        if function == 'sin':
            return [amplitude * math.sin(2 * math.pi * i / scaled_period + 2*math.pi*scaled_phase/scaled_period) for i in range(n_points)]
        elif function == 'cos':
            return [amplitude * math.cos(2 * math.pi * i / scaled_period + 2*math.pi*scaled_phase/scaled_period) for i in range(n_points)]
        else:
            return None

    def get_line(self, twist, n_points, way='twist'):
        if twist['type'] == 'sin' or twist['type'] == 'cos':
            return self.get_sin_cos(function=twist['type'], amplitude=twist['amplitude'], period=twist['period'], phase=twist['phase'], n_points = n_points, way = way)
        if twist['type'] == 'total_scale':
            return [i/n_points*self.base_diameter*(twist['scale']-1) for i in range(n_points)]
        if twist['type'] == 'constant':
            return [i*twist['value']/self.num_layers for i in range(n_points)]

    def kochSnowflake(self, diameter=100, iterations=3):
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
        shape = self.kochSnowflake(diameter=self.base_diameter, iterations=self.koch_iterations)
        if self.chamfer_r > 0:
            shape = offset(r=-self.chamfer_r, _fn=self._fn)(shape)
            shape = offset(r=self.chamfer_r*2, _fn=self._fn)(shape)
            shape = offset(r=-self.chamfer_r, _fn=self._fn)(shape)

        body = None

        rota_list = [0]*self.num_layers
        scaling = [1]*self.num_layers

        if len(self.twists_list) > 0:
            rota_list = sum(np.array(self.get_line(t, self.num_layers, way="twist")) for t in self.twists_list)
        if len(self.scaling_list) > 0:
            scaling = sum(np.array(self.get_line(s, self.num_layers+1, way="scale")) for s in self.scaling_list)
            scaling = [(self.base_diameter+scaling[i+1]*2)/(self.base_diameter+scaling[i]*2) for i in range(self.num_layers)]
        hollow = False
        for i in range(self.num_layers):
            if i > self.floor_layer and not hollow:
                if self.chamfer_r > 0:
                    inner_shape = offset(r=-self.wall_thickness, _fn=self._fn)(shape)
                else:
                    inner_shape = offset(delta=-self.wall_thickness, _fn=self._fn)(shape)
                shape = shape-inner_shape
                hollow = True
            layer = linear_extrude(
                height=self.height_per_layer,
                scale=scaling[i],
                twist=-rota_list[i],
                slices=1,
            )(shape)
            layer = translate([0, 0, self.height_per_layer*i])(layer)
            if body:
                body += layer
            else:
                body = layer

            if i != self.num_layers-1:
                shape = rotate([0, 0, rota_list[i]])(shape)
                shape = scale([scaling[i], scaling[i], 1])(shape)

        self.body = body

if __name__ == '__main__':

    config_dict = {
        "height":100,
        "base_diameter":50,
        "koch_iterations":3,
        "wall_thickness":0.4,
        "height_per_layer":20,
        "chamfer_r":0,
        "twists_list":
        [
            # {
            #     "type":"sin",
            #     "amplitude":2,
            #     "period":100,
            #     "phase":0
            # }
        ],
        "scaling_list":
        [
            {
                "type":"cos",
                "amplitude":5,
                "period":100,
                "phase":50
            }
        ]
    }


    creator = KochSnowflake_creator(config_dict)
    # creator.switch_config('testing')
    creator.create()
    creator.save_as_scad()
    # stl_filename = 'kochLamp.stl'
    # creator.save_as_stl(stl_filename)
    # print(scad_render(fractalChrismasTree))

    # save your model for use in OpenSCAD
    # fractalLamp.save_as_scad()