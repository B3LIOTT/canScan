
from modules import *
from time import sleep
import os


def list_files():
    os.chdir('dumps')
    datas = {}
    files = os.listdir(".")
    files = [file for file in files if os.path.isfile(os.path.join(".", file))]
    
    for i, file in enumerate(files):
        if file.endswith('.csv'):
            data_name = file.split('.')[0]
            datas[i] = data_name
            print(f"{i}. {data_name}")

    return datas


if __name__ == "__main__":
    try:
        print("Welcome to the CAN bus analyzer.")
        datas = list_files()
        ind = int(input("Which data do you want to analyze ?\n> "))
        assert ind > 0 and ind <= len(datas)
        analyze(datas[ind])

    except Exception as e:
        print(f"An error occured: {e}")
        exit(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        exit(0)
