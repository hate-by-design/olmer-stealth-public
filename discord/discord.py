from py_stealth import *
ID = 3
TOKEN = "NzM3NzA3OTQzODg5sdgfsgsgsdf"
USER_ID = 7334093043234234234123


def discord_message(message):
    MessengerSetToken(ID, TOKEN)
    MessengerSetConnected(ID, True)
    while not MessengerGetConnected(ID):
        Wait(100)

    _current_script = CurrentScriptPath().split("\\")
    MessengerSendMessage(
        ID, f"[{CharName()}] ({_current_script[-1]}): {message}", USER_ID)
    Wait(5000)
    MessengerSetConnected(ID, False)
