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

        if parts[0].endswith(" ") or parts[1].startswith(" "):
            print("For each field, the expected format is :")
            print("field_name=value_expected")
            return
        try:
            config_dict.update({parts[0]: parts[1]})
        except IndexError:
            print("No equal between values or, ", end="")
            print("no value before or after the equal\n")

    required_keys = [
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
        ]

    if not all(key in config_dict for key in required_keys):
        print("All six mandatory keys are not present, please ", end="")
        print("enter the following fields:")
        print("WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT")

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
            if parts[0].endswith(" ") or parts[1].startswith(" "):
                print("'ENTRY' field is expecting ", end="")
                print("two values ", end="")
                print("separated by a ',' without spaces as follows :")
                print("ENTRY=numeric_value,numeric_value")
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
            if parts[0].endswith(" ") or parts[1].startswith(" "):
                print("'EXIT' field is expecting ", end="")
                print("two values ", end="")
                print("separated by a ',' without spaces as follows :")
                print("EXIT=numeric_value,numeric_value")
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


if __name__ == "__main__":
    main()
