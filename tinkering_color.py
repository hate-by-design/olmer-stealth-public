from py_stealth import *
from Scripts.types import Types
from datetime import datetime as dt
RESOURCE_REQUIRED = 18
TOOLS_REQUIRED = 3
BANK_BOX = 0x40319F30
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
    }

}


def get_ore_number(text: str) -> int:
    for _index in ORE:        
        if ORE[_index]["text"] == text:
            return _index
    return 0


def make_tool(crafting_type, color, count, menu, submenu):
    while CountEx(crafting_type, color, Backpack()) < count:
        if get_resource_from_bank(color, RESOURCE_REQUIRED):
            if MenuHookPresent():
                CancelMenu()

            _started = dt.now()
            UseType(Types.TINKER_TOOLS, 0xFFFF)
            WaitMenu("Tinkering", menu)
            WaitMenu(menu, submenu)
            WaitJournalLine(_started, "опыта|Заготовка", 10000)
            CloseMenu()
        else:
            print("Failed to get resource from bank box")
            # TODO: Disconnect

def get_resource_from_bank(color: int, qty: int) -> bool:
    UseObject(BANK_BOX)
    Wait(500)
    if FindTypeEx(Types.INGOT, color, LastContainer()):
        if FindQuantity() > qty:
            Grab(FindItem(), qty)
            Wait(500)
            return True
    return False


def craft_colored_tool(index, count):    
    for _current in range(1, index + 1):
        print(f"Current: {_current}")
        _current_ore = ORE[_current]
        print(f"make_tool(crafting_type={Types.PICKAXE}, color={_current_ore['color']}, count={count}, menu=Pickaxes, submenu={_current_ore['text']} Pickaxe)")
        if _current == 1:
            make_tool(Types.PICKAXE, _current_ore["color"],
                      count, "Pickaxes", "Pickaxe")
            Wait(500)
        else:
            make_tool(Types.PICKAXE, _current_ore["color"],
                    count, "Pickaxes", f"{_current_ore['text']} pickaxe")
            Wait(500)


for i in range(3):
    print(i)
#craft_colored_tool(3, TOOLS_REQUIRED)

