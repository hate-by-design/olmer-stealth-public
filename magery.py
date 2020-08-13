
from py_stealth import *
from datetime import datetime as dt


def meditate():
    UseSkill("Meditation")
    Wait(500)
    while Mana() < MaxMana():
        Wait(500)

def heal():
    while HP() < MaxHP():
        Wait(500)


while not Dead():
    if Mana() < 20:
        meditate()
    if HP() < 10:
        heal()
    
    CastToObj("Magic Arrow", Self())
    Wait(1500)
