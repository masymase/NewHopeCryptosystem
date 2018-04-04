import debug
import sys

def main():
    if len(sys.argv) == 1:
        if str(sys.argv[0]).lower() == "debug":
            debug.setDebug()


if __name__ == "__main__":
    main()
