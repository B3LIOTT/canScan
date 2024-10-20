import pandas as pd
import base64
import matplotlib.pyplot as plt


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

# Fonction pour décoder la base64 et retourner une liste d'entiers (un entier par octet)
def base64_to_ints(b64_string):
    decoded_bytes = base64.b64decode(b64_string)
    decoded_ints = [int(byte) for byte in decoded_bytes]
    return decoded_ints



def analyze(name: str):
    print("Analyzing the file...")
    df, seq = load_data(name)

    df['data_ints'] = df['data'].apply(base64_to_ints)

    max_octets = max(df['data_ints'].apply(len))

    for i in range(max_octets):
        df[f'byte_{i+1}'] = df['data_ints'].apply(lambda x: x[i] if i < len(x) else None)

    dfs_par_arbitration_id = {arbitration_id: group for arbitration_id, group in df.groupby('arbitration_id')}

    for arbitration_id, df_group in dfs_par_arbitration_id.items():
        num_octets = df_group['data_ints'].apply(len).max()
        
        fig, axs = plt.subplots(num_octets, 1, figsize=(8, num_octets * 2))  # Une subplot par octet
        
        if num_octets == 1:
            axs = [axs]

        for i in range(num_octets):
            axs[i].plot(df_group['timestamp'], df_group[f'byte_{i+1}'], linestyle='-', label=f'Byte {i+1}')
            axs[i].set_xlabel('Timestamp')
            axs[i].set_ylabel(f'Byte {i+1}')
            axs[i].grid(True)
            axs[i].legend(loc='upper right')
        
        plt.suptitle(f'Arbitration ID {arbitration_id} - Byte Data')
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()