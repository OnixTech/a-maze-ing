import os
from pathlib import Path


class ParserError(Exception):
    pass


class ConfigParser:
    def __init__(self, filename: str) -> None:
        self.width: int = 20
        self.height: int = 20
        self.entry: tuple[int, int] = (0, 0)
        self.exit: tuple[int, int] = (19, 14)
        self.perfect: bool = False
        self.filename: str = filename

    def load(self) -> dict[str, str]:
        config = self._parse()
        self._validate(config)

        return config

    def _parse(self) -> dict[str, str]:
        config: dict[str, str] = {}

        try:
            with open(self.filename) as file:
                for line in file:
                    line = line.strip()

                    if not line or line.startswith("#"):
                        continue

                    try:
                        key, value = line.split("=")
                        config[key.strip()] = value.strip()
                    except ValueError as err:
                        raise ParserError(f"Extraneous value: {line}") from err

        except OSError as err:
            ParserError(f"{self.filename} not accessible: {err}")

        return config

    def _validate(self, config: dict[str, str]) -> None:
        # Keys Expected
        keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]

        # Check if all mandatory keys are available
        for key in keys:
            if key not in config:
                raise ParserError(f"Missing key: {key}")

        # Check for alien keys
        for key in config:
            if key not in keys:
                raise ParserError(f"Unknown key: {key}")

        self._validate_width_height(config["WIDTH"], config["HEIGHT"])

        # save the validated width and height
        self.width = int(config["WIDTH"])
        self.height = int(config["HEIGHT"])

        # Validate coordinates
        self._validate_coordinates(config)

        # Save the validated coordinates
        entry_x, entry_y = config["ENTRY"].split(",")
        self.entry = int(entry_x), int(entry_y)
        exit_x, exit_y = config["EXIT"].split(",")
        self.exit = int(exit_x), int(exit_y)

        # Check if OUTPUT_FILE is writable
        output_file = Path(config["OUTPUT_FILE"])
        if output_file.exists() and not os.access(output_file, os.W_OK):
            raise ParserError(f"OUTPUT_FILE '{output_file}' is not writable")

        # Check if PERFECT value is valid
        booleans = ["True", "False"]
        if config["PERFECT"] not in booleans:
            raise ParserError(
                f"PERFECT must be 'True' or 'False': {config['PERFECT']}"
            )

    def _validate_width_height(self, width: str, height: str) -> None:
        for name, value in zip(
            ["WIDTH", "HEIGHT"],
            [width, height],
            strict=False,
        ):
            try:
                v = int(value)
            except ValueError as err:
                raise ParserError(f"{name} must be integer: {value}") from err

            if 0 > v > 800:
                raise ParserError(f"{name} must be between 0 and 800: {v}")

    def _validate_coordinates(self, config: dict[str, str]) -> None:
        for name, value in zip(
            ["ENTRY", "EXIT"],
            [config["ENTRY"], config["ENTRY"]],
            strict=False,
        ):
            # Validate format
            try:
                x_str, y_str = value.split(",")
            except ValueError as err:
                raise ParserError(
                    f"{name} must have fomat of 'x,y': {value}"
                ) from err

            # Check if not int
            try:
                x, y = int(x_str), int(y_str)
            except ValueError as err:
                raise ParserError(
                    f"{name} must have valid integers: {value}"
                ) from err

            # Check if coordinates are valid for the maze
            if 0 > x > self.width or 0 > y > self.height:
                raise ParserError(f"{name} must be within the maze: {value}")
