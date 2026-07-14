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
        self._validation(config)

        return config

    def _parse(self) -> dict[str, str]:
        config: dict[str, str] = {}
        with open(self.filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                key, value = line.split("=")
                config[key] = value

        return config

    def _validation(self, config: dict[str, str]) -> None:
        keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
        for key in keys:
            if key not in config:
                raise ValueError(f"Missing key: {key}")

        for key in config:
            if key not in keys:
                raise ValueError(f"Unknown key: {key}")

        try:
            self.width = int(config["WIDTH"])
            self.height = int(config["HEIGHT"])
        except ValueError as err:
            raise ValueError(
                "WIDTH and HeIGHT must be integers"
            ) from err

        self._tuple_validation(config)

    def _tuple_validation(self, config: dict[str, str]) -> None:
        entry = config["ENTRY"].split(",")
        exit_point = config["EXIT"].split(",")

        if len(entry) != 2:
            raise ValueError("ENTRY must have format x,y")

        if len(exit_point) != 2:
            raise ValueError("EXIT must have format x,y")

        try:
            self.entry = (int(entry[0]), int(entry[1]))
            self.exit_point = (int(exit_point[0]), int(exit_point[1]))
        except ValueError as err:
            raise ValueError(
                "Entry and EXIT coordinates must be integers"
                ) from err
