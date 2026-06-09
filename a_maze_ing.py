from mazegen import MazeGenerator, solve, render_maze, generate_maze
from mazegen import write_output


def ask_user_action() -> None:
    print("""1. Change the color of the Maze
          2. Hide/Show the ideal path
          3. Re-generate the maze""")


if __name__ == "__main__":
    print("A-MAZE-ING !")
    # config dict
    maze_class = MazeGenerator(15, 15, (1, 3), (13, 13), "test", False)
    maze = generate_maze(maze_class)
    path = solve((1, 3), (13, 13), maze)
    solve(maze_class._entry, maze_class._exit, maze)
    write_output(maze, (1, 3), (13, 13), path)
    render_maze(maze)
