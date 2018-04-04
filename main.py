import logging
from logging import debug, warning, info
import sys

def main():
    debug("This is a message")
    warning("This is a warning")
    info("This is info")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if str(sys.argv[1]).lower() == "debug":
            print("Set debug")
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    main()
