
from modules import *


if __name__ == "__main__":
    try:
        wake_up_maestro()
    except Exception as e:
        print("The file has been deleted due to an error: ", e)
        exit(1)
