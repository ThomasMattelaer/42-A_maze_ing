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
        print(f"\x1b[38;5;{color}m{chr(9487) + chr(9473) * (self._width * 2)}"
              + f"{chr(9491)}\x1b[0m")

        for _ in range(self._height):
            print(f"\x1b[38;5;{color}m{chr(9475)}{' ' * (self._width * 2)}" +
                  f"{chr(9475)}\x1b[0m")

        print(f"\x1b[38;5;{color}m{chr(9495) + chr(9473) * (self._width * 2)}"
              + f"{chr(9499)}\x1b[0m")


if __name__ == "__main__":

    print("test")
    maze = MazeGenerator(18, 15, (10, 2), (10, 2), "test", True)
    maze.draw_rectangle()
