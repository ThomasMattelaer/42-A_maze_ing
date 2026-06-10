import random
from config import clear
import time


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
        if seed is not None:
            random.seed(seed)

    def init_maze(self) -> list[list[int]]:
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
        entry_row, entry_col = (self._entry[0] * 2) + 1, \
            (self._entry[1] * 2) + 1
        exit_row, exit_col = (self._exit[1] * 2) + 1, (self._exit[0] * 2) + 1
        matrix[entry_row][entry_col] = 3
        matrix[exit_row][exit_col] = 4
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
        render_maze(maze)

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

    def generate_path(self, maze: list[list[int]]) -> None:
        """Generate all the path of the maze with the DFS algorithm"""

        def oddNumber(a: int, b: int) -> int:
            """function to only have odd number"""
            number = random.randint(a, b)
            while (number % 2 == 0):
                number = random.randint(a, b)
            return number

        def valid_direction(direction: tuple, pos: tuple,
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
            directions: list[tuple] = [(0, 1), (0, -1), (1, 0), (-1, 0)]
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
            render_maze(maze)
            time.sleep(0.03)


def render_maze(maze: list[list[int]]) -> None:
    """"print the matrix"""

    chars = {
        0: '\x1b[38;5;37m██\x1b[0m',  # cellule
        1: '\x1b[38;5;24m██\x1b[0m',  # mur
        3: '\x1b[38;5;165m██\x1b[0m',  # entry
        4: '\x1b[38;5;196m██\x1b[0m',  # exit
        5: '\x1b[38;5;214m██\x1b[0m',  # 42
        6: '\x1b[38;5;245m██\x1b[0m',  # Path
    }
    for row in maze:
        line = ""
        for cell in row:
            line += chars[cell]
        print(f"{line}")
    print("""1. Re-generate the maze
2. Hide/Show the ideal path
3. Change the color of the maze
4. Leave the game
          """)


def generate_maze(maze_class: MazeGenerator) -> list[list[int]]:
    """a function to help to gather all the utils to generate the maze"""

    maze: list[list[int]] = maze_class.init_maze()
    if (maze_class._width > 10):
        maze_class.setup42(maze)
    maze_class.generate_path(maze)
    return maze
