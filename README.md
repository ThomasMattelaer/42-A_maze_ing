*This project has been created as part of the 42 curriculum by tmattela, josamba-.*

# A-Maze-ing

## Description

**A-Maze-ing** is a configurable maze generator written in Python 3.10+.

From a simple configuration file, the program:

1. **generates** a maze (optionally *perfect* — exactly one path between entry
   and exit),
2. draws a visible **"42"** pattern with fully-closed cells in the center,
3. computes the **shortest path** between entry and exit,
4. **writes** the result to an output file using a compact hexadecimal wall
   encoding,
5. **displays** the maze in the terminal with an interactive menu (regenerate,
   show/hide the path, change colours, move the entry).

The maze-generation logic is isolated in a reusable, pip-installable package
(`mazegen`) so it can be imported by future projects.

## Instructions

### Requirements

- Python **3.10 or later**
- The project has **no external runtime dependencies** (only the standard
  library). `flake8` / `mypy` are only needed for linting.

### Install, run, lint (via the Makefile)

```sh
make install      # create the venv and install dependencies
make run          # run the program on config.txt
make debug        # run under pdb
make lint         # flake8 . + mypy (project flags)
make lint-strict  # flake8 . + mypy --strict
make clean        # remove caches and the venv
```

### Run manually

```sh
python3 a_maze_ing.py config.txt
```

`a_maze_ing.py` takes exactly **one argument**: the path to a configuration
file. Any error (missing file, bad syntax, impossible parameters, …) is reported
with a clear message instead of crashing.

### Interactive controls

| Key       | Action                              |
|-----------|-------------------------------------|
| `1`       | Re-generate a new maze              |
| `2`       | Show / hide the shortest path       |
| `3`       | Change the maze colours (5 palettes)|
| `w/a/s/d` | Move the entry cell in the maze     |
| `4`       | Quit                                |

## Configuration file format

The configuration file contains **one `KEY=VALUE` pair per line**. Lines
starting with `#` and empty lines are ignored. **No spaces** are allowed around
the `=` sign.

A valid default configuration is provided in the repository.

### Example

