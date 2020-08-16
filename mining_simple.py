from py_stealth import *
from Scripts.types import Types
from datetime import datetime as dt
import re
import os

# Changeable
FORGE_COORDS = (5545, 1229)
BANK_COORDS = (5539, 1122)

# How much tools we have to keep in pack ( not including one in hand )
TOOLS_REQUIRED = 2
# Index of required ore in ORE dict
TOOL_INDEX = 9

PROMETHEUS = 1
FILE_NAME="mining"

MINE_COORDS = [
    (5554, 1234),
    (5515, 1250),
    (5549, 1260)
]

BANK_BOX = 0x40319F30
TILE_SEARCH_RANGE = 12
# 

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
RESOURCE_REQUIRED = 18
SKIP_TILE_MESSAGES = [
    "There is nothing",
    "You have no line",
    "You decide not to mine",
    "Try mining",
    "You cannot mine"
]

NEXT_TRY_MESSAGES = [
    "Ваш инструмент",
    "Ничего полезного",
    "You loosen",
    "You decide not",  # Alt-tab protection
]

MINEABLE_TILES = [581, 582, 1343]


def cancel_targets():
    CancelWaitTarget()
    if TargetPresent():
        CancelTarget()

def full_disconnect():
    print("Disconnected")
    SetARStatus(False)
    Disconnect()


def drop_ore(index):
    # TODO: Implement
    _ore = ORE[index]
    if FindTypeEx(Types.ORE, _ore["color"], Backpack()):
        DropHere(FindItem())
        Wait(500)


def find_tiles(radius) -> list:    
    _tiles_coordinates = []    
    for _tile in MINEABLE_TILES:
        _tiles_coordinates += GetLandTilesArray(GetX(Self()) - radius, GetY(Self()) - radius, GetX(Self()) + radius,
                                 GetY(Self()) + radius, WorldNum(), _tile)
                                 
        _tiles_coordinates += GetStaticTilesArray(GetX(Self()) - radius, GetY(Self()) - radius, GetX(Self()) + radius,
                                     GetY(Self()) + radius, WorldNum(), _tile)
                                     
    print("[FindTiles] Found "+str(len(_tiles_coordinates))+" tiles")
    return _tiles_coordinates


def tool_available() -> bool:
    if FindType(Types.PICKAXE, Backpack()):
        return True
    return False


def get_ore_number(text: str) -> int:
    for _index in ORE:
        if ORE[_index]["text"] == text:
            return _index
    return 0


def make_colored_tool(crafting_type, color, count, menu, submenu):
    while CountEx(crafting_type, color, Backpack()) <= count:
        if get_resource_from_bank(color, RESOURCE_REQUIRED):
            if MenuHookPresent():
                CancelMenu()

            _started = dt.now()
            UseType(Types.TINKER_TOOLS, 0xFFFF)
            WaitMenu("Tinkering", menu)
            WaitMenu(menu, submenu)
            WaitJournalLine(_started, "опыта|Заготовка", 10000)
        else:
            print(f"Failed to get resource from bank box | {submenu}")
            full_disconnect()


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
        _current_ore = ORE[_current]
        print(f"make_tool(crafting_type={Types.PICKAXE}, color={_current_ore['color']}, count={count}, menu=Pickaxes, submenu={_current_ore['text']} Pickaxe)")
        if _current == 1:
            make_colored_tool(
                Types.PICKAXE, _current_ore["color"], count, "Pickaxes", "Pickaxe")
            Wait(500)
        else:
            make_colored_tool(
                Types.PICKAXE, _current_ore["color"], count, "Pickaxes", f"{_current_ore['text']} pickaxe")
            Wait(500)

    

def equip_tool() -> bool:
    if tool_available():
        _right_hand = ObjAtLayer(RhandLayer())
        if _right_hand > 0:
            if GetType(_right_hand) != Types.PICKAXE:            
                UnEquip(RhandLayer())
                Wait(500)
                UseType(Types.PICKAXE, 0xFFFF)
                Wait(500)
        else:
            UseType(Types.PICKAXE, 0xFFFF)
            Wait(500)
    else:
        print("No more tools left")
        full_disconnect()


