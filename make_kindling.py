from py_stealth import *
from datetime import datetime as dt

CONTAINER = 0x404F15D3
LOGS = 0x1BE0
KINDLING = 0x0DE1


def resource_available(resource: int, container: int) -> bool:
    if FindType(resource, container):
        if FindFullQuantity() > 100:
            return True
    return False

def restock() -> bool:
    if resource_available(LOGS, CONTAINER):        
        Grab(FindType(LOGS, CONTAINER), 100)
        Wait(1000)
        return True
    return False

def unload():
    if resource_available(KINDLING, Backpack()):
        MoveItem(FindType(KINDLING, Backpack()), 0, CONTAINER, 0, 0, 0)
        Wait(1000)

if __name__ == "__main__":
    while not Dead():
        if resource_available(LOGS, Backpack()):
            _started = dt.now()
            UseType(LOGS, 0x0000)
            AutoMenu("Bowcraft", "щепки")
            WaitJournalLine(_started, "опыт", 10000)
            unload()
        else:
            if not restock():
                print("No more resources left")
                exit()