```
# A-Maze-ing configuration
WIDTH=15
HEIGHT=15
ENTRY=0,0
EXIT=14,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

### Mandatory keys

| Key           | Description                          | Constraints                                         |
|---------------|--------------------------------------|-----------------------------------------------------|
| `WIDTH`       | Maze width (number of cells)         | integer                                             |
| `HEIGHT`      | Maze height (number of cells)        | integer                                             |
| `ENTRY`       | Entry coordinates `x,y`              | `x` = column, `y` = row; non-negative; inside bounds|
| `EXIT`        | Exit coordinates `x,y`               | same as `ENTRY`; **must differ** from `ENTRY`       |
| `OUTPUT_FILE` | Output filename                      | must end with `.txt` (and not be just `.txt`)       |
| `PERFECT`     | Perfect maze?                        | `True` or `False`                                   |

> **Coordinate convention:** coordinates are written `x,y` where `x` is the
> column and `y` is the row. The same convention is used everywhere (generation,
> solving, hexadecimal export).

## Output file format

Each cell is encoded as **one hexadecimal digit** describing which of its walls
are **closed** (bit set to `1`):

| Bit (weight) | Direction |
|--------------|-----------|
| `0` → 1      | North     |
| `1` → 2      | East      |
| `2` → 4      | South     |
| `3` → 8      | West      |

Because a cell has 4 walls, there are exactly **16 combinations**, which map
perfectly onto a single hexadecimal digit (`0`–`F`). For example `9` (binary
`1001`) means North + West are closed.

Cells are written **row by row**, one row per line. Then, after an **empty
line**, three lines follow: the entry coordinates, the exit coordinates, and the
shortest path expressed with the letters `N`, `E`, `S`, `W`. Every line ends
with `\n`.

## Maze generation algorithm

We use an **iterative Depth-First Search (DFS) backtracker** (a.k.a. *recursive
backtracker*) on a grid where cells live at odd indices of a `(2·H+1) × (2·W+1)`
matrix and walls live between them.

1. Start from a random cell, mark it visited, push it on a stack.
2. From the top of the stack, pick a random **unvisited** neighbour, carve the
   wall between them, push the neighbour.
3. When a cell has no unvisited neighbour, **backtrack** (pop the stack).
4. Repeat until the stack is empty.

This naturally produces a **perfect maze** (a spanning tree: full connectivity,
no isolated cell, exactly one path between any two cells).

- **`PERFECT=False`:** while backtracking, with a 15% probability we open an
  extra wall ("braiding"), creating loops — so multiple paths can exist.
- **The "42" pattern:** centered cells are marked as fully closed before
  carving, and the DFS is forbidden from carving into them (including its random
  starting cell), so the "42" stays fully closed in **perfect** mazes. If the
  maze is too small to host the pattern, an error message is printed and the
  pattern is skipped.
  - **Design choice (non-perfect mazes):** when `PERFECT=False`, the braiding
    step may open a wall adjacent to the "42", partially breaching it. This is an
    accepted trade-off: non-perfect mazes deliberately allow extra openings, so
    we let the braiding act uniformly rather than special-casing the pattern.
    Use `PERFECT=True` if you need the "42" guaranteed fully closed.

The **shortest path** is computed separately with a **Breadth-First Search
(BFS)**, which guarantees the minimal number of steps between entry and exit.

### Why these algorithms

- **DFS backtracker** is simple to implement, memory-friendly (a single stack),
  and produces long, winding corridors with a single guaranteed solution — the
  textbook way to obtain a *perfect* maze (a spanning tree).
- **BFS** is the natural choice for the **shortest** path on an unweighted grid:
  the first time it reaches the exit, it has found a path of minimal length.

## Reusable code

The maze-generation logic is packaged as the standalone, pip-installable
`mazegen` package (built from `pyproject.toml`):

- `MazeGenerator` — the generator class (size, entry/exit, perfect flag, seed).
- `generate_maze()` — convenience helper that builds a full maze.
- `solve()` — BFS shortest-path solver returning the `N/E/S/W` path.

See [`mazegen/README.md`](mazegen/README.md) for the module documentation and a
usage example. Build the wheel/sdist with a standard build (e.g.
`python -m build`), producing `mazegen-1.0.0-py3-none-any.whl`.

## Advanced features

- **Perfect and non-perfect mazes** (with controlled braiding).
- **Reproducibility** through an optional `seed`.
- **Path-drawing animation** while solving.
- **Interactive terminal UI**: regenerate, show/hide path, 5 colour palettes,
  and **moving the entry** inside the maze (bonus).

## Resources

- Wikipedia: *Maze generation algorithm*, *Depth-first search*,
  *Breadth-first search*, *Spanning tree*.
- ANSI escape codes (256-colour mode) for terminal rendering.

### Use of AI

AI was used as an **assistant** on a few well-scoped tasks:

- writing the **end game animations**,
- drafting this **`README.md`**,
- explaining concepts (hexadecimal wall encoding, threading interactive state
  through the render loop).

All AI-assisted parts were **read, understood, tested, and adapted** by the
authors.

## Team & project management

| Member                | Login      | Responsibilities                                                                                      |
|-----------------------|------------|-------------------------------------------------------------------------------------------------------|
| Thomas Mattelaer      | `tmattela` | Maze generation, `a_maze_ing.py` (main), user interaction, docstrings, Makefile, visualizer           |
| Josué Samba Dianzungu | `josamba-` | Solver, configuration parsing, animation, error handling, output-file handling                        |

- **Planning:** we started with the configuration parser and the core grid
  generator, then added the hexadecimal export, the solver, and finally the
  interactive visual layer and bonuses. The plan evolved as we discovered the
  need to keep a consistent `x,y` convention across every module.
- **What worked well:** splitting the project into clear, independent modules
  (parser / generator / writer / solver / renderer) let each of us work in
  parallel and made debugging straightforward.
- **What could be improved:** decoupling the solver from the display, and wiring
  the optional `seed` from the configuration file.
- **Tools:** Git, `flake8`, `mypy`, `venv`, a `Makefile`, and an AI assistant
  (see above).
