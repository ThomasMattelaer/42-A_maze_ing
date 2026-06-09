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

def write_output(filename: str, list[list])
