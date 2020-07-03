from py_stealth import *
from datetime import datetime as dt
from Scripts.types import Types

BAG_TYPE = 0x0E75
BAG_COLOR = 0x0324


def tool_available():
    if Count(Types.LOCKPICK) > 0:
        return True    
    return False


def cancel_targets():
    CancelWaitTarget()
    if TargetPresent():
        CancelTarget()

def is_bag_closed(serial):
    _started = dt.now()
    UseObject(serial)
    Wait(500)
    if InJournalBetweenTimes("Закрыт", _started, dt.now()) > 0:
        return True
    return False

def process():
    if FindTypeEx(BAG_TYPE, BAG_COLOR, Backpack()):
        for _bag in GetFoundList():
            while is_bag_closed(_bag):
                if tool_available():
                    cancel_targets()                    
                    _started = dt.now()            
                    UseType(Types.LOCKPICK, 0x0000)
                    WaitForTarget(1000)
                    WaitTargetObject(_bag)
                    WaitJournalLine(_started, "Замок показался|Вам удалось", 1000)
                else:
                    print("No more lockpicks left")
                    exit()

if __name__ == "__main__":
    process()
