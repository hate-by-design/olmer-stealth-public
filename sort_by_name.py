from py_stealth import *
from datetime import datetime as dt
import re

RULES = {
    "Forensics": 0x400FF777,
    "Cooking": 0x400FEF2B,
    "Inscription": 0x400FEE9F,
    "Mining": 0x400FEE8E,
    "Blacksmithing": 0x400FEEDF,
    "Tactics": 0x400FEF71,
    "Veterinary": 0x400FEF87,
    "Alchemy": 0x400FEEBE,
    "MagicResistance": 0x400FEF07,
    "Anatomy": 0x400FEF51,
    "Taming": 0x400FEEEE,
    "Lumberjacking": 0x400FEF75,
    "DetectingHidden": 0x400FEEF8,
    "Archery": 0x400FEF0D,
    "Tinkering": 0x400FEFA1,
    "Carpentry": 0x400FF0CC,
    "Tailoring": 0x400FEFB1,
    "ArmsLore": 0x400FF0DB,
    "AnimalLore": 0x400FF08A,
    "Stealth": 0x400FF0F2,
    "Fishing": 0x400FEF93,
    "Fencing": 0x400FF0A6,
    "Anatomy": 0x400FAFF7,
}

BOOKS_CONTAINER = 0x40212B61
BAGS_CONTAINER = 0x400FF99A
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
    for container in [BOOKS_CONTAINER, BAGS_CONTAINER] + list(RULES.values()):
        UseObject(container)
        Wait(200)    
    process()
