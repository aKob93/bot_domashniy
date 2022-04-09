from aiogram.dispatcher import FSMContext  # этот хэндел используется конкретно в машине состояний
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
import conf
from database import sqlite_db
from keyboard import button_case_admin
ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    price = State()


# Получаем ID текущего админа
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    if message.from_user.id in conf.ID_ADMIN:

        ID = message.from_user.id

        await message.reply('Ты повелеваешь мной', reply_markup=button_case_admin)
        # await message.delete()
    else:
        await message.reply('You Shall Not Pass')


# Выход из состояний
# @dp.message_handler(state="*", commands='отмена')#Ползьзователь выбирает команду отмена. state="*" из любого состояния
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")#Пользователь пишут отмена
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')


async def select_table(message: types.Message):
    if message.from_user.id == ID:
        texts = sqlite_db.sql_select()
        await message.reply(texts)



# Начало диалога загрузки нового пункта меню
# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')


# Ловим первый ответ и пишем словарь(переходим в состояние "фото")
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    # сохранение полученного рез-та в словарь
    # сохранеятся не само фото а его айди
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        # переводим бота в ожидание следующего ответа
        await FSMAdmin.next()
        await message.reply('Теперь введи название')


# Ловим второй ответ
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи price')


# Ловим последний ответ и используем полученные данные
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)
        await sqlite_db.sql_add_command(state)
        # Бот выходит из машины состояний, очищает словарь
        await state.finish()


# Регситрируем хэндлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands='Загрузить', state=None)
    dp.register_message_handler(select_table, commands='Просмотр', state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands='good')
