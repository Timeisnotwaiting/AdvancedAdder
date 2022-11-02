from pyrogram import Client, filters, idle
from db import add, pop, get_users, cleandb
import os
import time

ID = os.environ["API_ID"]
HASH = os.environ["API_HASH"]
STRING = os.environ["STRING_SESSION"]
SUDO = os.environ["SUDO_USERS"].split()

SUDOS = []
for x in SUDO:
    SUDOS.append(int(x))

yashu = Client(":YashuAlpha:", api_id=ID, api_hash=HASH, session_string=STRING)

@yashu.on_message(filters.command("addtodb", "!") & filters.user(SUDOS))
async def addtodb(_, m):
    id = m.text.split()[1]
    if not id:
        return await m.reply("PROVIDE GROUP ID !")
    if not str(id)[0] == "-":
        return await m.reply("PROVIDE VALID GROUP ID !") 
    ok = await m.reply("ADDING MEMBERS TO DATABASE !")
    N = []
    try:
        async for v in _.get_chat_members(id):
            if v.user.is_bot or v.user.is_deleted:
                pass
            else:
                N.append(v.user.id)
        await ok.edit(f"{len(N)} IDS FOUND !")
        a = 0
        b = len(N) // 10
        c = len(N) // b
        z = 0
        for h in N:
            await add(h)
            a += 1
            z += 1
            if a == c:
                await ok.edit(f"PROGRESS : {z}")
                a = 0
    except Exception as e:
        await ok.edit(e)
        pass

@yashu.on_message(filters.command("scrapdb", "!") & filters.user(SUDOS))
async def scrapdb(_, m):
    if str(m.chat.id)[0] != "-":
        return await m.reply("THIS COMMAND ONLY WORKD IN GROUP !")
    USERS = await get_users()
    if not USERS:
        return await m.reply("DATABSE IS EMPTY !!")  
    a = 0
    b = 0
    c = 0
    ok = await m.reply(f"ADDING FROM DATABASE, {len(USERS)} FOUND") 
    for x in USERS:
        try:
            await _.add_chat_members(m.chat.id, x)
            a += 1
            await ok.edit(f"ADDED : {a}\n\nFAILED : {b}")
            await pop(x)
            time.sleep(2)
        except Exception as e:
            print(e)
            b += 1
            pass
        if a == 100:
            break

@yashu.on_message(filters.command("cleandb", "!") & filters.user(SUDOS))
async def db_cleaner(_, m):
    try:
        ok = await m.reply("CLEARING DATABASE...!")
        await cleandb()
        await ok.edit("DATABASE CLEARED !")
    except Exception as e:
        return await m.reply(e)

yashu.start()
print("YashuAlpha Op")
idle()
   
