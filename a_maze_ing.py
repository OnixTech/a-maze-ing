import config_parser


class Cell:
    def __init__(self) -> None:
        self.walls = 0b1111
        self.visited = False


class MazeGenerator:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = []

    def create_grid(self) -> None:
        for _ in range(self.height):
            row = []

            for _ in range(self.width):
                row.append(Cell())

            self.grid.append(row)

    def export(self, filename: str) -> None:
        with open(filename, "w") as file:
            for row in self.grid:
                for cell in row:
                    file.write(f"{cell.walls:X}")

                file.write("\n")


def main() -> None:
    maze = MazeGenerator(10, 10)
    maze.create_grid()
    maze.export("maze.txt")
    config = config_parser.ConfigParser("default_config.txt")
    print(config.parse())


if __name__ == "__main__":
    main()
