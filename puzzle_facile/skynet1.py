import sys
import math
import numpy as np

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

road = int(input())  # the length of the road before the gap.
gap = int(input())  # the length of the gap.
platform = int(input())  # the length of the landing platform.
begin_platform = road + gap

required_speed = gap + 1
print("Required speed : " + str(required_speed), file=sys.stderr)


current_speed = required_speed
current_position = road -1
while current_speed > 0:
    print("speed {0} at position {1}".format(current_speed, current_position),
        file=sys.stderr)
    current_position -= current_speed
    current_speed -= 1
begin_accel = current_position

print("begin accel : " + str(begin_accel), file=sys.stderr)
print("jump at " + str(road) , file=sys.stderr)


# game loop
while 1:
    speed = int(input())  # the motorbike's speed.
    coord_x = int(input())  # the position on the road of the motorbike.
    
    print("speed {0} at position {1}".format(speed, coord_x),
        file=sys.stderr)
    
    
    if coord_x <= begin_accel:
        if speed == 0 :
            print("SPEED")
        elif speed == 1 :
            print("WAIT")
        else :
            print("SLOW")
    elif coord_x < road -1 :
        print("SPEED")
    elif coord_x == road -1 :
        print("JUMP")
    else :
        print("SLOW")
    

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # A single line containing one of 4 keywords: SPEED, SLOW, JUMP, WAIT.
#    print("SPEED")

