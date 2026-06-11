import termios
import tty
import sys
import os


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


def clear() -> None:
    """"function to clear the terminal"""
    os.system("clear")
    # print("\033[2J")


def move_entry(maze: list[list[int]], entry: tuple[int, int],
               direction: tuple[int, int]) -> tuple[int, int]:
    """Move cursor to the position requested"""
    row, col = entry
    new_row, new_col = row + direction[0], col + direction[1]
    if (maze[new_row][new_col] in (0, 4, 6)):
        maze[row][col] = maze[new_row][new_col]
        maze[new_row][new_col] = 3
        new_pos = new_row, new_col
    else:
        new_pos = row, col
    return (new_pos)
