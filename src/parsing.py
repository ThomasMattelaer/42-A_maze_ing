import typing


def main() -> None:
    f: typing.IO = open("maze.txt", "r")
    content = f.read()
    f.close()
    print(f"{content}")


if __name__ == "__main__":
    main()
