from py_stealth import *
from datetime import datetime as dt
import re
#### Feel free to change for your needs
LOG_CONTAINER = 0x40286821
CLOTH_CONTAINER = Ground()
LEATHER_CONTAINER = Ground()
UNLOAD_CONTAINER = 0x40286821
SAW_TYPE = 0x1030
####

#### Basic types
PAPER = 0x0E34
EXP_SCROLL = 0x0E35
CLOTH = 0x175D
LOG = 0x1BE0
LEATHER = 0x1067
####

def open_containers():
    for _container in [LOG_CONTAINER, CLOTH_CONTAINER, LEATHER_CONTAINER, UNLOAD_CONTAINER]:
        if _container > 0 and IsObjectExists(_container) and IsContainer(_container):
            UseObject(_container)
            Wait(100)

def get_resource(resource: int, to_keep: int, container: int, name: str, color=0x0000) -> bool:
    _result = False    
    if FindTypeEx(resource, color, container):
        if FindFullQuantity() >= to_keep:
            print(f"{name} left: {FindFullQuantity() - to_keep}")
            Grab(FindItem(), to_keep)
            Wait(1000)
            _result = True            
    return _result
    
def restock(color: int) -> bool:
    _result = True
    
    if not FindTypeEx(LOG, color, Backpack()) or FindFullQuantity() < 100:
        if not get_resource(LOG, 100, LOG_CONTAINER, "Logs", color):
            _result = False
    
    if not FindType(CLOTH, Backpack()) or FindFullQuantity() < 100:
        if not get_resource(CLOTH, 100, CLOTH_CONTAINER, "Cloth"):
            _result = False

    if not FindType(LEATHER, Backpack()) or FindFullQuantity() < 100:
        if not get_resource(LEATHER, 100, LEATHER_CONTAINER, "Leather"):
            _result = False

    return _result

def unload():
    if FindType(EXP_SCROLL, Backpack()):        
        MoveItem(FindItem(), 0, UNLOAD_CONTAINER, 0, 0, 0)
        Wait(500)


def craft_item(tool: int, tool_color: int, menu: str, main_menu: str, submenu: str):
    _started = dt.now()
    if MenuHookPresent():
        CancelMenu()

    if MenuPresent():
        CloseMenu()
    
    if FindTypeEx(tool, tool_color, Backpack()):
        UseObject(FindItem())
        Wait(500)
    else:
        print("Failed to use tool... That should never happen btw xD")

    WaitMenu(menu, main_menu)
    WaitMenu(main_menu, submenu)
    WaitJournalLine(_started, "опыта|Заготовка", 10000)
    CloseMenu()

def get_item_quantity(type: int, color: int, container: int, item_name: str):
    _qty = 0
    if FindTypeEx(type, color, container):
        for _item in GetFoundList():
            #if get_item_name(_item) == item_name:
            if re.match(item_name, get_item_name(_item)):            
                _qty = GetQuantity(_item)
                print(f"{item_name} -> {_qty}")
    return _qty


def craft_quantity(tool: int, tool_color: int, menu: str, main_menu: str, submenu: str, craft_type: int, color: int, qty: int):    
    while get_item_quantity(craft_type, color, Backpack(), submenu) < qty:   
        craft_item(tool, tool_color, menu, main_menu, submenu)
        Wait(100)

def get_item_name(serial: int) -> str:
    if IsObjectExists(serial):
        ClickOnObject(serial)
        Wait(200)
        print(f" Obj name -> {GetName(serial)}")
        return GetName(serial)
    return ''

def get_logs_colors() -> list:
    _colors = []
    if FindType(LOG, LOG_CONTAINER):
        for _log in GetFoundList():
            if GetQuantity(_log) > 50 and GetColor(_log) > 0:
                _colors.append(GetColor(_log))
    return _colors

if __name__ == "__main__":
    SetARStatus(True)
    SetPauseScriptOnDisconnectStatus(True)
    SetWarMode(False)
    while not Dead():
        open_containers()
        for _color in get_logs_colors():
            if restock(_color):
                _log_name = get_item_name(FindTypeEx(LOG, _color, Backpack())).split(" ")[0]
                print(_log_name)                                
                craft_quantity(SAW_TYPE, 0x0000, "Carpentry", "Paper", f"{_log_name} paper", PAPER, _color, 20)
                craft_quantity(SAW_TYPE, 0x0000, "Carpentry", "Parchment", f"{_log_name} parchment", PAPER, _color, 10)
                craft_quantity(PAPER, _color, "Inscription", "Exp", f"{_log_name} exp", EXP_SCROLL, _color, 5)
                unload()
        Wait(1000)
