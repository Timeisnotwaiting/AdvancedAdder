from pyrogram import Client, filters, idle
from db import add, pop, get_users, cleandb
import os
import time
import asyncio
from pyrogram.errors import FloodWait, BadRequest

ID = os.environ["API_ID"]
HASH = os.environ["API_HASH"]
STRING = os.environ["STRING_SESSION"]
SUDO = os.environ["SUDO_USERS"].split()

SUDOS = []
for x in SUDO:
    SUDOS.append(int(x))

Stop = None

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
        async for v in _.get_chat_members(int(id)):
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
        await ok.edit(str(z) + " IDS UPLOADED TO DB !")
    except Exception as e:
        await ok.edit(e)
        pass

@yashu.on_message(filters.command("scrapdb", "!") & filters.user(SUDOS))
async def scrapdb(_, m):
    global Stop
    Stop = False
    if str(m.chat.id)[0] != "-":
        return await m.reply("THIS COMMAND ONLY WORKS IN GROUP !")
    USERS = await get_users()
    if not USERS:
        return await m.reply("DATABSE IS EMPTY !!")  
    a = 0
    b = 0
    c = 0
    ok = await m.reply(f"ADDING FROM DATABASE, {len(USERS)} FOUND") 
    for x in USERS:
        try:
            if Stop:
                return
            await _.add_chat_members(m.chat.id, int(x))
            a += 1
            await ok.edit(f"ADDED : {a}\n\nFAILED : {b}")
            await pop(x)
            time.sleep(2)
        except FloodWait:
            try:
                await ok.edit("SLEEPING FOR 20s")
            except:
                pass
            await asyncio.sleep(20)
        except BadRequest as e:
            print(e)
            await ok.edit("ID GOT LIMITED !")
            return
        except Exception as e:
            print(e)
            b += 1
            pass
        if a == 1000:
            break

@yashu.on_message(filters.command("stop", "!") & filters.user(SUDOS))
async def stop(_, m):
    global Stop
    if not Stop:
        Stop = True
        return await m.reply("PROCESS STOPPED..!")
    else:
        return await m.reply("NO PROCESS RUNNING..!")

@yashu.on_message(filters.command("cleandb", "!") & filters.user(SUDOS))
async def db_cleaner(_, m):
    try:
        ok = await m.reply("CLEARING DATABASE...!")
        await cleandb()
        await ok.edit("DATABASE CLEARED !")
    except Exception as e:
        return await m.reply(e)

@yashu.on_message(filters.command(["join", "leave"], "!") & filters.user(SUDOS))
async def joinleave(_, m):
    try:
        entity = m.text.split(None, 1)[1]
    except:
        return await m.reply("GIVE ID OR USERNAME !")
    try:
        if m.text.split()[0][1].lower() == "j":
            await _.join_chat(entity)
            return await m.reply("JOINED !!")
        else:
            await _.leave_chat(entity)
            return await m.reply("LEFT CHAT !!")
    except Exception as e:
        await m.reply(e)

yashu.start()
print("YashuAlpha Op")
idle()
   
