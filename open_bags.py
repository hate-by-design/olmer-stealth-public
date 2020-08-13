from py_stealth import *
from datetime import datetime as dt

LOCKPICKS = 0x14FB
BAG_TYPES = [0x0E75, 0x0E79, 0x09B0]
BAG_COLOR = 0x0324
## Сундук с сумками 
BAG_CONTAINER = 0x4018C66B

REG_BAG = 0x0E79
REAGENTS = [0X0F7A,0x0F7B,0x0F84,0x0F85,0x0F86,0x0F88,0x0F8C,0x0F8D]

def tool_available():
    if Count(LOCKPICKS) > 0:
        return True    
    return False


def cancel_targets():
    CancelWaitTarget()
    if TargetPresent():
        CancelTarget()

def is_bag_closed(serial):
    _started = dt.now()
    ClickOnObject(serial)
    Wait(500)
    if InJournalBetweenTimes("Закрыт", _started, dt.now()) > 0:
        return True    
    return False

def get_reagents(serial):
    Grab(serial, 1)
    Wait(500)
    UseObject(serial)
    Wait(500)
    if FindTypesArrayEx(REAGENTS, [0xFFFF], [Backpack()], False):
        for _reagent in GetFoundList():
            MoveItem(_reagent, 0, BAG_CONTAINER, 0, 0, 0)
            Wait(500)


def process():    
    if FindTypesArrayEx(BAG_TYPES, [0xFFFF], [BAG_CONTAINER], False):
        for _bag in GetFoundList():
            while is_bag_closed(_bag):
                if tool_available():
                    cancel_targets()                    
                    _started = dt.now()            
                    UseType(LOCKPICKS, 0xFFFF)
                    WaitForTarget(1000)
                    WaitTargetObject(_bag)
                    WaitJournalLine(_started, "Замок показался|Вам удалось", 1000)
                else:
                    print("No more lockpicks left")
                    exit()
            if GetType(_bag) == 0x0E79:
                get_reagents(_bag)                


if __name__ == "__main__":
    UseObject(BAG_CONTAINER)
    Wait(1000)    
    process()
