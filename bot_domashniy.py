# -*- coding: utf-8 -*-
import logging
from aiogram import executor
from create_bot import dp
from handlers import clients, admins
from database import sqlite_db
# Configure logging
logging.basicConfig(level=logging.INFO)


async def on_startup(_): #Бот запустился(в будующем подключение к бд)
    print('Бот онлайн')
    sqlite_db.sql_start()


clients.register_handlers_client(dp)
admins.register_handlers_admin(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup) #skip_updates=True - бот не будет отвечать на сообщения отправленные офлайн
