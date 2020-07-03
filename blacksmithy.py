from py_stealth import *
from Scripts.types import Types
from datetime import datetime as dt

CRAFT_TYPE = 0x241C
INGOT_COLOR = 0x0000
CRAFT_COLOR = 0x03B9
FORGE = 0x406A7A75
BANK_BOX = 0x40319F30
BANK_COORDS = (5539, 1122)
FORGE_COORDS = (5540, 1129)

def craft(target, count, menu, submenu):
    while Count(target) < count:
        if resources_available():
            if MenuHookPresent():
                CancelMenu()

            _started = dt.now()
            UseType(Types.INGOT, 0x0000)
            WaitMenu("Blacksmithing", menu)
            WaitMenu(menu, submenu)
            WaitJournalLine(_started, "опыта|Заготовка", 10000)        


def get_from_bank(type, color):
    _bank_x, _bank_y = BANK_COORDS    
    _craft_x, _craft_y = FORGE_COORDS
    _success = False

    newMoveXY(_bank_x, _bank_y, True, 0, True)
    UseObject(BANK_BOX)
    Wait(500)
    _bank_container = LastContainer()
    if FindTypeEx(Types.INGOT, INGOT_COLOR, _bank_container):
        if FindQuantity() > 200:
            Grab(FindItem(), 200)
            Wait(100)
            _success = True                    

    newMoveXY(_craft_x, _craft_y, True, 0, True)
    return _success

def resources_available():
    if FindTypeEx(Types.INGOT, INGOT_COLOR, Backpack()):
        if FindQuantity() > 10:
            return True
        else:
            if get_from_bank(Types.INGOT, 0x0000):
                return True
    else:        
        if get_from_bank(Types.INGOT, 0x0000):
            return True

    return False 

def smelt():
    if FindTypeEx(CRAFT_TYPE, CRAFT_COLOR, Backpack()):
        _craft_x, _craft_y = FORGE_COORDS
        newMoveXY(_craft_x, _craft_y, True, 0, True)
        for _ in range(FindCount()):
            _started = dt.now()
            UseObject(FORGE)
            WaitTargetType(CRAFT_TYPE)
            WaitJournalLine(_started, "Вы переплавили", 10000)
            

while not Dead() and resources_available():        
    craft(CRAFT_TYPE, 10, "Metal spheres", "Broken")
    smelt()
    Wait(100)
