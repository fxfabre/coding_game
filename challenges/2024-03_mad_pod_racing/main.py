import sys
import math


while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # You have to output the target position "x y thrust"
    if abs(next_checkpoint_angle) >= 90:
        thrust = 5
    else:
        thrust = min(95, next_checkpoint_dist // 10) + 5
    print(f"{next_checkpoint_x} {next_checkpoint_y} {thrust}")
