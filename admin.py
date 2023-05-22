import asyncio
from aiogram import Bot, Dispatcher
from handlers import hd_admin
from db.database import DbShop
import os
from money.cryptobot import CryptoPay
from user_data import ADMIN_LIST, TOKEN, DATABASE

#list of admins telegram user_id
ADMIN_LIST = ADMIN_LIST
#tg_bot token
TOKEN = TOKEN
#path to db
db_path = DATABASE



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
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    


    dp.include_routers(hd_admin.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    db.db_close_conn()


if __name__ == "__main__":
    asyncio.run(main())