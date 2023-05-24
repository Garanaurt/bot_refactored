import asyncio
from aiogram import Bot, Dispatcher
from handlers import hd_admin, hd_main
from db.database import DbShop
import os
from user_data import ADMIN_LIST, ADMIN_TOKEN, DATABASE, SHOP_TOKEN_BOT

#list of admins telegram user_id
ADMIN_LIST = ADMIN_LIST
#tg_bot admin token
TOKEN = ADMIN_TOKEN
#path to db
db_path = DATABASE
#token for user bot
SHOP_TOKEN = SHOP_TOKEN_BOT



#check and create db and tables
db = DbShop()
if not os.path.exists(db_path):
    db.db_path = db_path
    db.db_initialize()
    db.db_check_and_create_tables()
    db.db_close_conn()
db.db_path = db_path
db.db_initialize()


#start bot
async def main():
    #part of admin
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(hd_admin.router)
    await bot.delete_webhook(drop_pending_updates=True)

    #part of user
    bot_s = Bot(token=SHOP_TOKEN)
    dpt = Dispatcher()
    dpt.include_routers(hd_main.router)
    await bot_s.delete_webhook(drop_pending_updates=True)
    await dpt.start_polling(bot_s, bot)


    db.db_close_conn()



if __name__ == "__main__":
    asyncio.run(main())