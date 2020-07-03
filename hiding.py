from py_stealth import *
from datetime import datetime as dt


start_x = GetX(Self())
start_y = GetY(Self())

def hide():            
    _started = dt.now()
    UseSkill("Hiding")
    WaitJournalLine(_started, "Спрятаться не удалось|You have hidden", 10000)    
    

def train():
    while Hidden():
        newMoveXY(start_x + 2, start_y, True, 0, False)
        newMoveXY(start_x, start_y, True, 0, False)

    while not Hidden():
        hide()

while not Dead():
    # Stealth - uncomment
    train()

    # Stealth - comment
    #hide()
    
    Wait(100)
