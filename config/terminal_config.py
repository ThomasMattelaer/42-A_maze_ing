import termios
import tty
import sys
# import os


def get_key() -> str:
    """Read a single keypress without waiting for Enter.

    Returns:
        The character pressed.
    """
    fd = sys.stdin
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        key = fd.read(1)
    finally:
        termios.tcsetattr(
            fd,
            termios.TCSADRAIN,
            old_settings
        )
    return key


def move_entry(maze: list[list[int]], entry: tuple[int, int],
               direction: tuple[int, int]) -> tuple[int, int]:
    """Move cursor to the position requested
        ARGS: the maze that is a 2d matrix, entry and direction that are bot
          tuples to indicate coord
        Returns: a tuple of the new entry coord
    """
    row, col = entry
    new_row, new_col = row + direction[0], col + direction[1]
    if (maze[new_row][new_col] in (0, 4, 6)):
        maze[row][col] = maze[new_row][new_col]
        maze[new_row][new_col] = 3
        new_pos = new_row, new_col
    else:
        new_pos = row, col
    return (new_pos)
