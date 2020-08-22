import re
from py_stealth import *
from datetime import datetime as dt

class Runebook:
    ''' Runebook class, requires runebook serial to be provdided '''

    def __init__(self, runebook_serial):
        ''' Init method, checks if runebook exists '''        
        self._close_all_gumps()
        
        if IsObjectExists(runebook_serial):
            self.runebook_serial = runebook_serial
        else:
           raise ValueError("[Runebook] No runebook found!")
                        
        _runebook_gump_id = self._find_runebook_gump_id()
        if _runebook_gump_id > 0:
            self.runebook_gump_id = _runebook_gump_id
        else:
            raise ValueError("[Runebook] Failed to get runebook gump id")


    def _find_runebook_gump_id(self) -> int:
        ''' Find runebook gump index ( using Rename book anchor ) '''
        self.open_runebook()
        for _index in range(0, GetGumpsCount()):
            for _text_line in GetGumpTextLines(_index):
                if re.match(r"Зарядов", _text_line):
                    print(f"[Runebook] Runebook gump id found! {hex(GetGumpID(_index))}")                    
                    return GetGumpID(_index)           
        return 0


    def _close_all_gumps(self):
        ''' Closes all gumps that can be closed by CloseSimpleGump '''
        for _index in range(0, GetGumpsCount()):            
            CloseSimpleGump(_index)
            Wait(500)


    def _press_gump_button(self, button=0):
        ''' Press specified button by id in runebook '''
        print(f"[Runebook] Pressing button {button}")
        for _index in range(0, GetGumpsCount()):            
            if GetGumpID(_index) == self.runebook_gump_id:
                NumGumpButton(_index, button)                
                Wait(500)

    def _close_runebook(self):
        ''' Close runebook '''
        for _index in range(0, GetGumpsCount()):
                if GetGumpID(_index) == self.runebook_gump_id:
                    CloseSimpleGump(_index)
                    Wait(500)

    def get_runebook_charges(self, max=0) -> int:
        ''' Returns current or maximum runebook charges 
            -1 if failed to get quantity            
        ''' 
        _charges = 0
        _started = dt.now()
        ClickOnObject(self.runebook_serial)
        Wait(500)
        _journal_line = InJournalBetweenTimes("зарядов", _started, dt.now())
        if _journal_line > 0:
            _match = re.search(r"(\d+)\/(\d+)\sзарядов", Journal(_journal_line))
            if _match:
                if max == 0:                    
                    _charges = _match.group(1)
                else:
                    _charges = _match.group(2)
        
        return _charges

    def open_runebook(self):
        ''' Opens runebook '''
        _current_gumps_count = GetGumpsCount()
        _try = 0
        while _current_gumps_count == GetGumpsCount():
            _try += 1
            if _try > 20:
                raise RuntimeError("[Runebook] Failed to open runebook")
            UseObject(self.runebook_serial)
            Wait(1000)
        

    def recall(self, rune: int) -> bool:
        ''' Recalls to selected rune '''
        self._close_all_gumps()
        self.open_runebook()
        _x = GetX(Self())
        _y = GetY(Self())
        _try = 0
        self._press_gump_button(rune)
        while _x == GetX(Self()) and _y == GetY(Self()):
            _try += 1
            if _try > 20:
                raise RuntimeError("[Runebook] Recall failed!")            
            Wait(1000)

    def recharge_required() -> int:
        ''' Returns difference between max and current charges. If > 0 - recharge required '''
        return self.get_runebook_charges() - self.get_runebook_charges(max=1)
        


    def recharge(self, count=1):
        print(f"Current: {self.get_runebook_charges()}")
        print(f"Max: {self.get_runebook_charges(max = 1)}")

