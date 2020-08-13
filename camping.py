from py_stealth import *
from datetime import datetime as dt

KINDLING = 0x0DE1


def resource_available(resource: int, container: int) -> bool:
    if FindType(resource, container):        
        if FindFullQuantity() >= 10:            
            return True
    return False


def restock() -> bool:
    if resource_available(KINDLING, Ground()):
        FindType(KINDLING, Ground())        
        Grab(FindItem(), 10)
        Wait(1000)
        return True
    return False


if __name__ == "__main__":
    while not Dead():        
        if resource_available(KINDLING, Backpack()):            
            UOSay(".camp 2")
            Wait(10000)
        else:
            if not restock():
                print("No more resources left")
                exit()
