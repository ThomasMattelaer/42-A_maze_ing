from mazegen import MazeGenerator, solve, render_maze, generate_maze


if __name__ == "__main__":
    print("A-MAZE-ING !")
    maze_class = MazeGenerator(15, 15, (1, 3), (3, 5), "test", True, seed=81)
    maze = generate_maze(maze_class)
    solve(maze_class._entry, maze_class._exit, maze)
    render_maze(maze)
    