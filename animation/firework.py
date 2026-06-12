import time
import os

FIREWORKS_FRAMES = [
    """
        *       *
      * | *   * | *
    *---+---*---+---*
      * | *   * | *
        *       *
    """,
    """
       \\ | /   \\ | /
     ---[*]--- ---[*]---
       / | \\   / | \\
    """,
    """
    *  .  *  .  *  .  *
    .  *  .  *  .  *  .
    *  .  *  .  *  .  *
    """,
    """
         🎆  YOU WON  🎆
    """,
]


def celebrate() -> None:
    """Function to display ascii code when program is over"""
    for _ in range(10):
        for frame in FIREWORKS_FRAMES:
            os.system('clear')
            print(frame)
            time.sleep(0.15)
    os.system('clear')
    print("\n\n\t🎆  YOU WON  🎆\n\n")
