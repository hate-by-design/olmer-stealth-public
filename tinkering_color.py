from py_stealth import *
from Scripts.types import Types
from datetime import datetime as dt
RESOURCE_REQUIRED = 12
TOOLS_REQUIRED = 1
BANK_BOX = 0x4018C655
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


def get_ore_number(text: str) -> int:
    for _index in ORE:        
        if ORE[_index]["text"] == text:
            return _index
    return 0


def make_tool(crafting_type, color, count, menu, submenu):
    print (f"make_tool(crafting_type={crafting_type}, color={color}, count={count}, menu={menu}, submenu={submenu})")
    while CountEx(crafting_type, color, Backpack()) < count:
        if get_resource_from_bank(color, RESOURCE_REQUIRED):
            if MenuHookPresent():
                CancelMenu()

            _started = dt.now()
            UseType(Types.TINKER_TOOLS, 0xFFFF)
            Wait(200)
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

def craft_colored_tool(index, count, menu, submenu_part, tool_type):
    for _current in range(1, index + 1):
        print(f"Current: {_current}")
        _current_ore = ORE[_current]        
        if _current == 1:
            make_tool(tool_type, _current_ore["color"],count, menu, submenu_part)
            Wait(500)
        else:
            make_tool(tool_type, _current_ore["color"],count, menu, f"{_current_ore['text']} {submenu_part}")
            Wait(500)



craft_colored_tool(9, 1, "Smith hammers", "smith hammer", Types.SMITHING_HAMMER)