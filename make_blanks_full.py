from py_stealth import *
from datetime import datetime as dt

#### Feel free to change for your needs
# Откуда брать ресурсы ( если с земли - то Ground() )
LOG_CONTAINER = 0x404F15D3 
CLOTH_CONTAINER = Ground()
LEATHER_CONTAINER = Ground()
# Куда складывать бланк скроллы ( лучше в контейнер, на пол не тестил )
UNLOAD_CONTAINER = 0x404F15D3
# Тулзы для карпентри, у меня была пила
SAW_TYPE = 0x1034
####

#### Basic types
PAPER = 0x0E34
PAPER_COLOR = 0x000
PARCHMENT_COLOR = 0x0462
BLANK_SCROLL_COLOR = 0x034B
CLOTH = 0x175D
LOG = 0x1BE0
LEATHER = 0x1067
####

def open_containers():
    for _container in [LOG_CONTAINER, CLOTH_CONTAINER, LEATHER_CONTAINER, UNLOAD_CONTAINER]:
        if _container > 0 and IsObjectExists(_container) and IsContainer(_container):
            UseObject(_container)
            Wait(100)

def get_resource(resource: int, to_keep: int, container: int, name: str) -> bool:
    _result = False    
    if FindTypeEx(resource, 0x0000, container):
        if FindFullQuantity() >= to_keep:
            print(f"{name} left: {FindFullQuantity() - to_keep}")
            Grab(FindItem(), to_keep)
            Wait(500)
            _result = True            
    return _result
    
def restock() -> bool:
    _result = True
    
    if not FindType(LOG, Backpack()) or FindFullQuantity() < 50:
        if not get_resource(LOG, 50, LOG_CONTAINER, "Logs"):
            _result = False
    
    if not FindType(CLOTH, Backpack()) or FindFullQuantity() < 50:
        if not get_resource(CLOTH, 50, CLOTH_CONTAINER, "Cloth"):
            _result = False

    if not FindType(LEATHER, Backpack()) or FindFullQuantity() < 50:
        if not get_resource(LEATHER, 50, LEATHER_CONTAINER, "Leather"):
            _result = False

    return _result

def unload():
    if FindTypeEx(PAPER, BLANK_SCROLL_COLOR, Backpack()):        
        MoveItem(FindItem(), 0, UNLOAD_CONTAINER, 0, 0, 0)
        Wait(500)
        if FindTypeEx(PAPER, BLANK_SCROLL_COLOR, UNLOAD_CONTAINER):
            print(f"Blank scrolls: {FindFullQuantity()}")


def craft_item(tool: int, tool_color: int, menu: str, submenu: str):
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

    WaitMenu(menu, submenu)
    WaitMenu(submenu, submenu)
    WaitJournalLine(_started, "опыта|Заготовка", 10000)
    CloseMenu()

def get_item_quantity(type: int, color: int, container: int):
    _qty = 0
    if FindTypeEx(type, color, container):
        _qty = FindFullQuantity()
    return _qty


def craft_quantity(tool: int, tool_color:int, menu: str, submenu: str, craft_type: int, color: int, qty: int):
    while get_item_quantity(craft_type, color, Backpack()) < qty:        
        craft_item(tool, tool_color, menu, submenu)
        Wait(100)
        

if __name__ == "__main__":
    while not Dead():
        open_containers()
        if not restock():
            while not restock():
                print("Failed to restock, out of resources ?")
                Wait(1000)
            #SetARStatus(False)
            #Disconnect()

        craft_quantity(SAW_TYPE, 0x0000, "Carpentry", "Paper", PAPER, PAPER_COLOR, 20)
        craft_quantity(SAW_TYPE, 0x0000, "Carpentry", "Parchment", PAPER, PARCHMENT_COLOR, 10)
        craft_quantity(PAPER, PARCHMENT_COLOR, "Inscription", "Blank", PAPER, BLANK_SCROLL_COLOR, 5)
        unload()
