# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, executor
import conf


bot = Bot(token=conf.API_TOKEN)
dp = Dispatcher(bot)
