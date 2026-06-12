import time
import os

LOSER_FRAMES = [
    r"""
  ___________
 |  L O S E R  |
 |___________|

    o  O  o
  .    |    .
  ( x___x )
   (  ___  )
    \     /
  ---o---o---
    /     \

  try harder next time
    """,
    r"""
  ___________
 |  L O S E R  |
 |___________|

    o  O  o
  *    |    *
  ( >___< )
   (  ___  )
    \     /
  ---o---o---
    /     \

  try harder next time
    """,
]


def loser() -> None:
    """ascii code to display when the program ends without success"""
    for _ in range(6):
        for frame in LOSER_FRAMES:
            os.system('clear')
            print(frame)
            time.sleep(0.2)
    os.system('clear')
