import random
import time
from config import clear


class MazeGenerator():
    """Class that handle the generation of the maze"""

    def __init__(self,
                 height: int,
                 width: int,
                 entry: tuple[int, int],
                 exit: tuple[int, int],
                 output_file: str,
                 perfect: bool,
                 seed: int | None = None
                 ) -> None:

        self._height = height
        self._width = width
        self._entry = entry
        self._exit = exit
        self._output_file = output_file
        self._perfect = perfect
        self._seed = seed
        if seed is not None:
            random.seed(seed)

    def init_maze(self, color_index: int = 0) -> list[list[int]]:
        """Inititate a 2 dimensions matrix with one entry, one exit walls and
        cells

        Returns: a 2d matrix.
        """

        matrix: list[list[int]] = []
        for row in range(self._height * 2 + 1):
            columns: list[int] = []
            for col in range(self._width * 2 + 1):
                if (col % 2 == 0 or row % 2 == 0):
                    columns.append(1)
                else:
                    columns.append(0)
            matrix.append(columns)
        entry_row, entry_col = (self._entry[1] * 2) + 1, \
            (self._entry[0] * 2) + 1
        exit_row, exit_col = (self._exit[1] * 2) + 1, (self._exit[0] * 2) + 1
        matrix[entry_row][entry_col] = 3
        matrix[exit_row][exit_col] = 4
        clear()
        render_maze(matrix, True, color_index)
        return matrix

    def setup42(self, maze: list[list[int]]) -> None:
        """place the '42' pattern at the center of the maze.

        Args: maze is the matrix that we've initiliaze in the init function.
        """
        height_42 = 5
        width_42 = 7

        PATTERN_42 = [  # 4
                        (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2),
                        (3, 2), (4, 2),
                        # 2
                        (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (2, 5), (2, 4),
                        (3, 4), (4, 4), (4, 5), (4, 6)
                      ]
        start_row = round((self._height - height_42) / 2)
        start_col = round((self._width - width_42) / 2)
        for row, col in PATTERN_42:
            r = (start_row + row) * 2 + 1
            c = (start_col + col) * 2 + 1
            maze[r][c] = 5
        self.fulfill42(maze)

    def fulfill42(self, maze: list[list[int]]) -> None:
        """Adjust the color of the walls in between of the the 42 pattern"""
        rows = len(maze)
        cols = len(maze[0])
        for r in range(1, rows - 1):
            for c in range(1, cols - 1):
                if maze[r][c] == 1:
                    if (maze[r-1][c] == 5 and maze[r+1][c] == 5) or \
                     (maze[r][c-1] == 5 and maze[r][c+1] == 5):
                        maze[r][c] = 5

    def generate_path(self, maze: list[list[int]], path: bool = True,
                      color_index: int = 0) -> None:
        """Generate all the path of the maze with the DFS algorithm"""

        if self._seed is not None:
            random.seed(self._seed)

        def oddNumber(a: int, b: int) -> int:
            """function to only have odd number"""
            number = random.randint(a, b)
            while (number % 2 == 0):
                number = random.randint(a, b)
            return number

        def valid_direction(direction: tuple[int, int], pos: tuple[int, int],
                            visited: set[tuple[int, int]],
                            maze: list[list[int]]) -> bool:
            """valid direction that are possible from a certain
            position in the matrix"""

            check_row, check_col = pos[0] + 2 * direction[0], \
                pos[1] + 2 * direction[1]
            check_pos: tuple[int, int] = (check_row, check_col)
            return (check_pos not in visited and 0 < check_row <
                    (self._height * 2)
                    and 0 < check_col < (self._width * 2)
                    and maze[check_row][check_col] != 5)

        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = []
        pos = (oddNumber(1, (self._height * 2) - 1),
               oddNumber(1, (self._width * 2) - 1))
        stack.append(pos)
        visited.add(pos)
        while (len(stack) > 0):
            pos = stack[-1]
            directions: list[tuple[int, int]] = [
                (0, 1), (0, -1), (1, 0), (-1, 0)
                ]
            valid_directions = [
                direction for direction in directions
                if valid_direction(direction, pos, visited, maze)
            ]
            if (valid_directions):
                direction = random.choice(valid_directions)
                maze[pos[0] + direction[0]][pos[1] + direction[1]] = 0
                new_pos = ((pos[0] + direction[0] * 2),
                           (pos[1] + direction[1] * 2))
                stack.append(new_pos)
                visited.add(new_pos)
            else:
                if ((not self._perfect) and (random.random() < 0.15)):
                    random_dir = random.choice(directions)
                    row = pos[0] + random_dir[0]
                    col = pos[1] + random_dir[1]
                    if (0 < row < (self._height * 2)
                        and 0 < col < (self._width * 2)
                            and maze[row][col] != 5):
                        maze[row][col] = 0
                stack.pop()
            clear()
            render_maze(maze, path, color_index)
            time.sleep(0.01)


def generate_maze(maze_class: MazeGenerator,
                  path: bool = True, color_index: int = 0) -> list[list[int]]:
    """a function to help to gather all the utils to generate the maze"""

    maze: list[list[int]] = maze_class.init_maze(color_index)
    if (maze_class._width > 10):
        maze_class.setup42(maze)
    maze_class.generate_path(maze, path, color_index)
    return maze


COLORS = [
    # [cellule, mur, entry, exit, 42, path]
    [37,  24,  165, 196, 220, 245],
    [175, 161, 165, 196, 10,  11],
    [135, 90,  165, 196, 29,  95],
    [244, 232, 165, 196, 1,   3],
    [208, 94,  165, 196, 45,  230],
]


def make_block(color: int) -> str:
    """Create a block to display the maze
    Args: a number between 0 and 256
    Returns: the string to display with the ansicode
    """
    return f"\x1b[38;5;{color}m██\x1b[0m"


def mapping_color(path: bool, color_index: int) -> dict[int, str]:
    """help to create the correct set of function for the correct type block
    Args: path is true or false to show or not the path, color_index define
      which set of color
    Returns: a dict with the type of block as a int and the str to display
    """
    color = COLORS[color_index]
    mapping = {
        0: make_block(color[0]),
        1: make_block(color[1]),
        3: make_block(color[2]),
        4: make_block(color[3]),
        5: make_block(color[4]),
    }

    if (path):
        mapping[6] = make_block(color[5])
    else:
        mapping[6] = make_block(color[0])

    return mapping


def render_maze(maze: list[list[int]], path: bool,
                color_index: int = 0) -> None:
    """"print the matrix
    Args: maze, a 2d matrix, path is a bool to display or not, color_index
      define the set of color
    """

    chars = mapping_color(path, color_index)
    for row in maze:
        line = ""
        for cell in row:
            line += chars[cell]
        print(f"{line}")
    print("\n1. Re-generate the maze")
    print("2. Hide/Show the ideal path")
    print("3. Change the color of the maze")
    print("4. Leave the game\n")
