import typing


def main() -> None:
    config_dict: dict = {}
    f: typing.IO = open("./config.txt")
    content = f.read()
    f.close()
    print(f"{content}")
    lines = content.splitlines()

    for line in lines:

        if line.startswith("#") or line.strip() == "":
            continue

        parts = line.split("=")

        if len(parts) < 2:
            print("No equal between values OR, ", end="")
            print("no value before or after the equal")
            print("Please check that there's one equal between", end="")
            print(" your key and your value")
            return

        elif len(parts) > 2:
            print("Too many equals")
            print("Please check that there's only one equal between", end="")
            print(" your key and your value")
            return

        elif parts[0].endswith(" ") or parts[1].startswith(" "):
            print("For each field, the expected format is :")
            print("field_name=value_expected")
            return
        else:
            config_dict.update({parts[0]: parts[1]})

    required_keys = [
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
        ]

    if not all(key in config_dict for key in required_keys):
        print("All six mandatory keys are not present, please ", end="")
        print("enter the following fields:")
        print("WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT")
        return

    for key in config_dict:

        if key == "WIDTH":
            try:
                int(config_dict[key])
            except ValueError:
                print("'WIDTH' field is expecting ", end="")
                print(" a numeric value as follows :")
                print("WIDTH=numeric_value")

        if key == "HEIGHT":
            try:
                int(config_dict[key])
            except ValueError:
                print("'HEIGHT' field is expecting ", end="")
                print("a numeric value as follows :")
                print("WIDTH=numeric_value")

        if key == "ENTRY":
            parts = config_dict[key].split(",")

            if len(parts) < 2:
                print("No ',' between values OR, ", end="")
                print("no value before or after the ','")
                print("Please check that there's one comma between", end="")
                print(" your two numbers")
                return

            elif len(parts) > 2:
                print("Too many commas")
                print("Please check that there's only one ", end="")
                print("comma between your two numbers")
                return

            elif parts[0].endswith(" ") or parts[1].startswith(" "):
                print("'ENTRY' field is expecting ", end="")
                print("two values ", end="")
                print("separated by a ',' without spaces as follows :")
                print("ENTRY=numeric_value,numeric_value")
            else:
                try:
                    parts = config_dict[key].split(",")
                    int(parts[0])
                    int(parts[1])
                except ValueError:
                    print("'ENTRY' fiels is expecting ", end="")
                    print("two numeric values ", end="")
                    print("outside of the ',' separator:")
                    print("ENTRY=numeric_value,numeric_value")

        if key == "EXIT":
            parts = config_dict[key].split(",")

            if len(parts) < 2:
                print("No ',' between values OR, ", end="")
                print("no value before or after the ','")
                print("Please check that there's one comma between", end="")
                print(" your two numbers")
                return

            elif len(parts) > 2:
                print("Too many commas")
                print("Please check that there's only one ", end="")
                print("comma between your two numbers")
                return

            elif parts[0].endswith(" ") or parts[1].startswith(" "):
                print("'EXIT' field is expecting ", end="")
                print("two values ", end="")
                print("separated by a ',' without spaces as follows :")
                print("EXIT=numeric_value,numeric_value")
            else:
                try:
                    parts = config_dict[key].split(",")
                    int(parts[0])
                    int(parts[1])
                except ValueError:
                    print("'EXIT' fiels is expecting ", end="")
                    print("two numeric values ", end="")
                    print("outside of the ',' separator:")
                    print("EXIT=numeric_value,numeric_value")

        if key == "OUTPUT_FILE":
            if not config_dict[key].endswith(".txt"):
                print("'OUTPUT_FILE' field is expecting ", end="")
                print("to end with '.txt' as follows :")
                print("OUTPUT_FILE=file_name.txt")

        if key == "PERFECT":
            if (not config_dict[key] == "True"
                    and not config_dict[key] == "False"):
                print("'PERFECT' field is expecting ", end="")
                print("'True' or 'False' as value as follows :")
                print("PERFECT=True or PERFECT=False")
    for key in config_dict:
        if key == "ENTRY":
            parts = config_dict[key].split(",")
            x = int(parts[0])
            y = int(parts[1])
            if x >= int(config_dict["WIDTH"]):
                print("The entry point is outside the maze")
                print("Please check that the maze contains ", end="")
                print("exactly one entry point")
                return
            if y >= int(config_dict["HEIGHT"]):
                print("The entry point is outside the maze")
                print("Please check that the maze contains ", end="")
                print("exactly one entry point")
                return
        if key == "EXIT":
            parts = config_dict[key].split(",")
            x = int(parts[0])
            y = int(parts[1])
            if x >= int(config_dict["WIDTH"]):
                print("The exit point is outside the maze")
                print("Please check that the maze contains ", end="")
                print("exactly one exit point")
                return
            if y >= int(config_dict["HEIGHT"]):
                print("The exit point is outside the maze")
                print("Please check that the maze contains ", end="")
                print("exactly one exit point")
                return
    return


if __name__ == "__main__":
    main()
