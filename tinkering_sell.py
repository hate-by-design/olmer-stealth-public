from py_stealth import *
from Scripts.types import Types
from datetime import datetime as dt

CRAFT_TYPE = 0x1004
CRAFT_COLOR = 0x0000
SELL_BOX = 0x40319F1C
BANK_BOX = 0x40319F30
BANK_COORDS = (5539, 1122)
SELL_COORDS = (5539, 1117)

def craft(target, count, menu, submenu):
    while Count(target) < count:
        if resources_available():
            if MenuHookPresent():
                CancelMenu()

            _started = dt.now()
            UseType(Types.TINKER_TOOLS, 0xFFFF)
            WaitMenu("Tinkering", menu)
            WaitMenu(menu, submenu)
            WaitJournalLine(_started, "опыта|Заготовка", 10000)        


def get_from_bank(type, color):
    _bank_x, _bank_y = BANK_COORDS
    _sell_x, _sell_y = SELL_COORDS
    _success = False

    newMoveXY(_bank_x, _bank_y, True, 0, True)
    UseObject(BANK_BOX)
    Wait(500)
    _bank_container = LastContainer()
    if FindTypeEx(Types.INGOT, CRAFT_COLOR, _bank_container):
        if FindQuantity() > 100:
            Grab(FindItem(), 100)
            Wait(100)
            _success = True                    

    newMoveXY(_sell_x, _sell_y, True, 0, True)    
    return _success

def resources_available():
    if FindTypeEx(Types.INGOT, CRAFT_COLOR, Backpack()):
        if FindQuantity() > 10:
            return True
        else:
            if get_from_bank(Types.INGOT, 0x0000):
                return True
    else:        
        if get_from_bank(Types.INGOT, 0x0000):
            return True

    return False 

def sell():
    if FindTypeEx(CRAFT_TYPE, CRAFT_COLOR, Backpack()):
        for _ in range(FindCount()):
            _started = dt.now()
            UseObject(SELL_BOX)
            WaitTargetType(CRAFT_TYPE)
            WaitJournalLine(_started, "gold", 10000)
            

while not Dead() and resources_available():    
    craft(CRAFT_TYPE, 10, "Parts", "Tap barrel")
    sell()
    Wait(100)
