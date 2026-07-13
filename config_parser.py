class ConfigParser:
    def __init__(self, filename: str) -> None:
        self.width: int = 20
        self.height: int = 20
        self.entry: tuple[int, int]
        self.exit: tuple[int, int]
        self.perfect: bool = False
        self.filename: str = filename

    def parse(self) -> dict:
        config = {}
        with open(self.filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                key, value = line.split("=")
                config[key] = value

        return config

    def validation(self, config: dict[str, str]) -> bool:
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
        except ValueError:
            print("WIDTH and HIGHT must be integers")

        return True
