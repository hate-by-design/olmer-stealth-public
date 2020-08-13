from py_stealth import *
from datetime import datetime as dt

def close_all_gumps():
    for _index in range(0, GetGumpsCount()):
        CloseSimpleGump(_index)
        Wait(500)

def train():
    _try = 0
    _gump_count = GetGumpsCount()    
    UseSkill("Tracking")
    while _gump_count == GetGumpsCount():
        _try += 1
        if _try > 5:
            break;        
        Wait(100)
    close_all_gumps()
    _started = dt.now()
    UseSkill("Detect Hidden")
    WaitJournalLine(_started, "Ничего|Радиус", 10000)

    
    

if __name__ == "__main__":
    while not Dead():
        train()  
        Wait(100)