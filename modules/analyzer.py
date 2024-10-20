import pandas as pd

def load_csv(file_path: str):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print("Invalid or nonexistent file.")
        exit(1)

def analyze(df: pd.DataFrame):
    print("Analyzing the file...")
    print(df.head())

    # Some analysis here...

    print("Analysis done.")