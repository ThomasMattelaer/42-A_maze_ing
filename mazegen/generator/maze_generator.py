import random


class MazeGenerator():
    """Class that handle the generation of the maze"""

    def __init__(self,
                 height: int,
                 width: int,
                 entry: tuple[int, int],
                 exit: tuple[int, int],
                 output_file: str,
                 perfect: bool
                 ) -> None:

        self._height = height
        self._width = width
        self._entry = entry
        self._exit = exit
        self._output_file = output_file
        self._perfect = perfect

    # def draw_rectangle(self) -> None:
    #     color = random.randint(0, 256)
    #     print(f"\x1b[38;5;{color}m{chr(9581) + chr(9472) * (self._width * 2)}"
    #           + f"{chr(9582)}\x1b[0m")

    #     for i in range(self._height):
    #         print(f"\x1b[38;5;{color}m{chr(9474)}{' ' * (self._width * 2)}" +
    #               f"{chr(9474)}\x1b[0m")

    #     print(f"\x1b[38;5;{color}m{chr(9584) + chr(9472) * (self._width * 2)}"
    #           + f"{chr(9583)}\x1b[0m")
    def init_maze(self) -> list[list[int]]:
        matrix: list[list[int]] = []
        for row in range(self._height * 2 + 1):
            columns: list[int] = []
            for col in range(self._width * 2 + 1):
                if (col % 2 == 0 or row % 2 == 0):
                    columns.append(1)
                else:
                    columns.append(2)
            matrix.append(columns)
        return matrix

    def setup42(self, maze: list[list[int]]) -> None:
        height_42 = 6
        width_42 = 7

        PATTERN_42 = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2),
                      (3, 2), (4, 2), (5, 2),
                      (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (2, 5), (2, 4),
                      (3, 4), (4, 4), (5, 4), (5, 5), (5, 6)
                      ]
        start_row = round((self._height - height_42) / 2)
        start_col = round((self._width - width_42) / 2)
        print(f"height={self._height} width={self._width}")
        print(f"start_row={start_row} start_col={start_col}")
        for row, col in PATTERN_42:
            r = (start_row + row) * 2 + 1
            c = (start_col + col) * 2 + 1
            maze[r][c] = 5
        print(maze)


def get_corner(maze: list[list[int]], row: int, col: int) -> str:
    rows, cols = len(maze), len(maze[0])
    N, E, S, W = 1, 2, 4, 8

    on_top = row == 0
    on_bot = row == rows
    on_left = col == 0
    on_right = col == cols

    topl = maze[row-1][col-1] if row > 0 and col > 0 else None
    topr = maze[row-1][col] if row > 0 and col < cols else None
    bottoml = maze[row][col-1] if row < rows and col > 0 else None
    bottomr = maze[row][col] if row < rows and col < cols else None

    vert = (topl and topl & E) or (topr and topr & W) or \
           (bottoml and bottoml & E) or (bottomr and bottomr & W)

    horiz = (topl and topl & S) or (bottoml and bottoml & N) or \
            (topr and topr & S) or (bottomr and bottomr & N)

    if on_top and on_left:
        return '┌'
    if on_top and on_right:
        return '┐'
    if on_bot and on_left:
        return '└'
    if on_bot and on_right:
        return '┘'
    if on_top:
        if (vert):
            return '┬'
        return '───'
    if on_bot:
        if (vert):
            return '┴'
        return '───'
    if on_left:
        if (horiz):
            return '├'
        return '│'
    if on_right:
        if (horiz):
            return '┤'
        return '│'
    if (vert and horiz):
        return '┼'
    return "   "


def render_matrix(maze: list[list[int]]) -> None:

    chars = {
        1: '\x1b[38;5;16m███\x1b[0m',
        2: '\x1b[48;5;24m   \x1b[0m',
        5: '\x1b[38;5;200m███\x1b[0m',
    }
    for row in maze:
        print(''.join(chars[cell] for cell in row))


def render_tab(maze: list[list[int]]) -> None:
    rows = len(maze)
    cols = len(maze[0])
    color = random.randint(0, 256)

    for row in range(rows + 1):
        line = ""
        for col in range(cols + 1):
            line += get_corner(maze, row, col)
        print(f"\x1b[38;5;{color}m{line}\x1b[0m")

        if row < rows:
            line = ""
            for col in range(cols):
                if maze[row][col] & 8:
                    line += "│"
                else:
                    line += "   "

            if maze[row][cols - 1] & 2:
                line += "│"
            else:
                line += "   "
            print(line)


if __name__ == "__main__":

    maze = MazeGenerator(12, 15, (10, 2), (10, 2), "test", True)
    init = maze.init_maze()
    maze.setup42(init)
    render_matrix(init)
