import random


class MazeGenerator():
    """Class that handle the generation of the maze"""

    def __init__(self,
                 width: int,
                 height: int,
                 entry: tuple[int, int],
                 exit: tuple[int, int],
                 output_file: str,
                 perfect: bool
                 ) -> None:

        self._height = height
        self._width = width
        self._entry = entry
        self._exit = exit
        self._output_file = output_file
        self._perfect = perfect

    def draw_rectangle(self) -> None:
        color = random.randint(0, 256)
        print(f"\x1b[38;5;{color}m{chr(9581) + chr(9472) * (self._width * 2)}"
              + f"{chr(9582)}\x1b[0m")

        for i in range(self._height):
            print(f"\x1b[38;5;{color}m{chr(9474)}{' ' * (self._width * 2)}" +
                  f"{chr(9474)}\x1b[0m")

        print(f"\x1b[38;5;{color}m{chr(9584) + chr(9472) * (self._width * 2)}"
              + f"{chr(9583)}\x1b[0m")

    def tab(self) -> list[list[int | str]]:
        tab: list[list[int | str]] = [[9, 5, 5, 5, 3],
                                      [8, 0, 5, 0, 2],
                                      [8, 6, 5, "C", 2],
                                      [8, 0, 5, 0, 2],
                                      ["C", 5, 5, 5, 6],
                                      ]
        return tab

    def render_tab(self, tab):
        TOP = 1
        RIGHT = 2
        BOTTOM = 4
        LEFT = 8
        color = random.randint(0, 256)
        for row in range(len(tab)):
            # HIGH
            for cell, value in enumerate(tab[row]):
                if isinstance(tab[row][cell], str):
                    value = int(tab[row][cell], 16)
                if (row == 0 and cell == 0):
                    print(f"\x1b[38;5;{color}m╭\x1b[0m", end="")
                if (value & TOP):
                    print(f"\x1b[38;5;{color}m──\x1b[0m", end="")
                else:
                    print("  ", end="")

            # RIGHT BORDER
            if row == 0:
                print(f"\x1b[38;5;{color}m╮\x1b[0m", end="")
            elif row == self._height - 1:
                print(f"\x1b[38;5;{color}m╯\x1b[0m", end="")
            else:
                print(f"\x1b[38;5;{color}m│\x1b[0m", end="")
            print()

            # MID
            for cell, value in enumerate(tab[row]):
                if isinstance(value, str):
                    value = int(value, 16)
                if (value & LEFT):
                    print(f"\x1b[38;5;{color}m│\x1b[0m", end="")
                if value & BOTTOM:
                    print(f"\x1b[38;5;{color}m──\x1b[0m", end="")
                else:
                    print("  ", end="")
            if row == self._height - 1:
                print(f"\x1b[38;5;{color}m╯\x1b[0m", end="")
            else:
                print(f"\x1b[38;5;{color}m│\x1b[0m", end="")
            print()

if __name__ == "__main__":

    maze = MazeGenerator(5, 5, (10, 2), (10, 2), "test", True)
    tab = maze.tab()
    maze.render_tab(tab)
