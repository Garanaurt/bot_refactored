import asyncio
from aiogram import Bot, Dispatcher
from handlers import hd_main
from db.database import DbShop

TOKEN = "5756085358:AAEboc6ZRK1pkgCnB1hDL_WTNlUqlTDWNg0"
db_path = 'users.db'
db = DbShop()
db.db_path = db_path
db.db_initialize()

# Запуск бота
async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(hd_main.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    db.db_close_conn()


if __name__ == "__main__":
    asyncio.run(main())