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

    def init_maze(self) -> list[list[int]]:
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
        return matrix

    def setup42(self, maze: list[list[int]]) -> None:
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
        rows = len(maze)
        cols = len(maze[0])
        for r in range(1, rows - 1):
            for c in range(1, cols - 1):
                if maze[r][c] == 1:
                    if (maze[r-1][c] == 5 and maze[r+1][c] == 5) or \
                     (maze[r][c-1] == 5 and maze[r][c+1] == 5):
                        maze[r][c] = 5

    def generate(self, maze: list[list[int]]) -> None:
        """Generate all the path of the maze with the DFS algorithm"""

        def oddNumber(a: int, b: int) -> int:
            number = random.randint(a, b)
            while (number % 2 == 0):
                number = random.randint(a, b)
            return number

        def valid_direction(direction: tuple, pos: tuple,
                            visited: set[tuple[int, int]],
                            maze: list[list[int]]) -> bool:

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
                stack.pop()


def render_matrix(maze: list[list[int]]) -> None:

    chars = {
        0: '\x1b[38;5;37m██\x1b[0m',  # cellule
        1: '\x1b[38;5;24m██\x1b[0m',  # mur
        3: '\x1b[38;5;165m██\x1b[0m',  # entry
        4: '\x1b[38;5;196m██\x1b[0m',  # exit
        5: '\x1b[38;5;214m██\x1b[0m',  # 42
        6: '\x1b[48;5;37m\x1b[38;5;245m██\x1b[0m',  # Path
    }
    for row in maze:
        line = ""
        for cell in row:
            line += chars[cell]
        print(line)
