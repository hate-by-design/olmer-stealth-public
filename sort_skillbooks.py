from py_stealth import *
from datetime import datetime as dt
import re

RULES = {
    "Tinkering": 0x40483E69,
    "Blacksmithing": 0x40483ED4,
}

BOOKS_CONTAINER = 0x4059BE10
BAGS_CONTAINER = 0x2
BOOK_TYPE = 0x1C27

def get_skillbook_bonus(serial: int) -> str:
    _started = dt.now()
    if IsObjectExists(serial):
        ClickOnObject(serial)
        Wait(500)
        _journal_line = InJournalBetweenTimes("%", _started, dt.now())
        if _journal_line > 0:            
            _match = re.search(r"You\ssee:\s\d\.\d\%\s(.+)",Journal(_journal_line))
            if _match:                
                return _match.group(1)
    return ''

def get_container_for_skillbook(name: str) -> int:
    if name in RULES:
        print("ok")
        return RULES[name]
    return 0        

def process():
    if FindType(BOOK_TYPE, BOOKS_CONTAINER):
        for _book in GetFindedList():
            _name = get_skillbook_bonus(_book)
            _container = get_container_for_skillbook(_name)
            if _container > 0:
                print(f"Moving {_name}...")
                MoveItem(_book, 0, _container, 0, 0, 0)
                Wait(1000)
                

###
if __name__ == "__main__":
    for container in [BOOKS_CONTAINER, BAGS_CONTAINER]:
        UseObject(container)
        Wait(200)
    process()
