# coding=utf-8

# w: width of the building.
# h: height of the building.
w, h = [int(i) for i in input().split()]
n = int(input())  # maximum number of turns before game over.
x, y = [int(i) for i in input().split()]

min_y = 0
max_y = h
min_x = 0
max_x = w

# game loop
while True:
    bomb_dir = input()  # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)

    if 'L' in bomb_dir:
        max_x = x
    elif 'R' in bomb_dir:
        min_x = x
    else:
        min_x = x
        max_x = x

    if 'U' in bomb_dir:
        max_y = y
    elif 'D' in bomb_dir:
        min_y = y
    else:
        min_y = y
        max_y = y

    x = (min_x + max_x) // 2
    y = (min_y + max_y) // 2

    print(x, y)
