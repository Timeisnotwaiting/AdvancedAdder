import os
from motor.motor_asyncio import AsyncIOMotorClient as K

try:
    MONGO = os.environ["MONGO_DB_URL"]
except:
    from yashu import MONGO

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

async def get_users():
    y = userdb.find({"user_id": {"$gt": 0}})
    USERS = []
    for x in await y.to_list(length=1000000000):
        USERS.append(x["user_id"])
    return USERS

async def cleandb():
    x = await get_users()
    for y in x:
        await pop(y)

async def check_db():
    x = await get_users()
    return len(x)
