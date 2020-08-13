from py_stealth import *
from Scripts.discord import discord_message
import random
LOCATION = "Пустыня"
PHRASES = [
    "Как Вас жизнь разбросала-то. Отдельно вкус, отдельно ум, отдельно красота.",
    "Да, Вы, я смотрю мастер спорта по традиционному русскому единоборству — борьбе с похмельным синдромом..",
    "А у Вас всегда волосы шевелятся, когда Вы начинаете думать?",
    "В Вашем присутствии совсем не вежливо выглядеть талантливым и умным.",
    "Я никогда еще не видел столько грязи в таких красивых шелковых чулках!",
    "Да, я вижу, Вас постоянно преследуют умные мысли. Но Вы всегда оказываетесь быстрее!",
    "Таких как Вы, на самом деле, на свете очень мало. Но расставлены они так грамотно, что постоянно натыкаешься на дурака или идиота.",
    "Чтоб оно вам поперек горла встало, когда по-большому пойдете."
]

def handle_attack(text: str, sender_name: str, sender_id: int):
    print(f"Text: {text}, sender_name: {sender_name}, sender_id: {sender_id}")
    if "attacking you" in text:
        discord_message(f"{sender_name} атакует меня в локации **>>{LOCATION}<<**")
        UOSay(random.choice(PHRASES))

SetEventProc("evSpeech", handle_attack)


while 1:
    Wait(100)
