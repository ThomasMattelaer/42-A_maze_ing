from collections import deque
from config import clear
from .maze_generator import render_maze
import time


def solve(entry: tuple[int, int], exit: tuple[int, int],
          maze: list[list[int]],
          path: bool = True, color_index: int = 0) -> str:
    """finding the best path thanks to the BSF algorithm"""
    directions = [
        ("N", (-1, 0), (-2, 0)),
        ("E", (0, 1), (0, 2)),
        ("S", (1, 0), (2, 0)),
        ("W", (0, -1), (0, -2)),
    ]

    entry_maze = entry
    exit_maze = exit
    coord_entry = ((entry_maze[1] * 2)+1, (entry_maze[0] * 2) + 1)
    coord_exit = ((exit_maze[1] * 2)+1, (exit_maze[0] * 2) + 1)

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
    path_solver = []
    current = coord_exit
    while current != coord_entry:
        potential_previous = came_from[current]
        if isinstance(potential_previous, tuple):
            previous: tuple[int, int] = potential_previous
        if current[0] < previous[0]:
            path_solver.append("N")
        elif current[0] > previous[0]:
            path_solver.append("S")
        elif current[1] > previous[1]:
            path_solver.append("E")
        else:
            path_solver.append("W")
        curr_row, curr_col = current[0], current[1]
        if (current != coord_entry and current != coord_exit):
            maze[curr_row][curr_col] = 6
        clear()
        render_maze(maze, path, color_index)
        time.sleep(0.02)
        current = previous
    path_solver.reverse()
    return "".join(path_solver)
