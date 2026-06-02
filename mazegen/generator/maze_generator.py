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

    def render_tab(self, tab: list[list[int | str]]) -> None:
        color = random.randint(0, 256)

        for row in range(len(tab)):
            len_row = len(tab[row])
            #  high
            for cell in range(len_row):
                value = tab[row][cell]
                if isinstance(value, str):
                    value = int(value, 16)
                if (row == 0 and cell == 0):
                    print(f"\x1b[38;5;{color}m{chr(9581) }\x1b[0m", end="")
                if (value & 1):
                    print(f"\x1b[38;5;{color}m{chr(9472) * 2}\x1b[0m", end="")
                else:
                    print("  ", end="")
            if row == 0:
                print(f"\x1b[38;5;{color}m{chr(9582)}\x1b[0m", end="")
            elif row == self._height - 1:
                print(f"\x1b[38;5;{color}m{chr(9584)}\x1b[0m", end="")
            else:
                print(f"\x1b[38;5;{color}m{chr(9474)}\x1b[0m", end="")
            print()
            #  mid
            for cell, value in enumerate(tab[row]):
                if isinstance(value, str):
                    value = int(value, 16)
            if (value & 8):
                print(f"\x1b[38;5;{color}m│\x1b[0m", end="")
            elif (value & 4):
                print(f"\x1b[38;5;{color}m──\x1b[0m", end="")
            else:
                print("  ", end="")


if __name__ == "__main__":

    maze = MazeGenerator(5, 5, (10, 2), (10, 2), "test", True)
    tab = maze.tab()
    maze.render_tab(tab)
