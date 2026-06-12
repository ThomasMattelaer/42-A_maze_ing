import sys
import random
from mazegen import MazeGenerator, solve, render_maze, generate_maze, COLORS
from mazegen import write_output
from config import clear, get_key, parsing_main, move_entry
from animation import celebrate, loser


class GameContext():
    """Class to handle the state of the maze afteer the useraction"""

    def __init__(self,
                 maze_class: MazeGenerator,
                 maze: list[list[int]],
                 entry: tuple[int, int],
                 exit: tuple[int, int],
                 color_index: int,
                 path: bool) -> None:

        self.maze_class = maze_class
        self.maze = maze
        self.initial_entry = entry
        self.entry = entry
        self.exit = exit
        self.color_index = color_index
        self.path = path


def generate(maze_class: MazeGenerator, path: bool = True,
             color_index: int = 0) -> list[list[int]]:
    """Helper to consolidate all the functions to generate
    Args: maze_class, the instance of the maze, path is a boolean,
    color index to define the theme
    Returns: a 2d matrix
    """
    maze = generate_maze(maze_class, path, color_index)
    path_solver = solve(maze_class._entry, maze_class._exit, maze,
                        path, color_index)
    write_output(maze, maze_class._entry, maze_class._exit, path_solver,
                 maze_class._output_file)
    return maze


def extend_tuple(tuple: tuple[int, int]) -> tuple[int, int]:
    """Double the tuple to fit the 2d matrix

       Args: a tuple of int

       Returns: a tuple of int
    """
    row, col = tuple
    new_row, new_col = (row * 2) + 1, (col * 2) + 1
    return new_row, new_col


def handle_input(ctx: GameContext) -> bool:
    """Helper to send the state to the instance of the class GameContext
    Args: ctx a GameContext instance
    Returns: a bool to stop or not the programm
    """
    key = get_key()

    MOVES = {"a": (0, -1), "d": (0, 1), "s": (1, 0), "w": (-1, 0)}
    should_refresh = True

    if (key == "1"):
        ctx.maze = generate(ctx.maze_class, ctx.path, ctx.color_index)
        ctx.entry = ctx.initial_entry
    elif (key == "2"):
        ctx.path = not ctx.path
    elif (key == "3"):
        new_index = ctx.color_index
        while new_index == ctx.color_index:
            new_index = random.randint(0, len(COLORS) - 1)
        ctx.color_index = new_index
    elif (key in MOVES):
        ctx.entry = move_entry(ctx.maze, ctx.entry, MOVES[key])
        if ctx.entry == ctx.exit:
            celebrate()
            return False
    elif (key == "4"):
        loser()
        return False
    else:
        should_refresh = False

    if (should_refresh):
        clear()
        render_maze(ctx.maze, ctx.path, ctx.color_index)
    return True


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        raise SystemExit(1)
    try:
        config_file = sys.argv[1]
        config = parsing_main(config_file)
        maze_class = MazeGenerator(config["height"],
                                   config["width"],
                                   config["entry"],
                                   config["exit"],
                                   config["output_file"],
                                   config["perfect"],
                                   81
                                   )
        clear()
        maze = generate(maze_class, True)
        ctx = GameContext(maze_class,
                          maze,
                          extend_tuple(config["entry"]),
                          extend_tuple(config["exit"]),
                          0,
                          True
                          )
        handle = True
        while (handle):
            handle = handle_input(ctx)

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
    except IndexError as e:
        print(f"ERROR: {e}")
    except PermissionError as e:
        print(f"ERROR: {e}")
    except IsADirectoryError as e:
        print(f"ERROR: {e}")
    except UnicodeError as e:
        print(f"ERROR: {e}")
    except KeyError as e:
        print(f"ERROR: {e}")
    except ValueError as e:
        print(f"ERROR: {e}")
    except OSError as e:
        print(f"ERROR: {e}")
    except KeyboardInterrupt as e:
        print(f"ERROR: {e}")
