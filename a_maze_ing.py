import sys

def main() -> None:
    with open(sys.argv[1], "r") as file:
        content = file.read()

    print(content)


if __name__ == "__main__":
    main()
