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

    def fulfill42(self, maze: list[list[int]]) -> None:
        rows = len(maze)
        cols = len(maze[0])
        for r in range(1, rows - 1):
            for c in range(1, cols - 1):
                if maze[r][c] == 1:  # c'est un mur
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
                            visited: set[tuple[int, int]]) -> bool:
            check_row, check_col = pos[0] + 2 * direction[0], pos[1] + 2 * direction[1]
            check_pos: tuple[int, int] = (check_row, check_col)
            return (check_pos not in visited and 0 < check_row <
                    self._height - 1 and 0 < check_col < self._width - 1)

        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = []
        pos = (oddNumber(1, self._height - 1), oddNumber(1, self._width - 1))
        stack.append(pos)
        visited.add(pos)
        while (len(stack) > 0):
            pos = stack[-1]
            print(visited)
            directions: list[tuple] = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            valid_directions = [
                direction for direction in directions
                if valid_direction(direction, pos, visited)
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
        print(maze)


def render_matrix(maze: list[list[int]]) -> None:

    chars = {
        0: '\x1b[38;5;25m██\x1b[0m',
        1: '\x1b[38;5;16m██\x1b[0m',
        2: '\x1b[48;5;24m  \x1b[0m',
        5: '\x1b[48;5;220m  \x1b[0m',
    }
    for row in maze:
        line = ""
        for cell in row:
            line += chars[cell]
        print(line)


if __name__ == "__main__":

    maze = MazeGenerator(15, 15, (10, 2), (10, 2), "test", True)
    init = maze.init_maze()
    if (maze._width > 10):
        maze.setup42(init)
    maze.generate(init)
    render_matrix(init)
