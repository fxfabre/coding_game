# coding=utf-8

import sys
import math

"""
(9 * d) / 5 = time required to reach trafic light at distance d (in meters), speed 1 km/h
if light at distance d, with period T, is green when we arrive :
we can find n, integer, such as :
 n <=           9 d / 5 v T
 n >  -1 / 2 + (9 d / 5 v T)
so decimal_part(n) < 0.5

with :
 d : distance to the light in meters
 v : speed in km/h
 T : period of the light in seconds
"""

max_speed = int(input())
light_count = int(input())
lights = []

for i in range(light_count):
    d, T = [int(j) for j in input().split()]
    lights.append((T, (9 * d) / (5 * T)))

for v in range(max_speed, 0, -1):
    only_green_lights = True

    for T, s in lights:
        n = round(math.modf(s / v)[0], 10)
        if n >= 0.5:
            only_green_lights = False
            break

    if only_green_lights:
        break

print(v)
