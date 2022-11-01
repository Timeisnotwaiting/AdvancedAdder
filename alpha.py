from pyrogram import Client, filters, idle
from db import add, pop
import os

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
                return
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
                await ok.edit("PROGRESS : {z}")
                a = 0
    except Exception as e:
        await ok.edit(e)
        pass

            
