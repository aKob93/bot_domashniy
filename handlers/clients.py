# -*- coding: utf-8 -*-

from aiogram import types, Dispatcher
import keyboard
from create_bot import dp

# @dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Привет!\nМожно узнать наличие по блюдами, либо сделать заказ на нужную дату.",
                        reply_markup=keyboard.check_menu)
    print(message.from_user.id)

# @dp.callback_query_handler(lambda c: c.data == 'order_menu')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await types.ChatActions.upload_photo() #уведомление об отправке файла
    await callback_query.answer(text='Отправляю меню!')
    # await message.answer(text='fgdf')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_callback_query_handler(process_callback_button1, lambda c: c.data == 'order_menu')
