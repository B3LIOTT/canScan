import can
import os

"""
The dumper module is listenning to the CAN bus and writes the messages to a CSV file.
This CSV file will be analyzed later by the analyser module.
"""


def end_checks(file_path: str, sequence: list, delta: float, componentIndex: int):
    print(f"File {file_path} has been created.")
    print('Do you want to save it ? (o/n)')
    choice = input()
    if choice.lower() == 'n':
        os.remove(file_path)
        print(f"File {file_path} has been deleted.")
    else:
        # TODO: do not do this here
        with open(file_path.replace('.csv', '.seq'), 'wt') as file:
            file.write(f"{delta}:{componentIndex}\n")
            for step in sequence:
                file.write(f"{step[0]}:{step[1].value}\n")
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