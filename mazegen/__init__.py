from .generator.maze_generator import (MazeGenerator,
                                       render_maze,
                                       clear,
                                       generate_maze,
                                       COLORS)
from .generator.solver import solve


__all__ = ["solve", "MazeGenerator", "render_maze", "generate_maze",
           "COLORS", "clear"]
