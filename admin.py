
import asyncio
from aiogram import Bot, Dispatcher
from handlers import hd_admin, hd_main
from dbss import db
from user_data import ADMIN_LIST, ADMIN_TOKEN, DATABASE, SHOP_TOKEN_BOT

#list of admins telegram user_id
ADMIN_LIST = ADMIN_LIST
#tg_bot admin token
TOKEN = ADMIN_TOKEN
#path to db
db_path = DATABASE
#token for user bot
SHOP_TOKEN = SHOP_TOKEN_BOT


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

    tasks = [
        asyncio.create_task(dp.start_polling(bot)),
        asyncio.create_task(dpt.start_polling(bot_s))
    ]

   

    await asyncio.gather(*tasks)

    
    db.db_close_conn()


if __name__ == "__main__":
    asyncio.run(main())