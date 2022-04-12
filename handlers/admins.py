from aiogram.dispatcher import FSMContext  # этот хэндел используется конкретно в машине состояний
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher

import keyboard
from create_bot import dp, bot
import conf
from database import sqlite_db
from keyboard import menu_admin
from conf import type_product

ID = None
text_price = ''
text_name = ''
list_category = []


class FSMAdminSelect(StatesGroup):
    select_product = State()


class FSMAdminChanges(StatesGroup):
    changes = State()
    changes_product = State()
    some = State()

class FSMAdminAdd(StatesGroup):
    add_tab = State()
    add_name = State()
    add_price = State()


# Получаем ID текущего админа
# @dp.message_handler(commands=['good'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    if message.from_user.id in conf.ID_ADMIN:

        ID = message.from_user.id
        await message.reply('Ты повелеваешь мной', reply_markup=menu_admin)
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


async def select_category(message: types.Message):
    if message.from_user.id == ID:
        btn = keyboard.btn()

        await message.answer(text='Отправляю список категорий!', reply_markup=btn)
        await message.delete()
        await FSMAdminSelect.select_product.set()


async def select_product(message: types.Message, state: FSMContext):

    text = message.text
    name_price_products = sqlite_db.select_name_price_product(text)
    for name_price in name_price_products:
        await message.answer(name_price)
    await message.answer('Конец', reply_markup=menu_admin)
    await state.finish()





async def changes_product_select(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdminChanges.changes.set()
        btn = keyboard.btn()
        await message.answer(text='Отправляю список категорий для изменения!', reply_markup=btn)
        await message.delete()

async def changes(message: types.Message):
    text = message.text
    btn_prod = keyboard.btn_prod(text)
    await message.answer(text='выбери продукт', reply_markup=btn_prod)
    await FSMAdminChanges.next()


async def changes_category(message: types.Message):
    global text_name

    if message.from_user.id == ID:
        text_name = message.text
        await message.answer(text='напиши цену')

        await FSMAdminChanges.next()

async def some_func(message: types.Message, state: FSMContext):
        global text_price
        text_price = message.text
        sqlite_db.select_chages(text_name, text_price)
        #TODO сделать проверку на дробное число,выдаёт ошибку если разделитель ","
        await message.answer('Значение обновлено', reply_markup=menu_admin)
        await state.finish()


async def add_table(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdminAdd.add_tab.set()
        btn = keyboard.btn()
        await message.answer(text='Отправляю список категорий для добавления!', reply_markup=btn)

        # await message.delete()
text_category = ''
async def add_category(message: types.Message):
    global text_category
    text_category = message.text
    await message.answer(f'Добавление в категорию {text_category}:')
    await FSMAdminAdd.next()

text_add_name = ''
async def add_name(message:types.Message):
    global text_add_name
    text_add_name = message.text
    await message.answer(f'Добавление цены для {text_add_name}:')
    await FSMAdminAdd.next()

text_add_price = ''
async def add_price(message:types.Message, state: FSMContext):
    global text_add_price
    text_add_price = message.text
    await sqlite_db.sql_add_command(text_category, text_add_name, text_add_price)
    await message.answer('Значение добавлено', reply_markup=menu_admin)
    await state.finish()





# Регситрируем хэндлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands='good', state=None)

    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")

    dp.register_message_handler(select_category, commands='Просмотр', state=None)
    dp.register_message_handler(select_product, state=FSMAdminSelect.select_product)

    dp.register_message_handler(changes_product_select, commands='Изменение', state=None)
    dp.register_message_handler(changes, state=FSMAdminChanges.changes)
    dp.register_message_handler(changes_category, state=FSMAdminChanges.changes_product)
    dp.register_message_handler(some_func, state=FSMAdminChanges.some)


    dp.register_message_handler(add_table, commands='Добавление', state=None)
    dp.register_message_handler(add_category, state=FSMAdminAdd.add_tab)
    dp.register_message_handler(add_name, state=FSMAdminAdd.add_name)
    dp.register_message_handler(add_price, state=FSMAdminAdd.add_price)


