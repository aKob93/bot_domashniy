# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, executor
import conf
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

bot = Bot(token=conf.API_TOKEN)
dp = Dispatcher(bot, storage=storage)

