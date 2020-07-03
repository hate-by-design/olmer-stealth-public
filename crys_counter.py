from py_stealth import *
from datetime import datetime as dt
import re

CRYSTONE = 0x1F1C
CRYSTONE_DICT = {}
CONTAINER = LastContainer()


def get_item_name(item_serial, message):    
    _started = dt.now()
    ClickOnObject(item_serial)
    Wait(500)
    _journal_line = InJournalBetweenTimes(message, _started, dt.now())
    if _journal_line > 0:
        _match = re.search(r"{(.+)}", Journal(_journal_line))
        if _match:
            return _match.group(1)
                    
    return "Error"                


if __name__ == "__main__":    
    if FindType(CRYSTONE, CONTAINER):
        for _item in GetFoundList():
            _name = get_item_name(_item, "Crystone")
            if _name in CRYSTONE_DICT:                
                CRYSTONE_DICT[_name] = CRYSTONE_DICT[_name] + 1
            else:
                CRYSTONE_DICT.update({_name: 1})

    data_sorted = {k: v for k, v in sorted(CRYSTONE_DICT.items(), key=lambda x: x[1])}
    
    for name, qty in CRYSTONE_DICT.items():
        print(f"{name}: {qty}")
