import random
import os
from time import sleep
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import MessageEntityType

from pyrogram.errors import FloodWait

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

app = Client('my_account', api_id=api_id, api_hash=api_hash)

@app.on_message(filters.command("delegate", prefixes=".") & filters.me)
async def echo(client, msg: Message):
    users = list()

    if msg.entities is None:
        await msg.edit("А на кого делигировать?")
        return

    i = 0
    for e in msg.entities:
        i+=1
        if e.type == MessageEntityType.MENTION:
            users.append(msg.command[i])
    
    perc = 0
    
    if len(users) == 0:
        await msg.edit("А на кого делигировать?")
        return
    
    await msg.edit(f"🕵️‍♂️ Начинаю искать на кого делигировать задачу из: {', '.join(users)}")
    
    random.shuffle(users)
    
    msg = await app.send_message(msg.chat.id, "🔍 Выбираю подходящего кандидата для делигирования")
    
    while(perc < 100):
        try:
            text = "🔍 Выбираю подходящего кандидата для делигирования ..." + str(perc) + "%"
            await msg.edit(text)
 
            perc += random.randint(1, 3)
            sleep(0.1)
 
        except FloodWait as e:
            sleep(e.x)
    
    await msg.edit(f"🎉 Поздравляем {users[0]} с делегированной на него задачей!")
        
app.run()