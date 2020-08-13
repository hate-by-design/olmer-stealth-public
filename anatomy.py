from py_stealth import *
from datetime import datetime as dt


while not Dead():
    _started = dt.now()
    UseSkill("Anatomy")
    WaitTargetObject(0x005EE02F)
    WaitJournalLine(_started, "Вы не поняли|Жизненная", 50000)
