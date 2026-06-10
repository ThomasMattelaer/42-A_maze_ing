from mazegen import MazeGenerator, solve, render_maze, generate_maze
from mazegen import write_output
from config import clear, parsing_config, get_key


def generate(maze_class: MazeGenerator) -> list[list[int]]:
    maze = generate_maze(maze_class)
    path = solve((1, 3), (13, 13), maze)
    solve(maze_class._entry, maze_class._exit, maze)
    write_output(maze, (1, 3), (13, 13), path)
    render_maze(maze)
    return maze


def handle_input(maze_class: MazeGenerator, maze: list[list[int]]) -> bool:
    key = get_key()
    if (key == "1"):
        clear()
        generate(maze_class)
    elif (key == "3"):
        clear()
        render_maze(maze)
    elif (key == "a"):
        
    elif (key == "4"):
        return False
    else:
        return True
    return True


if __name__ == "__main__":
    print("A-MAZE-ING !")
    # config dict
    maze_class = MazeGenerator(15, 15, (1, 3), (13, 13), "test", False)
    clear()
    maze = generate(maze_class)
    handle = True
    while (handle):
        handle = handle_input(maze_class, maze)
