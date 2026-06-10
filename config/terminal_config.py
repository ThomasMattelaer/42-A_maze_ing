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


def move_entry(maze: list[list[int]], entry: tuple, direction: tuple) -> None:
    """Move cursor to the position requested"""
    entry_row, entry_col = entry[0], entry[1]
    maze[entry_row][entry_col] = 0
    maze[entry_row + direction[0]][entry_col + direction[1]] = 4


if __name__ == "__main__":
    while (1):
        get_key()
