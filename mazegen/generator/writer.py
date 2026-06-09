def convert_maze(maze: list[list[int]]) -> list[str]:
    height = (len(maze) - 1) // 2
    width = (len(maze[0]) - 1) // 2
    lines: list[str] = []

    for y in range(height):
        line = ""
        for x in range(width):
            row, col = y*2+1, x*2+1
            value = 0
            if maze[row-1][col] != 0:
                value += 1
            if maze[row][col+1] != 0:
                value += 2
            if maze[row+1][col] != 0:
                value += 4
            if maze[row][col-1] != 0:
                value += 8
            line += format(value, 'X')
        lines.append(line)
    return lines


def write_output(maze: list[list[int]], entry: tuple[int, int],
                 exit: tuple[int, int], path: str,
                 filename: str = "output_maze.txt") -> None:
    lines = convert_maze(maze)
    with open(filename, 'w') as f:
        for line in lines:
            f.write(line+"\n")
        f.write("\n")
        
        f.write(f"{entry[0],entry[1]}")
        f.write("\n")
        
        f.write(f"{exit[0],exit[1]}")
        f.write("\n")
        f.write(path+"\n")
