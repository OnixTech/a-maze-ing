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

    def validation(self) -> bool:
        return True
