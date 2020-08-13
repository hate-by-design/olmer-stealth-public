from py_stealth import *
from datetime import datetime as dt
import re

TO_REPAIR = 0x0E85

def item_durability(serial: int) -> tuple:
    _result = (0, 0)
    if IsObjectExists(serial):
        _started = dt.now()
        ClickOnObject(serial)
        Wait(100)
        _journal_line = InJournalBetweenTimes("/", _started, dt.now())
        if _journal_line > 0:
            _match = re.search(r"(\d+)/(\d+)", Journal(_journal_line))
            if _match:
                return (_match.group(1), _match.group(2))                        
    return _result


def repair_required(serial: int) -> bool:
    _min_durability, _max_durability = item_durability(serial)
    print(f"{_min_durability}/{_max_durability}")
    if _min_durability < _max_durability:        
        return True
    return False


def repair_item(serial: int):
    while repair_required(serial):
        _started = dt.now()
        WaitTargetObject(serial)
        UseSkill("Arms Lore")
        WaitJournalLine(_started, "Идеальное состояние|не выйдет", 100000)
        if FoundedParamID() == 1:
            break

if __name__ == "__main__":
    if FindType(TO_REPAIR, Backpack()):
        for _item in GetFindedList():
            repair_item(_item)
