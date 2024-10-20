from models import Component, ComponentType, SignalType
from modules.dumper import *
from time import sleep
import random
import json
import os

"""
The Maestro module is the one which orchestrates CAN messages sended by the user.
The user wants to find which messages are sent by the ECU when he presses the brake pedal for example.
Maestro will create a specific sequence, and the user has to reproduce it.
Then, the analyzer can easily find the specific sequence (if the user isn't too bad at reproducing it).
"""

SIZE = 15

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def orchestrates_sequence(component: Component, sequence, default_msg, rep: bool):
    watch_m = "Watch this sequence"
    rep_m = "Reproduce this sequence"
    m = f"{watch_m if not rep else rep_m}"
    print(m)

    init_line = "-" * SIZE
    messages = [default_msg] * SIZE
    for step in sequence:
        messages[step[0]] = step[1]
        init_line = init_line[:step[0]] + "X" + init_line[step[0]+1:]
    
    line = ""
    try:
        if rep:
            print("Listening to CAN bus...")
            config, file_path = load_config()
            zoomies = listen(config=config, file_path=file_path)
            sleep(0.5)
            print("Ready to record the sequence.\n")

        for i in range(SIZE):
            clear_terminal()
            line = init_line[:i] + "." + init_line[i+1:]
            print(f"{m}:\n{line}\n\t{messages[i]}")
            sleep(1)

        if not rep:
            input("Press Enter to reproduce the sequence.")
            orchestrates_sequence(component, sequence, default_msg, True)

        else:
            dispose(*zoomies)
            again = input("Do you want to try again ? (o/n) > ")
            if again.lower() == "o":
                os.remove(file_path)
                orchestrates_sequence(component, sequence, default_msg, True)

            end_checks(file_path, sequence)
            print("Sequence reproduced, use the analyzer to determine the ID of the component.")

    except KeyboardInterrupt:
        dispose(*zoomies)
        raise Exception("User interrupted.")  

    return


def generate_sequence(component: Component):
    if component.ctype == ComponentType.AllOrNothing:
        print("Generating a random sequence for AllOrNothing component.")
        input("Press Enter to continue...")
        default_msg = "release"
        if component.stype == SignalType.Instant:
            seq = [(2, "press"), (4, "press"), (5, "press"), (8, "press"), (10, "press"), (12, "press")]
        else: 
            seq = [(i, "activate") for i in range(1, 5)] + [(i, "activate") for i in range(7, SIZE-2)]

        return orchestrates_sequence(component, seq, default_msg, False)
    
    elif component.ctype == ComponentType.Continuous:
        print("Generating a random sequence for Continuous component.")
        input("Press Enter to continue...")
        default_msg = "go to initial position and wait"
        seq = [(i, "increment progressively") for i in range(1, 5)] + [(i, "increment progressively") for i in range(8, SIZE-2)]

        return orchestrates_sequence(component, seq, default_msg, False)

    raise NotImplementedError("Only AllOrNothing component is implemented.")
    

def choose_component(components: list[Component]):
    print("Choose a component:")
    for i, component in enumerate(components):
        print(f"{i+1}. {component.name}")

    try:
        choice = int(input("> "))
        assert choice > 0 and choice <= len(components)
    except KeyboardInterrupt:
        raise Exception("User interrupted.")
    except ValueError:
        raise ValueError("Invalid choice.")

    comp = components[choice-1]
    print(f"Component {comp.name} choosen.")
    return generate_sequence(comp)


def load_components(components: dict):
    comps = []
    for component in components:
        comps.append(Component(name=component['name'], ctype=ComponentType(component['type']), stype=SignalType(component['signal'])))

    return comps


def wake_up_maestro():
    try:
        with open("components.json", "r") as file:
            file_content = file.read()

        json_comps = json.loads(file_content)
        comps = load_components(json_comps)
    
    except FileNotFoundError:
        raise FileNotFoundError("File components.json not found.")
    except json.JSONDecodeError:
        raise json.JSONDecodeError("Invalid components.json file.")
    except Exception as e:
        raise Exception(f"Error when Maestro woke up: {e}")

    print("Maestro is ready to guide you.")
    return choose_component(comps)
