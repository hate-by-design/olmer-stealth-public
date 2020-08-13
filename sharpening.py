from py_stealth import *
from datetime import datetime as dt
from Scripts.types import Types
import re

TYPE = Types.PICKAXE
ATTACK_REQUIRED = 76


def cancel_targets():
    CancelWaitTarget()
    if TargetPresent():
        CancelTarget()

def sharp(target: int):
    _started = dt.now()
    cancel_targets()
    UseType(0x241C, 0xFFFF)
    if WaitForTarget(1000):
        WaitTargetObject(target)        
        WaitJournalLine(_started, "Неудачная|атака", 5000)
        Wait(100)



def item_attack_power(item_serial: int) -> int:        
    _started = dt.now()
    ClickOnObject(item_serial)
    Wait(500)
    _journal_line = InJournalBetweenTimes("Атака", _started, dt.now())
    if _journal_line > 0:
        _match = re.search(r"Атака\s(\d+)", Journal(_journal_line))
        if _match:
            print(_match.group(1))
            return int(_match.group(1))
    print("!!! Fail to get current attack, returning 1000 to break loop")
    return 1000

def spheres_available() -> bool:
    if FindType(0x241C, Backpack()):
        return True
    return False

if __name__ == "__main__":
    if FindType(TYPE, Backpack()):
        for target in GetFoundList():
            while item_attack_power(target) < ATTACK_REQUIRED:
                sharp(target)
                Wait(100)
