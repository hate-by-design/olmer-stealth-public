from py_stealth import *
from Scripts.types import Types
from datetime import datetime as dt

CRAFT_TYPE = Types.PICKAXE
ORE_INDEX = 4
RESOURCE_REQUIRED = 18
SELL_BOX = 0x40319F1C
BANK_BOX = 0x40319F30
BANK_COORDS = (5539, 1122)
SELL_COORDS = (5539, 1117)


ORE = {
    1: {
        "text": "Iron",
        "color": 0x0000
    },
    2: {
        "text": "Steel",
        "color": 0x0471
    },
    3: {
        "text": "Hiron",
        "color": 0x0515
    },
    4: {
        "text": "Malahit",
        "color": 0x022E
    },
    5: {
        "text": "Dull copper",
        "color": 0x0B82
    },
    6: {
        "text": "Shadow",
        "color": 0x0455
    },
    7: {
        "text": "Copper",
        "color": 0x0B83
    },
    8: {
        "text": "Brute",
        "color": 0x0474
    },
    9: {
        "text": "Crimson",
        "color": 0x0A11
    },

}


def craft_colored(crafting_type, color, count, menu, submenu):
    while CountEx(crafting_type, color, Backpack()) <= count:
        if resources_available(color):
            if MenuHookPresent():
                CancelMenu()

            _started = dt.now()
            UseType(Types.TINKER_TOOLS, 0xFFFF)
            WaitMenu("Tinkering", menu)
            WaitMenu(menu, submenu)
            WaitJournalLine(_started, "опыта|Заготовка", 10000)
        else:
            print(f"Failed to get resource from bank box | {submenu}")
            exit()
            #full_disconnect()



def get_from_bank(type, color):
    _bank_x, _bank_y = BANK_COORDS
    _sell_x, _sell_y = SELL_COORDS
    _success = False

    newMoveXY(_bank_x, _bank_y, True, 0, True)
    UseObject(BANK_BOX)
    Wait(500)
    _bank_container = LastContainer()
    if FindTypeEx(Types.INGOT, color, _bank_container):
        if FindQuantity() > 100:
            Grab(FindItem(), 100)
            Wait(100)
            _success = True                    

    newMoveXY(_sell_x, _sell_y, True, 0, True)    
    return _success

def resources_available(color):
    if FindTypeEx(Types.INGOT, color, Backpack()):
        if FindQuantity() > RESOURCE_REQUIRED:
            return True
        else:
            if get_from_bank(Types.INGOT, color):
                return True
    else:        
        if get_from_bank(Types.INGOT, color):
            return True

    return False 

def sell(color):
    if FindTypeEx(CRAFT_TYPE, color, Backpack()):
        for _ in range(FindCount()):
            _started = dt.now()
            UseObject(SELL_BOX)
            WaitTargetType(CRAFT_TYPE)
            WaitJournalLine(_started, "gold", 10000)
            

while not Dead():    
    for _current in range(1, ORE_INDEX + 1):
        _current_ore = ORE[_current]
        print(_current_ore["text"])
        print(
            f"make_tool(crafting_type={Types.PICKAXE}, color={_current_ore['color']}, count={3}, menu=Pickaxes, submenu={_current_ore['text']} Pickaxe)")
        if _current == 1:
            craft_colored(
                Types.PICKAXE, _current_ore["color"], 3, "Pickaxes", "Pickaxe")
            Wait(500)
        else:
            craft_colored(
                Types.PICKAXE, _current_ore["color"], 3, "Pickaxes", f"{_current_ore['text']} pickaxe")
            Wait(500)
                               
    sell(_current_ore["color"])
    Wait(100)
