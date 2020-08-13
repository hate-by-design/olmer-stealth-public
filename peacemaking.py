from py_stealth import *
from datetime import datetime as dt


def meditate():
    UseSkill("Meditation")
    Wait(500)
    while Mana() < MaxMana():
        Wait(500)

def train():
    if WarMode():
        SetWarMode(False)
    if Mana() < 10:
        meditate()

    _started = dt.now()
    Wait(10000)
    if InJournalBetweenTimes("Хватит|Друзья|Узпокойся|Давайте", _started, dt.now()) < 0:
        UseSkill("Peacemaking")


if __name__ == "__main__":
    SetARStatus(True)
    SetPauseScriptOnDisconnectStatus(True)
    while not Dead() and Connected():
        train()
