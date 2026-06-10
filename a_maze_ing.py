from mazegen import MazeGenerator, solve, render_maze, generate_maze
from mazegen import write_output
from config import clear, parsing_config, get_key, move_entry


def generate(maze_class: MazeGenerator) -> list[list[int]]:
    maze = generate_maze(maze_class)
    path = solve((1, 3), (13, 13), maze)
    solve(maze_class._entry, maze_class._exit, maze)
    write_output(maze, (1, 3), (13, 13), path)
    render_maze(maze)
    return maze


def handle_input(maze_class: MazeGenerator, maze: list[list[int]],
                 entry: tuple) -> tuple[bool,
                                        list[list[int]],
                                        tuple[int, int]]:
    key = get_key()
    if (key == "1"):
        clear()
        maze = generate(maze_class)
    elif (key == "3"):
        clear()
        render_maze(maze)
    elif (key == "a"):
        clear()
        entry = move_entry(maze, entry, (-1, 0))
        render_maze(maze)
    elif (key == "d"):
        clear()
        entry = move_entry(maze, entry, (1, 0))
        render_maze(maze)
    elif (key == "w"):
        clear()
        entry = move_entry(maze, entry, (0, -1))
        render_maze(maze)
    elif (key == "s"):
        clear()
        entry = move_entry(maze, entry, (0, 1))
        render_maze(maze)
    elif (key == "4"):
        return False, maze, entry
    else:
        return True, maze, entry
    return True, maze, entry


if __name__ == "__main__":
    print("A-MAZE-ING !")
    # config dict
    # parsing_config()
    maze_class = MazeGenerator(15, 15, (1, 3), (13, 13), "test", False)
    clear()
    maze = generate(maze_class)
    handle = True
    pos = ((1 * 2) + 1, (3 * 2) + 1)
    while (handle):
        handle, maze, pos = handle_input(maze_class, maze, pos)
