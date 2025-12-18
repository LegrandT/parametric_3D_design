from solid2 import *
import math
import numpy as np

inner= circle(5.5, _fn = 72)
outer= circle(7.5, _fn = 72)


body = outer - inner
body = linear_extrude(9)(body)

cube_len = 10

opening = square(cube_len)
opening = linear_extrude(100)(opening)
opening = translate([-cube_len/2, -cube_len/2, -50])(opening)

opening = rotate([0, 0, 45])(opening)
opening = translate([5, 0, 0])(opening)

# opening = translate([0, 0, 1])(opening)

body = body - opening

scad_filename = 'shower_dongle2.scad'

body.save_as_scad(scad_filename)