from enum import Enum


class ComponentType(Enum):
    AllOrNothing = 1
    Continuous = 2
    Discrete = 3

class SignalType(Enum):
    Instant = 1
    Periodic = 2

class Component:
    def __init__(self, name: str, ctype: ComponentType, stype: SignalType):
        self.name = name
        self.ctype = ctype
        self.stype = stype
        self.id = None
        self.values = []  # if continuous: [min, max], if discrete: [value1, value2, ...], if AllOrNothing: [unique value]
    
    def setID(self, id: int):
        self.id = id

    def addValue(self, value: int):
        self.values.append(value)

    def isDiscrete(self):
        return self.type == ComponentType.Discrete