def move_to(x: int, y: int) -> bool:
    _try = 0    
    while GetX(Self()) != x or GetY(Self()) != y:
        newMoveXY(x, y, True, 0, True)
        _try += 1
        if _try > 10:
            print(f"[move_to] Can't reach X: {x} Y: {y}")
            return False            
    return True


def unload():
    _bank_x, _bank_y = BANK_COORDS    
    if move_to(_bank_x, _bank_y):
        UseObject(BANK_BOX)
        Wait(500)
        for _type in [Types.INGOT, Types.GOLD_INGOT]:
            if FindType(_type, Backpack()):
                for _item in GetFoundList():
                    MoveItem(_item, 0, LastContainer(), 0, 0, 0)
                    Wait(500)
        if PROMETHEUS == 1:
            to_prometheus()


def smelt():
    _forge_x, _forge_y = FORGE_COORDS
    if move_to(_forge_x, _forge_y):
        while FindType(Types.ORE, Backpack()):
            for _ in range(FindCount()):
                _started = dt.now()
                UseType(Types.ORE, 0xFFFF)
                WaitJournalLine(_started, "You smelt", 10000)


def get_item_name(item_serial, message):
    _started = dt.now()
    ClickOnObject(item_serial)
    Wait(500)
    _journal_line = InJournalBetweenTimes(message, _started, dt.now())
    if _journal_line > 0:        
        _match = re.search(r"(\d+)\s(\S+)", Journal(_journal_line))
        if _match:
            return (_match.group(2), _match.group(1))

    return ('error', 1)

def to_prometheus():
    # To empty file lulz    
    open(f"{FILE_NAME}", 'w').close()
    # Now we can append some data...
    with open(FILE_NAME, "a") as _to_exporter:        
        if FindType(Types.INGOT, LastContainer()):
            for _ingot in GetFoundList():
                _ingot, _qty = get_item_name(_ingot, "ingot")
                if _ingot != "error":
                    _to_exporter.write(f"{_ingot}={_qty}\n")

        _to_exporter.close()

def mine():
    for _tile_data in find_tiles(TILE_SEARCH_RANGE):
        _tile, _x, _y, _z = _tile_data
        while not Dead():            
            if Weight() >= MaxWeight() - 20:
                smelt()
                
                if Weight() >= MaxWeight() - 50:                                        
                    unload()
                    make_colored_tool(Types.TINKER_TOOLS, 0x0000, 2, "Tools", "Tinker")

                    #
                    _tools_count = CountEx(Types.PICKAXE, ORE[TOOL_INDEX]["color"], Backpack())
                    if _tools_count < TOOLS_REQUIRED:
                        craft_colored_tool(TOOL_INDEX, TOOLS_REQUIRED - _tools_count)
                    # 

                    _mine_x, _mine_y = MINE_COORDS[0]
                    move_to(_mine_x, _mine_y)

            if newMoveXY(_x, _y, True, 1, True):
                if GetX(Self()) == _x and GetY(Self()) == _y:
                    newMoveXY(_x + 1, _y, True, 0, True)

                equip_tool()                
                cancel_targets()                                

                _started = dt.now()
                UseObject(ObjAtLayer(RhandLayer()))
                WaitForTarget(2000)
                if TargetPresent():
                    WaitTargetTile(_tile, _x, _y, _z)
                    WaitJournalLine(_started, "|".join(
                        SKIP_TILE_MESSAGES + NEXT_TRY_MESSAGES), 40000)

                if InJournalBetweenTimes("|".join(SKIP_TILE_MESSAGES), _started, dt.now()) > 0:
                    break
            else:
                print(f"Can't reach X: {_x} Y: {_y}")
                break

        Wait(500)


# Initialization

SetARStatus(True)
SetPauseScriptOnDisconnectStatus(True)
SetWarMode(False)
SetMoveThroughNPC(20)


while not Dead():
    for point in MINE_COORDS:
        point_x, point_y = point
        move_to(point_x, point_y)        
        mine()



#smelt()
#unload()


