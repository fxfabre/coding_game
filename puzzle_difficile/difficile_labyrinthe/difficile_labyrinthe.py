import sys
import numpy as np
np.set_printoptions(linewidth=150)

CELL_WALL = -10
CELL_EMPTY = -11
CELL_START = -12
CELL_CMD_ROOM = -13
CELL_UNKNOWN = -14

char_to_int = {
    '#' : CELL_WALL,
    '.' : CELL_EMPTY,
    'T' : CELL_START,
    'C' : CELL_CMD_ROOM,
    '?' : CELL_UNKNOWN
}


def read_line_file(fp):
    line = fp.readline().strip()
    print(line)
    return line


def read_line_input():
    line = input()
    debug(line)
    return line


def debug(msg : str, *args):
    print(msg % args, file=sys.stderr)


def print_funct_call(func):
    def _wrapper(*args, **kwargs):
        debug("Calling " + func.__name__)
        res = func(*args, **kwargs)
        debug("End " + func.__name__)
        return res
    return _wrapper


def main(get_line_func=read_line_input):
    # r: number of rows.
    # c: number of columns.
    # a: number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
    r_max, c_max, a = [int(i) for i in get_line_func().split()]
    found_cmd_room = False

    while True:
        kr, kc = [int(i) for i in get_line_func().split()]
        lab = Labyrinthe(r_max, c_max, kr, kc)
        lab.parse_labyrinthe(get_line_func)
        lab.propagate_distance_from_position_iter(kr, kc)
        found_cmd_room = found_cmd_room or (lab.current_position == lab.cmd_room)

        if found_cmd_room:
            lab.go_to_start()
        elif lab.position_nearest_unknown[0] > 0:
            lab.one_step_to_closest_unknown()
        elif lab.can_go_to_cmd_room:
            lab.try_go_to_cmd_room()
        else:
            lab.one_step_to_closest_unknown()


