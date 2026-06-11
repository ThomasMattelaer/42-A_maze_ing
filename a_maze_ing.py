import sys
import random
from mazegen import MazeGenerator, solve, render_maze, generate_maze, COLORS
from mazegen import write_output
from config import clear, get_key, parsing_main, move_entry


def generate(maze_class: MazeGenerator, path: bool = True,
             color_index: int = 0) -> list[list[int]]:
    maze = generate_maze(maze_class, path)
    path_solver = solve(maze_class._entry, maze_class._exit, maze,
                        path, color_index)
    write_output(maze, maze_class._entry, maze_class._exit, path_solver)
    return maze


def extend_tuple(tuple: tuple[int, int]) -> tuple[int, int]:
    """Double the tuple to fit the 2d matrix

       Args: a tuple of int

       Returns: a tuple of int
    """
    row, col = tuple
    new_row, new_col = (row * 2) + 1, (col * 2) + 1
    return new_row, new_col


def handle_input(
        maze_class: MazeGenerator, maze: list[list[int]],
        entry: tuple, color_index: int, path: bool
        ) -> tuple[bool, list[list[int]], tuple[int, int], int, bool]:
    key = get_key()
    if (key == "1"):
        clear()
        maze = generate(maze_class, path, color_index)
        entry = extend_tuple(maze_class._entry)
    elif (key == "2"):
        clear()
        path = not path
        print(path)
        render_maze(maze, path, color_index)
    elif (key == "3"):
        new_index = random.randint(0, len(COLORS) - 1)
        while new_index == color_index:
            new_index = random.randint(0, len(COLORS) - 1)
        color_index = new_index
        clear()
        render_maze(maze, path, color_index)
    elif (key == "a"):
        clear()
        entry = move_entry(maze, entry, (0, -1))
        render_maze(maze, path, color_index)
    elif (key == "d"):
        clear()
        entry = move_entry(maze, entry, (0, 1))
        render_maze(maze, path, color_index)
    elif (key == "w"):
        clear()
        entry = move_entry(maze, entry, (-1, 0))
        render_maze(maze, path, color_index)
    elif (key == "s"):
        clear()
        entry = move_entry(maze, entry, (1, 0))
        render_maze(maze, path, color_index)
    elif (key == "4"):
        return False, maze, entry, color_index, path
    else:
        return True, maze, entry, color_index, path
    return True, maze, entry, color_index, path


if __name__ == "__main__":
    print("A-MAZE-ING !")
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        raise SystemExit(1)
    config_file = sys.argv[1]
    config = parsing_main(config_file)
    output_file = config["OUTPUT_FILE"]
    width = int(config["WIDTH"])
    height = int(config["HEIGHT"])
    entry_x = int(config["ENTRY"].split(",")[0])
    entry_y = int(config["ENTRY"].split(",")[1])
    entry = (entry_x, entry_y)
    exit_x = int(config["EXIT"].split(",")[0])
    exit_y = int(config["EXIT"].split(",")[1])
    exit = (exit_x, exit_y)
    perfect = config["PERFECT"] == "True"
    maze_class = MazeGenerator(height, width, entry, exit, output_file,
                               perfect)
    clear()
    maze = generate(maze_class, True)
    color_index = 0
    handle = True
    pos = extend_tuple(entry)
    path = True
    while (handle):
        handle, maze, pos, color_index, \
            path = handle_input(maze_class, maze, pos, color_index, path)
