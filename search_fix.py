from py_stealth import *
CHEST = 0x40317177

UseObject(CHEST)
Wait(500)
FindType(-1, CHEST)
for _item in GetFindedList():
    ClickOnObject(_item)
    Wait(100)
