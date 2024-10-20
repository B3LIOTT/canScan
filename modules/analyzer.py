import pandas as pd

def load_data(name: str):
    try:
        csv_path = f"{name}.csv"
        seq_path = f"{name}.seq"
        df = pd.read_csv(csv_path)
        
        with open(seq_path, "r") as file:
            seq = [(int(parts[0]), parts[1]) for line in file for parts in [line.strip().split(":", 1)]]

        return df, seq
    except FileNotFoundError:
        print("Invalid or nonexistent file.")
        exit(1)


def analyze(name: str):
    print("Analyzing the file...")
    df, seq = load_data(name)

    print(df, seq)

    print("Analysis done.")