import os
from motor.motor_asyncio import AsyncIOMotorClient as K

MONGO = os.environ["MONGO_DB_URL"]

x = K(MONGO)
db = x.ADV

userdb = db.user

async def is_user(user_id: int):
    x = await userdb.find_one({"user_id": user_id})
    if x:
        return True
    return False

async def add(user_id: int):
    x = await is_user(user_id)
    if x:
        return
    await userdb.insert_one({"user_id": user_id})
    return

async def pop(user_id: int):
    x = await is_user(user_id)
    if not x:
        return
    await userdb.delete_one({"user_id": user_id})
    return
