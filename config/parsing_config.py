from typing import Any


class ConfigError(ValueError):
    """Custom error class"""
    pass


def parsing_config(filename: str) -> dict[str, str]:
    """Parsing the filename that is used to make the configuration of the maze

        ARGS: a .txt filename as string

        RETURNS: return a dict with the key value of the filename
    """
    config_dict: dict[str, str] = {}
    with open(filename) as f:
        content = f.read()
    lines = content.splitlines()

    for line in lines:

        if line.startswith("#") or line.strip() == "":
            continue

        parts = line.split("=")

        if len(parts) < 2:
            raise ConfigError(
                "No equal between values OR no value "
                + "before or after the equal.\n"
                "Please check that there's one equal "
                + "between your key and your value."
            )
        elif len(parts) > 2:
            raise ConfigError(
                "Too many equals.\n"
                "Please check that there's only one equal between "
                + "your key and your value."
            )
        elif parts[0].endswith(" ") or parts[1].startswith(" "):
            raise ConfigError(
                "For each field, the expected format is : field_name=value\n"
                "Please check that there's no spaces before" +
                "or after the equal sign."
            )
        else:
            config_dict.update({parts[0]: parts[1]})

    required_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                     "OUTPUT_FILE", "PERFECT"]

    if not all(key in config_dict for key in required_keys):
        raise ConfigError(
            "All six mandatory keys are not present, please enter: " +
            "WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT"
        )

    for key in config_dict:
        if key == "WIDTH":
            int(config_dict[key])

        if key == "HEIGHT":
            int(config_dict[key])

    for key in config_dict:
        if key in ("ENTRY", "EXIT"):
            parts = config_dict[key].split(",")
            if len(parts) < 2:
                raise ConfigError(
                    f"No ',' between values in '{key}'.\n"
                    "Please check that there's one comma between " +
                    "your two numbers."
                )
            elif len(parts) > 2:
                raise ConfigError(
                    f"Too many commas in '{key}'.\n"
                    "Please check that there's one comma between " +
                    "your two numbers."
                )
            elif parts[0].endswith(" ") or parts[1].startswith(" "):
                raise ConfigError(
                    f"'{key}' expects two values separated by " +
                    "',' without spaces: "
                    f"{key}=numeric_value,numeric_value"
                )
            x = int(parts[0])
            y = int(parts[1])
            if x < 0 or y < 0:
                raise ConfigError(f"Coordinates in '{key}' can't be negative.")
            if x >= int(config_dict["WIDTH"]):
                raise ConfigError(f"The {key.lower()} point x={x} is " +
                                  "outside the maze width.")
            if y >= int(config_dict["HEIGHT"]):
                raise ConfigError(f"The {key.lower()} point y={y} is " +
                                  "outside the maze height.")

        if key == "OUTPUT_FILE":
            if not config_dict[key].endswith(".txt"):
                raise ConfigError("'OUTPUT_FILE' must end with " +
                                  "'.txt': OUTPUT_FILE=file_name.txt")
            if len(config_dict[key]) == 4:
                raise ConfigError("The file name can't just be '.txt' " +
                                  ", add a name before.")
        if key == "PERFECT":
            if config_dict[key] not in ("True", "False"):
                raise ConfigError("'PERFECT' expects 'True' or 'False': " +
                                  "PERFECT=True or PERFECT=False")
        if key == "SEED":
            (int(config_dict["SEED"]))

    if config_dict["ENTRY"] == config_dict["EXIT"]:
        raise ConfigError("'ENTRY' and 'EXIT' can't have the same "
                          + "coordinates.")

    return config_dict


def parsing_output(filename: str) -> dict[str, Any]:
    """Function to set properly the type of the dict
        ARGS: filename in str to passs to the fucntion parsing_config

        Returns: a dict that contain a string key and different type of value
    """
    config = parsing_config(filename)
    entry_row = int(config["ENTRY"].split(",")[0])
    entry_col = int(config["ENTRY"].split(",")[1])
    entry = (entry_row, entry_col)
    exit_row = int(config["EXIT"].split(",")[0])
    exit_col = int(config["EXIT"].split(",")[1])
    exit = (exit_row, exit_col)
    perfect = config["PERFECT"] == "True"
    seed = None
    if "SEED" in config:
        seed = int(config["SEED"])
    config_dict = {
        "output_file": config["OUTPUT_FILE"],
        "width": int(config["WIDTH"]),
        "height": int(config["HEIGHT"]),
        "entry": entry,
        "exit": exit,
        "perfect": perfect,
        "seed": seed
    }

    return config_dict


def parsing_main(filename: str) -> dict[str, Any]:
    """catch the error of the previous functions and share it with the main

        ARGS: filename in str to passs to the fucntion parsing_config

        Returns: a dict that contain a string key and different type of value
    """
    try:
        return parsing_output(filename)
    except (ConfigError, ValueError, FileNotFoundError, OSError) as e:
        print(f"Config error: {e}")
        raise SystemExit(1)
