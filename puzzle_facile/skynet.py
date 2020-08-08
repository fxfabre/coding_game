import sys
import math
import numpy as np

def find_path(required_pos, required_speed, current_pos, current_speed, path):
    """ try to find if we can, from (current position, current speed)
    reach the required position at the required speed """
    if (required_pos == current_pos) and (required_speed == current_speed):
#        print("== Solution : " + str(path), file=sys.stderr)
        return path # ok, we have a solution
    if required_speed <= 0:
#        print("negative speed", file=sys.stderr)
        return -1
    if required_pos < current_pos:
#        print("negative position : {0} < {1}".format(required_pos, current_pos),
#            file=sys.stderr)
        return -1 # No path from current pos to get to required pos

    path.append( [required_pos, required_speed] )
#    print("path : " + str(path), file=sys.stderr)
    
    # find path, if we slow, keep speed or accelerate
    path_speed = find_path(required_pos - required_speed, required_speed+1,
        current_pos, current_speed, path.copy())
    path_wait = find_path(required_pos - required_speed, required_speed,
        current_pos, current_speed, path.copy())
    path_slow = find_path(required_pos - required_speed, required_speed-1,
        current_pos, current_speed, path.copy())
    
    # find best path
    best_path = -1
    for p in [path_slow, path_wait, path_speed]:
        if p == -1:
            continue
        if best_path == -1:
            best_path = p
        elif len(p) < len(best_path):
            best_path = p
    return best_path


road = int(input())  # the length of the road before the gap.
gap = int(input())  # the length of the gap.
platform = int(input())  # the length of the landing platform.
begin_platform = road + gap

required_speed = gap + 1
print("jump at " + str(road-1) , file=sys.stderr)

speed = int(input())    # initial speed
coord_x = int(input())  # initial position
best_path = find_path(road-1, required_speed, coord_x, speed, [])
print("best path : " + str(best_path), file=sys.stderr)


while 1:
    print("speed {0} at position {1}".format(speed, coord_x),
        file=sys.stderr)
    
    if coord_x >= road :
        print("SLOW")
    elif coord_x == road-1:
        print("JUMP")
    else:
        if len(best_path) > 0:
            next_step = best_path.pop()
            next_x    = next_step[0]
            next_speed= next_step[1]
            print("next : speed {0} at position {1}".format(next_speed, next_x),
                file=sys.stderr)
            
            if next_speed < speed:
                print("SLOW")
            elif next_speed == speed:
                print("WAIT")
            else:
                print("SPEED")
        else:
            print("ERROR ! Missing value in best_path", file=sys.stderr)
            print("WAIT") # ???????

    speed = int(input())  # the motorbike's speed.
    coord_x = int(input())  # the position on the road of the motorbike.




