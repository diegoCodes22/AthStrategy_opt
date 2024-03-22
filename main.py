from static_portal import StaticPortal
from utils import sleep_till_open


def main() -> None:
    sleep_till_open()
    StaticPortal()


if __name__ == "__main__":
    main()
