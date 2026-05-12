import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from database import init_db

from handlers import start, task, referral, wallet, withdraw
from admin import admin_handlers
from keep_alive import run_server

async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Initialize database
    await init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Include routers
    dp.include_router(start.router)
    dp.include_router(task.router)
    dp.include_router(referral.router)
    dp.include_router(wallet.router)
    dp.include_router(withdraw.router)
    dp.include_router(admin_handlers.router)

    # Start web server for Replit/Render keep-alive
    await run_server()

    print("Bot is starting...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")
