import typing


def main() -> None:
    config_dict: dict = {}
    f: typing.IO = open("./output_maze.txt")
    content = f.read()
    f.close()
    print(f"{content}")
    lines = content.splitlines()

    for line in lines
