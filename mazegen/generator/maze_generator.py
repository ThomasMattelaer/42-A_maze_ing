import random
from collections import deque
from typing import Deque


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
        entry_row, entry_col = (self._entry[0] * 2) + 1, \
            (self._entry[1] * 2) + 1
        exit_row, exit_col = (self._exit[0] * 2) + 1, (self._exit[1] * 2) + 1
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
                        (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (2, 5), (2, 4), (3, 4), (4, 4),
                        (4, 5), (4, 6)
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
                    (self._height * 2) - 1
                    and 0 < check_col < (self._width * 2) - 1
                    and maze[check_row][check_col] != 5)

        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = []
        pos = (oddNumber(1, (self._height * 2) - 1), oddNumber(1, (self._width * 2) - 1))
        print(pos)
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

    def solve(self, maze: list[list[int]]) -> str:
        directions = [
            ("N", (-1, 0), (-2, 0)),
            ("E", (0, 1), (0, 2)),
            ("S", (1, 0), (2, 0)),
            ("W", (0, -1), (0, -2)),
        ]

        entry_maze = self._entry
        exit_maze = self._exit
        coord_entry = ((entry_maze[0] * 2)+1, (entry_maze[1] * 2) + 1)
        coord_exit = ((exit_maze[0] * 2)+1, (exit_maze[1] * 2) + 1)

        deque_path = deque([coord_entry])
        came_from: dict[tuple[int, int],
                        tuple[int, int] | None] = {coord_entry: None}

        while deque_path:
            current: tuple[int, int] = deque_path.popleft()
            if current == coord_exit:
                break
            for letter, wall, cell in directions:
                wall_coord = (current[0] + wall[0], current[1] + wall[1])
                neighbor_coord = (current[0] + cell[0], current[1] + cell[1])
                if (maze[wall_coord[0]][wall_coord[1]] == 0
                        and neighbor_coord not in came_from):
                    came_from[neighbor_coord] = current
                    deque_path.append(neighbor_coord)
        print(came_from)
        path = []
        current = coord_exit
        while current != coord_entry:
            potential_previous = came_from[current]
            if isinstance(potential_previous, tuple):
                previous: tuple[int, int] = potential_previous
            print(f"previoous {previous}")

            if current[0] < previous[0]:
                path.append("N")
            elif current[0] > previous[0]:
                path.append("S")
            elif current[1] > previous[1]:
                path.append("E")
            else:
                path.append("W")
            curr_row, curr_col = current[0], current[1]
            if (current != coord_entry and current != coord_exit):
                maze[curr_row][curr_col] = 6
            current = previous
        path.reverse()
        return "".join(path)


def render_matrix(maze: list[list[int]]) -> None:

    chars = {
        0: '\x1b[38;5;231m██\x1b[0m',  # cellule
        1: '\x1b[38;5;24m██\x1b[0m',  # mur
        3: '\x1b[38;5;40m██\x1b[0m',  # entry
        4: '\x1b[38;5;196m██\x1b[0m',  # exit
        5: '\x1b[38;5;214m██\x1b[0m',  # 42
        6: '\x1b[38;5;202m██\x1b[0m',  # 42
    }
    for row in maze:
        line = ""
        for cell in row:
            line += chars[cell]
        print(line)


if __name__ == "__main__":

    maze = MazeGenerator(15, 15, (1, 3), (3, 5), "test", True)
    init = maze.init_maze()
    if (maze._width > 10):
        maze.setup42(init)
    maze.generate(init)
    str = maze.solve(init)
    print(str)
    render_matrix(init)
