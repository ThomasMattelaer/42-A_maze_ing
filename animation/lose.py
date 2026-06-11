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

  gg ez, try harder next time
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

  gg ez, try harder next time
    """,
]


def loser():
    for _ in range(6):
        for frame in LOSER_FRAMES:
            os.system('clear')
            print(frame)
            time.sleep(0.2)
    os.system('clear')
    print("\n\t💀  L O S E R  💀\n\tpress [1] to cry and retry\n")
