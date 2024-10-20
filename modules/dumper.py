from datetime import datetime
import yaml
import can
import os

"""
The dumper module is listenning to the CAN bus and writes the messages to a CSV file.
This CSV file will be analyzed later by the analyser module.
"""

def load_config():
    try:
        with open('config.yaml', 'rt') as file:
            config = yaml.safe_load(file)

        wdir = config['dumps_dir']
        os.makedirs(wdir, exist_ok=True)
        str_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_path = f'{wdir}/{str_date}.csv'

    except FileNotFoundError:
        print("Invalid or nonexistent configuration file.")
        print("Please create a config.yaml file in the current directory.")
        exit(1)

    return config, file_path


def end_checks(file_path: str, sequence: list):
    print(f"File {file_path} has been created.")
    print('Do you want to save it ? (o/n)')
    choice = input()
    if choice.lower() == 'n':
        os.remove(file_path)
        print(f"File {file_path} has been deleted.")
    else:
        # TODO: pas ouf de faire ça ici
        with open(file_path.replace('.csv', '.seq'), 'wt') as file:
            for step in sequence:
                file.write(f"{step[0]}:{step[1]}\n")
        print(f"File {file_path} has been saved.")


def listen(config: dict, file_path: str):
    try:
        bus = can.Bus(interface=config['BUS']['interface'],
                    channel=config['BUS']['channel'],
                    receive_own_messages=True)

        file = open(file_path, 'wt')
        writer = can.CSVWriter(file)
        notifier = can.Notifier(bus, [writer])

        return writer, file, notifier, bus
        
    except Exception as e:
        print(f"Error while listenning CAN BUS: {e}")
        if os.path.exists(file_path):
            os.remove(file_path)
        exit(1)


def dispose(writer, file, notifier, bus):
    notifier.stop()
    writer.stop()
    file.close()
    bus.shutdown()