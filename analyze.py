
from modules import *
from time import sleep


if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        print("The file has been deleted due to an error: ", e)
        exit(1)
