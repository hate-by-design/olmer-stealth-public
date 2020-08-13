from py_stealth import *
from Scripts.types import Types
from datetime import datetime as dt
import re
import os

# Changeable
FORGE_COORDS = (186, 621)
PROMETHEUS = 1
KEEP_TOOLS = 1
KILL_ELEMENTALS = 0
KEEP_BANDAGES = 100
FILE_NAME="mining"
MINE_COORDS = [
    (192, 592),
    (191, 579),
    (179, 579),
    (176, 566),
    (188, 560),
    (176, 556),
    (188, 554)
]
CHEST = 0x4018C655
TILE_SEARCH_RANGE = 8
# 
LOOT = [0x19B7, 0x19B8, 0x19BA, Types.GOLD_COIN,
        Types.ORE, 0x0F8E, 0x0E35, 0x0FEF]
ROCK = 0x1779
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

MINEABLE_TILES = [1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351, 1352,
             1353, 1354, 1355, 1356, 1357, 1358, 1359, 1361, 1362, 1363, 1386, 581, 582]



def cancel_targets():
    CancelWaitTarget()
    if TargetPresent():
        CancelTarget()

def full_disconnect():
    print("Disconnected")
    SetARStatus(False)
    Disconnect()

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

def bandages_available() -> bool:
    if FindType(Types.BANDAGES, Backpack()):
        if FindQuantity() > 20:
            return True
    return False

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
        smelt()
        unload()
        _x, _y = MINE_COORDS[0]
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


def elemental_around() -> int:
    if FindType(0x003A, Ground()):
        return FindItem()
    return 0

def loot():
    if FindType(0x2006, Ground()):
        corpse = FindItem()
        newMoveXY(GetX(corpse), GetY(corpse), True, 0, True)
        UseObject(corpse)
        Wait(100)
        if FindTypesArrayEx(LOOT, [0xFFFF], [FindItem()], False):
            for _item in GetFindedList():
                Grab(_item, 0)
                Wait(1000)


def kill_elemental(elemental: int):
    print("Killing isonite elemental...")
    while GetHP(elemental) > 0:
        newMoveXY(GetX(elemental), GetY(elemental), True, 1, True)
        Attack(elemental)
        Wait(500)        

def restock():
    if Count(Types.PICKAXE) < KEEP_TOOLS:
        if FindType(Types.PICKAXE, CHEST):
            if FindCount() > KEEP_TOOLS:
                _got = 0
                for _item in GetFindedList():
                    print("Getting new pickaxe")
                    _got += 1                    
                    Grab(_item, 1)
                    Wait(1000)
                    if _got >= KEEP_TOOLS:
                        return True
            return False
        return False
    return True


def get_bandages():
    if FindType(Types.BANDAGES, LastContainer()):
        if FindQuantity() > KEEP_BANDAGES:
            Grab(FindItem(), KEEP_BANDAGES)
            Wait(500)            

def unload():
    _unload_x, _unload_y = FORGE_COORDS
    if move_to(_unload_x, _unload_y):                
        UseObject(CHEST)        
        Wait(500)


        if not restock():
            print("No more tools left in chest!")
            full_disconnect()

        for _type in [Types.INGOT, Types.GOLD_INGOT, Types.SILVER_INGOT]:
            if FindType(_type, Backpack()):
                for _item in GetFoundList():
                    MoveItem(_item, 0, LastContainer(), 0, 0, 0)
                    Wait(500)

        if PROMETHEUS == 1:
            to_prometheus()

        if KILL_ELEMENTALS == 1:
            get_bandages()
            # Unload loot from elementals
            if FindTypesArrayEx(LOOT, [0xFFFF], [Backpack()], False):
                for _loot_item in GetFoundList():
                    MoveItem(_loot_item, 0, LastContainer(), 0, 0, 0)
                    Wait(500)

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
    _data = []
    # Collect data to reduce spaces in metrics
    # Yeah, gold ingot has different type =\
    for _type in [Types.INGOT, Types.GOLD_INGOT, Types.SILVER_INGOT]:
        if FindType(_type, LastContainer()):
            for _ingot in GetFoundList():
                _ingot_name, _ingot_qty = get_item_name(_ingot, "ingot")
                if _ingot_name != "error":
                    _data.append((_ingot_name, _ingot_qty))

    # Workaround for bricks   
    if FindTypeEx(Types.INGOT, 0x04E8, LastContainer()):
        _brick, _qty = get_item_name(FindItem(), "Brick")
        if _brick != "error":
            _data.append((_brick, _qty))

    # Pickaxes info
    if FindType(Types.PICKAXE, LastContainer()):
        _data.append(("pickaxe", FindCount()))

    # To empty file lulz    
    open(FILE_NAME, 'w').close()
    # Now we can append some data...
    with open(FILE_NAME, "a") as _to_exporter:        
        for _set in _data:
            _ingot, _qty = _set
            _to_exporter.write(f"{_ingot}={_qty}\n")
    _to_exporter.close()

def crash_rocks():
    if FindType(ROCK, Backpack()):
        for _rock in GetFindedList():
            cancel_targets()
            UseObject(ObjAtLayer(RhandLayer()))
            WaitForTarget(2000)
            if TargetPresent():
                WaitTargetObject(FindItem())
                Wait(1000)                

def mine():
    for _tile_data in find_tiles(TILE_SEARCH_RANGE):
        _tile, _x, _y, _z = _tile_data
        while not Dead():
            # Overload?     
            if Weight() >= MaxWeight() - 20:
            #if Weight() >= 200:
                smelt()                                
                unload()                    
                move_to(_x, _y)

            # You can't mine so close to yourself 
            if newMoveXY(_x, _y, True, 1, True):
                if GetX(Self()) == _x and GetY(Self()) == _y:
                    newMoveXY(_x + 1, _y, True, 0, True)

                # Prepare to fight ^W dig
                equip_tool()
                crash_rocks()
                # Kill some elementals
                if KILL_ELEMENTALS == 1:
                    elemental = elemental_around()
                    if elemental > 0 and bandages_available():
                        kill_elemental(elemental)
                        loot()
                        SetWarMode(False)
                #
                cancel_targets()
                                
                _started = dt.now()
                UseObject(ObjAtLayer(RhandLayer()))
                WaitForTarget(2000)
                if TargetPresent():
                    WaitTargetTile(_tile, _x, _y, _z)
                    WaitJournalLine(_started, "|".join(
                        SKIP_TILE_MESSAGES + NEXT_TRY_MESSAGES), 50000)

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
SetFindDistance(20)

smelt()
unload()
#exit()


while not Dead():
    for point in MINE_COORDS:
        point_x, point_y = point
        move_to(point_x, point_y)        
        mine()


