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


class FSMAdminDel(StatesGroup):
    del_type = State()
    del_cat = State()
    del_name = State()


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
        await message.reply('OK', reply_markup=menu_admin)


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
    # TODO сделать проверку на дробное число,выдаёт ошибку если разделитель ","
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


async def add_name(message: types.Message):
    global text_add_name
    text_add_name = message.text
    await message.answer(f'Добавление цены для {text_add_name}:')
    await FSMAdminAdd.next()


text_add_price = ''


async def add_price(message: types.Message, state: FSMContext):
    global text_add_price
    text_add_price = message.text
    await sqlite_db.sql_add_command(text_category, text_add_name, text_add_price)
    await message.answer('Значение добавлено', reply_markup=menu_admin)
    await state.finish()


async def del_sql_type(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdminDel.del_cat.set()
        btn = keyboard.btn()
        await message.answer(text='Отправляю список категорий откуда надо удалить!', reply_markup=btn)


del_cat = ''


async def del_sql_cat(message: types.Message):
    global del_cat
    del_cat = message.text
    btn_prod = keyboard.btn_prod(del_cat)
    await message.answer(f'Удаление из категорию {del_cat}:', reply_markup=btn_prod)
    await FSMAdminDel.next()


del_name = ''


async def del_sql_name(message: types.Message, state: FSMContext):
    global del_name
    del_name = message.text
    await sqlite_db.sql_del(del_name)
    await message.answer(f'Удаление {del_name}', reply_markup=menu_admin)
    await state.finish()


class FSMAdminAddDishes(StatesGroup):
    select_add_1 = State()
    select_add_2 = State()
    select_add_3 = State()
    select_add_4 = State()
    select_add_5 = State()
    select_add_6 = State()



async def select_for_add_dishes(callback_query: types.CallbackQuery):
    await FSMAdminAddDishes.select_add_1.set()
    await bot.send_message(ID, 'Название блюда')

name_dish = ''
async def select_for_add_name_dish(message: types.Message):
    global name_dish
    name_dish = message.text
    btn = keyboard.btn()
    await message.reply('Выбери продукты входящие в состав. Сначала категорию продуктов:', reply_markup=btn)
    await FSMAdminAddDishes.next()

type_categ = ''
async def select_for_add_categ(callback_query: types.CallbackQuery):
    global type_categ
    type_categ = callback_query.data
    btn_prod = keyboard.btn_prod(type_categ)
    await bot.send_message(ID, 'Выбери продукт', reply_markup=btn_prod)
    await FSMAdminAddDishes.next()
name_product = ''
async def select_for_add_prod(callback_query: types.CallbackQuery):
    global name_product
    name_product = callback_query.data
    await bot.send_message(ID, 'Напиши нетто')
    await FSMAdminAddDishes.next()
netto_prod = ''
brutto_prod = ''
sum = ''
price = ''
async def select_for_add_netto(message: types.Message):
    global netto_prod
    global brutto_prod
    global sum
    global price
    netto_prod = message.text

    #TODO сделать отдельгную функцию
    percent, price = await sqlite_db.get_percent_price(name_product)
    brutto_prod = round((int(netto_prod) / (100 - int(percent))) * 100)
    sum = round((int(price)*brutto_prod)/1000)

    btn_choice = keyboard.btn_choice(name_dish)
    await message.answer('Продолжить выбор или закончить?', reply_markup=btn_choice)
    await FSMAdminAddDishes.next()
product_list = []
netto_list = []
brutto_plist = []
price_list = []
sum_list = []
async def select_for_add_choice(callback_query: types.CallbackQuery):
    global product_list
    global netto_list
    global brutto_plist
    global price_list
    global sum_list
    global name_product
    product_list.append(name_product)
    netto_list.append(netto_prod)
    brutto_plist.append(brutto_prod)
    price_list.append(price)
    sum_list.append(sum)

    btn = keyboard.btn()
    if callback_query.data == name_dish:
        await callback_query.answer('продолжаем')
        await bot.send_message(chat_id=ID, text='Выбери продукты входящие в состав. Сначала категорию продуктов:',
                               reply_markup=btn)
        await FSMAdminAddDishes.select_add_2.set()
    elif callback_query.data == 'STOP':
        ff = zip(product_list, netto_list, brutto_plist, price_list, sum_list)
        await sqlite_db.create_table_dish(name_dish)
        for r in list(ff):
            name_product = r[0]
            brutto_product = r[2]
            netto_product = r[1]
            price_kg = r[3]
            summ = r[4]
            await sqlite_db.add_table_dish(name_dish, name_product, brutto_product, netto_product, price_kg, summ)
        await bot.send_message(ID, 'DONE')



# async def select_for_add_products(message: types.Message):
#     name_dishes = message.text  # название таблицы\блюда
#     while not message.text == 'стоп':
#         name_products = []
#         netto_products = []
#         brutto_products = []
#         btn = keyboard.btn()
#         await message.answer('выбери категорию', reply_markup=btn)  # кнопки с категорией, выбираешь один и далее
#         categ = message.text
#         # в цикле добавляется
#         btn_prod = keyboard.btn_prod(categ)
#         await message.answer('выбери продукт', reply_markup=btn_prod)
#         produc=message.text
#         name_products.append(produc)  # название выбранного продукта
#         await message.answer('напишии нетто продукта')
#         netto_product = message.text  # нетто продукта
#         netto_products.append(netto_product)
#         percent = f'SELECT percent_off FROM products WHERE = "{produc}"'  # подсчёт брутто
#         brutto_product = (netto_product/(100 - percent))*100
#         brutto_products.append(brutto_product)
#         price_kg =f'SELECT price FROM products WHERE = "{produc}"'  # подставляется цена за кг продукта
#     summ = None  # подсчёт суммы price_kg*brutto_product
    # запрос на создание таблицы (CREATE TABLE {name_dishes} (products TEXT, brutto REAL,
    # netto REAL, price_kg REAL, sum REAL))
    # запрос на добавление данных в таблицу INSERT INTO {name_dishes}
    # (Products, brutto, netto, price_kg, summ) VALUES (name_product,
    # brutto_product, netto_product, price_kg, summ)
    # занесение в таблицу meny нового блюда и подсчёт price(себестоиости)


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

    dp.register_message_handler(add_table, commands='ДобавлениеПродуктов', state=None)
    dp.register_message_handler(add_category, state=FSMAdminAdd.add_tab)
    dp.register_message_handler(add_name, state=FSMAdminAdd.add_name)
    dp.register_message_handler(add_price, state=FSMAdminAdd.add_price)

    dp.register_message_handler(del_sql_type, commands='Удаление', state=None)
    dp.register_message_handler(del_sql_cat, state=FSMAdminDel.del_cat)
    dp.register_message_handler(del_sql_name, state=FSMAdminDel.del_name)

    dp.register_callback_query_handler(select_for_add_dishes, lambda c: c.data == 'Добавление Блюда', state=None)
    dp.register_message_handler(select_for_add_name_dish, state=FSMAdminAddDishes.select_add_1)
    dp.register_callback_query_handler(select_for_add_categ, state=FSMAdminAddDishes.select_add_2)
    dp.register_callback_query_handler(select_for_add_prod, state=FSMAdminAddDishes.select_add_3)
    dp.register_message_handler(select_for_add_netto, state=FSMAdminAddDishes.select_add_4)
    dp.register_callback_query_handler(select_for_add_choice, state=FSMAdminAddDishes.select_add_5)



