from py_stealth import *
from Scripts.types import Types
from datetime import datetime as dt
import re
import os

# Changeable
BANK_COORDS = (5539, 1122)
PROMETHEUS = 1
KEEP_TOOLS = 2
FILE_NAME="lumber"
FIELDS_COORDS = [
    (5502, 1218),
    (5503, 1243),
    (5510, 1288),
    (5518, 1263),
    (5552, 1246),
    (5537, 1283),
    (5576, 1279),
    (5625, 1282),
    (5626, 1258),
    (5629, 1243)
]
CHEST = 0x40319F30
TILE_SEARCH_RANGE = 10
# 
SKIP_TILE_MESSAGES = [
    "There is nothing",
    "You have no line",    
    "You can't see",
    "Try chopping",
    "It appears immune"
        
]

NEXT_TRY_MESSAGES = [
    "Ваш инструмент",
    "Нарубленные дрова",    
    "You decide not",  # Alt-tab protection
]

TREE_TILES = [3274, 3275, 3277, 3280, 3283, 3287, 3286, 3288, 3290, 3293, 3296, 3320, 3323, 3326, 3329, 3393, 3394, 3395,
              3396, 3415, 3416, 3418, 3419, 3438, 3439, 3440, 3441, 3442, 3460, 3461, 3462, 3476, 3478, 3480, 3482, 3484, 3492, 3496]



def cancel_targets():
    CancelWaitTarget()
    if TargetPresent():
        CancelTarget()

def full_disconnect():
    print("Disconnected")
    SetARStatus(False)
    #Disconnect()

def find_tiles(radius) -> list:    
    _tiles_coordinates = []    
    for _tile in TREE_TILES:
        _tiles_coordinates += GetLandTilesArray(GetX(Self()) - radius, GetY(Self()) - radius, GetX(Self()) + radius,
                                 GetY(Self()) + radius, WorldNum(), _tile)
                                 
        _tiles_coordinates += GetStaticTilesArray(GetX(Self()) - radius, GetY(Self()) - radius, GetX(Self()) + radius,
                                     GetY(Self()) + radius, WorldNum(), _tile)
                                     
    print("[FindTiles] Found "+str(len(_tiles_coordinates))+" tiles")
    return _tiles_coordinates


def tool_available() -> bool:
    if FindType(Types.HATCHET, Backpack()):
        return True
    return False


def equip_tool() -> bool:
    if tool_available():
        _left_hand = ObjAtLayer(LhandLayer())
        if _left_hand > 0:
            if GetType(_left_hand) != Types.HATCHET:            
                UnEquip(LhandLayer())
                Wait(500)
                UseType(Types.HATCHET, 0xFFFF)
                Wait(500)
        else:
            UseType(Types.HATCHET, 0xFFFF)
            Wait(500)
    else:
        unload()
        _x, _y = FIELDS_COORDS[0]
        move_to(_x, _y)


def move_to(x: int, y: int) -> bool:
    _try = 0    
    while GetX(Self()) != x or GetY(Self()) != y:
        newMoveXY(x, y, True, 0, True)
        _try += 1
        if _try > 10:
            print(f"[move_to] Can't reach X: {x} Y: {y}")
            return False            
    return True

def restock():
    if Count(Types.HATCHET) < KEEP_TOOLS:
        if FindType(Types.HATCHET, LastContainer()):
            if FindCount() > KEEP_TOOLS:
                _got = 0
                for _item in GetFindedList():
                    _got += 1                    
                    Grab(_item, 1)
                    Wait(1000)
                    if _got >= KEEP_TOOLS:
                        return True
        return False
    return True

def unload():
    _unload_x, _unload_y = BANK_COORDS
    if move_to(_unload_x, _unload_y):                
        UseObject(CHEST)        
        Wait(500)

        if not restock():
            print("No more tools left in chest!")
            full_disconnect()

        for _type in [Types.LOG]:
            if FindType(_type, Backpack()):
                for _item in GetFoundList():
                    MoveItem(_item, 0, LastContainer(), 0, 0, 0)
                    Wait(500)
        if PROMETHEUS == 1:
            to_prometheus()


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
    _data = []
    # Collect data to reduce spaces in metrics    
    for _type in [Types.LOG]:
        if FindType(_type, LastContainer()):
            for _log in GetFoundList():
                _log_name, _log_qty = get_item_name(_log, "logs|Logs")
                if _log_name != "error":
                    _data.append((_log_name, _log_qty))

    # HATCHETs info
    if FindType(Types.HATCHET, LastContainer()):
        _data.append(("hatchet", FindCount()))

    # To empty file lulz    
    open(FILE_NAME, 'w').close()
    # Now we can append some data...
    with open(FILE_NAME, "a") as _to_exporter:        
        for _set in _data:
            _log, _qty = _set
            _to_exporter.write(f"{_log}={_qty}\n")
    _to_exporter.close()       

def chop():
    for _tile_data in find_tiles(TILE_SEARCH_RANGE):
        _tile, _x, _y, _z = _tile_data
        while not Dead():
            # Overload?     
            if Weight() >= MaxWeight() - 20:            
                unload()                    
                move_to(_x, _y)
                
            if newMoveXY(_x, _y, True, 1, True):    
                # Prepare to fight ^W chop
                equip_tool()                
                cancel_targets()                                

                _started = dt.now()
                UseObject(ObjAtLayer(LhandLayer()))
                WaitForTarget(2000)
                if TargetPresent():
                    WaitTargetTile(_tile, _x, _y, _z)
                    WaitJournalLine(_started, "|".join(
                        SKIP_TILE_MESSAGES + NEXT_TRY_MESSAGES), 60000)

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


unload()
while not Dead():
    for field in FIELDS_COORDS:
        field_x, field_y = field
        move_to(field_x, field_y)
        chop()