class Labyrinthe:
    def __init__(self, nb_row, nb_col, kr, kc):
        self.grid = np.zeros([nb_row + 2, nb_col + 2], dtype=int)
        self.nb_row = nb_row + 2
        self.nb_col = nb_col + 2
        self.start = (-1, -1)
        self.cmd_room = (-1, -1)
        self.current_position = (kr + 1, kc + 1)
        self.distance_nearest_unknown = 2 ^ 30
        self.position_nearest_unknown = (-1, -1)

    # @print_funct_call
    def parse_labyrinthe(self, get_line_func):
        for current_row in range(1, self.nb_row - 1):
            row = get_line_func()  # C of the characters in '#.TC?' (i.e. one line of the ASCII maze).
            current_col = 0
            for char in row:
                current_col += 1
                self.grid[current_row, current_col] = char_to_int[char]
                if char == 'C':
                    self.cmd_room = (current_row, current_col)
                if char == 'T':
                    self.start = (current_row, current_col)

        for row in range(0, self.nb_row):
            self.grid[row, 0              ] = CELL_WALL
            self.grid[row, self.nb_col - 1] = CELL_WALL

        for col in range(0, self.nb_col - 1):
            self.grid[0              , col] = CELL_WALL
            self.grid[self.nb_row - 1, col] = CELL_WALL

        debug("Current position : %s", self.current_position)
        debug("Start : %s", self.start)
        debug("Cmd room : %s", self.cmd_room)

    def propagate_distance_from_position(self, current_r, current_c):
        """
        Propagate from current_r, current_c to all the map
        """
        nb_moves = 0
        cells_to_propagate = [(current_r + 1, current_c + 1)]
        while len(cells_to_propagate) > 0:
            cells = cells_to_propagate
            cells_to_propagate = []
            nb_moves += 1

            for current_r, current_c in cells:
                if 0 < self.grid[current_r, current_c] < nb_moves:
                    # Cell already set with better value
                    pass
                elif self.grid[current_r, current_c] == CELL_WALL:
                    # print("Wall on", current_r, current_c)
                    pass
                elif self.grid[current_r, current_c] == CELL_UNKNOWN:
                    # print("Cell unknown at", current_r, current_c)
                    if nb_moves < self.distance_nearest_unknown:
                        self.distance_nearest_unknown = nb_moves
                        self.position_nearest_unknown = (current_r, current_c)
                else:
                    self.grid[current_r, current_c] = nb_moves

                    cells_to_propagate.append( (current_r, current_c - 1) )
                    cells_to_propagate.append( (current_r + 1, current_c) )
                    cells_to_propagate.append( (current_r - 1, current_c) )
                    cells_to_propagate.append( (current_r, current_c + 1) )

    def propagate_source_to_target(self, source_r, source_c, target_r, target_c):
        nb_moves = 0
        nb_max_moves = 500 * 500

        source_to_propagate = [(source_r, source_c)]
        target_to_propagate = [(target_r, target_c)]

        loop = True
        while loop and (len(source_to_propagate) + len(target_to_propagate) > 0):
            nb_moves += 1

            cells = source_to_propagate
            source_to_propagate = []
            for current_r, current_c in cells:
                if self.grid[current_r, current_c] > nb_max_moves / 2:
                    loop = False    # Joined the target cells
                elif 0 < self.grid[current_r, current_c]:
                    pass    # Cell already set with better value
                elif self.grid[current_r, current_c] in (CELL_WALL, CELL_UNKNOWN):
                    pass
                else:
                    self.grid[current_r, current_c] = nb_moves

                    source_to_propagate.append((current_r, current_c - 1))
                    source_to_propagate.append((current_r + 1, current_c))
                    source_to_propagate.append((current_r - 1, current_c))
                    source_to_propagate.append((current_r, current_c + 1))

            cells = target_to_propagate
            target_to_propagate = []
            for current_r, current_c in cells:
                if 0 < self.grid[current_r, current_c]:
                    if self.grid[current_r, current_c] < nb_max_moves / 2:
                        loop = False  # Joined the source cells
                    pass  # Cell already set with better value
                elif self.grid[current_r, current_c] in (CELL_WALL, CELL_UNKNOWN):
                    pass
                else:
                    self.grid[current_r, current_c] = nb_max_moves - nb_moves

                    target_to_propagate.append((current_r, current_c - 1))
                    target_to_propagate.append((current_r + 1, current_c))
                    target_to_propagate.append((current_r - 1, current_c))
                    target_to_propagate.append((current_r, current_c + 1))

        return nb_moves

    # @print_funct_call
    def try_go_to_cmd_room(self, out_func=print):
        debug("Go to cnd room")

        move = 'unknown_move'
        current_row, current_col = self.cmd_room
        current_value = self.grid[current_row, current_col]

        while current_value > 1:
            if 0 < self.grid[current_row - 1, current_col] < current_value:
                current_row -= 1
                move = 'DOWN'
            elif 0 < self.grid[current_row, current_col - 1] < current_value:
                current_col -= 1
                move = 'RIGHT'
            elif 0 < self.grid[current_row + 1, current_col] < current_value:
                current_row += 1
                move = 'UP'
            elif 0 < self.grid[current_row, current_col + 1] < current_value:
                current_col += 1
                move = 'LEFT'
            else:
                debug("go_to_cmd_room : Unable to find better value that %s %s %s", current_value, current_row, current_col)
                return self.current_position == self.cmd_room
            current_value = self.grid[current_row, current_col]

        out_func(move)
        return True

    # @print_funct_call
    def one_step_to_closest_unknown(self, out_func=print):
        debug("Go to unknown cell")

        move = 'unknown_move'
        current_row, current_col = self.position_nearest_unknown
        current_value = self.distance_nearest_unknown

        while current_value > 1:
            if 0 < self.grid[current_row - 1, current_col] < current_value:
                current_row -= 1
                move = 'DOWN'
            elif 0 < self.grid[current_row, current_col - 1] < current_value:
                current_col -= 1
                move = 'RIGHT'
            elif 0 < self.grid[current_row + 1, current_col] < current_value:
                current_row += 1
                move = 'UP'
            elif 0 < self.grid[current_row, current_col + 1] < current_value:
                current_col += 1
                move = 'LEFT'
            else:
                debug("to_closest_unknown : Unable to find better value that %s %s %s",
                      current_value, current_row, current_col)
                return self.current_position == self.cmd_room

            current_value = self.grid[current_row, current_col]

        out_func(move)

    # @print_funct_call
    def go_to_start(self, out_func=print):
        debug("Go to start")

        move = 'unknown_move'
        current_row, current_col = self.start
        current_value = self.grid[current_row, current_col]

        while current_value > 1:
            if 0 < self.grid[current_row - 1, current_col] < current_value:
                current_row -= 1
                move = 'DOWN'
            elif 0 < self.grid[current_row, current_col - 1] < current_value:
                current_col -= 1
                move = 'RIGHT'
            elif 0 < self.grid[current_row + 1, current_col] < current_value:
                current_row += 1
                move = 'UP'
            elif 0 < self.grid[current_row, current_col + 1] < current_value:
                current_col += 1
                move = 'LEFT'
            else:
                debug("to_start : Unable to find better value that %s %s %s",
                      current_value, current_row, current_col)
                return self.current_position == self.cmd_room

            current_value = self.grid[current_row, current_col]

        out_func(move)

    @property
    def can_see_cmd_room(self):
        return self.cmd_room[0] > 0

    @property
    def can_go_to_cmd_room(self):
        cmd_room_r, cmd_room_c = self.cmd_room
        return self.can_see_cmd_room and (self.grid[cmd_room_r, cmd_room_c] > 0)

    def __str__(self):
        return str(self.grid)


if __name__ == '__main__':
    main()
