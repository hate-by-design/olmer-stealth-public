from py_stealth import *
from Scripts.types import Types
from datetime import datetime as dt

CRAFT_TYPE = 0x1413
SELL_BOX = 0x40319F1C
BANK_BOX = 0x40319F30
FORGE_COORDS = (5540, 1129)
BANK_COORDS = (5539, 1122)
SELL_COORDS = (5539, 1117)

def craft(target, count, menu, submenu):
    while Count(target) < count:
        if resources_available():
            if MenuHookPresent():
                CancelMenu()

            _started = dt.now()
            UseType(Types.INGOT, 0xFFFF)
            WaitMenu("Blacksmithing", menu)
            WaitMenu(menu, submenu)
            WaitJournalLine(_started, "опыта|Заготовка", 10000)   


def get_from_bank(type):
    _bank_x, _bank_y = BANK_COORDS
    _forge_x, _forge_y = FORGE_COORDS
    _success = False    
    newMoveXY(_bank_x, _bank_y, True, 0, True)    
    UseObject(BANK_BOX)
    Wait(500)
    _bank_container = LastContainer()
    if FindTypeEx(Types.INGOT, 0xFFFF, _bank_container):
        #if FindQuantity() > 100:
        Grab(FindItem(), 100)
        Wait(1000)
        _success = True
        
    if FindType(Types.GOLD_COIN, Backpack()):
        MoveItem(FindItem(), 0, _bank_container, 0, 0, 0)
        Wait(1000)
        
    newMoveXY(_forge_x, _forge_y, True, 0, True)
    return _success

def resources_available():
    if FindTypeEx(Types.INGOT, 0xFFFF, Backpack()):
        if FindQuantity() > 10:
            return True
        else:
            if get_from_bank(Types.INGOT):
                return True
    else:        
        if get_from_bank(Types.INGOT):
            return True

    return False 

def sell():
    _sell_x, _sell_y = SELL_COORDS
    _forge_x, _forge_y = FORGE_COORDS
    newMoveXY(_sell_x, _sell_y, True, 0, True)
    if FindTypeEx(CRAFT_TYPE, 0xFFFF, Backpack()):
        for _ in range(FindCount()):
            _started = dt.now()
            UseObject(SELL_BOX)
            WaitTargetType(CRAFT_TYPE)
            WaitJournalLine(_started, "gold", 10000)
    newMoveXY(_forge_x, _forge_y, True, 0, True)
            

while not Dead() and resources_available():
    craft(CRAFT_TYPE, 10, "platemail", "gorget")
    sell()
    Wait(100)
