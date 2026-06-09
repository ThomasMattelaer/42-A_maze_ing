from mazegen import MazeGenerator, solve, render_matrix


if __name__ == "__main__":
    print("A-MAZE-ING !")
    maze = MazeGenerator(15, 15, (1, 3), (3, 5), "test", True)
    init = maze.init_maze()
    if (maze._width > 10):
        maze.setup42(init)
    maze.generate(init)
    solve((1, 3), (3, 5), init)
    render_matrix(init)
