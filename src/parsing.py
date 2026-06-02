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
            print("Invalid format, please respect the subject format")
            return
        try:
            config_dict.update({parts[0]: parts[1]})
        except IndexError:
            print("No equal between values or, ", end="")
            print("no value before or after the equal\n")
    required_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    if not all(key in config_dict for key in required_keys):
        print("All six mandatory keys are not present, please enter the following fields")
        print("WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT")
    for key in config_dict:
        if key == "WIDTH" or key == "HEIGHT":
            try:
                int(config_dict[key])
            except ValueError:
                print("You need to enter a number in both WIDTH and HEIGHT field\n")
        if key == "ENTRY" or key == "EXIT":
            parts = config_dict[key].split(",")
            if parts[0].endswith(" ") or parts[1].startswith(" "):
                print("Invalid format, please respect the subject format")
            try:
                parts = config_dict[key].split(",")
                int(parts[0])
                int(parts[1])
            except ValueError:
                print("You need to enter two number separated by ', ' in both ENTRY and EXIT field\n")
        if key == "OUTPUT_FILE":
            if not config_dict[key].endswith(".txt"):
                print("The excepted format of your output file ends with a '.txt'\n")
        if key == "PERFECT":
            if not config_dict[key] == "True" and not config_dict[key] == "False":
                print("The excepted format of the 'perfect' field is 'True' or 'False'\n")


if __name__ == "__main__":
    main()
