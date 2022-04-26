from aiogram.dispatcher import FSMContext  # этот хэндел используется конкретно в машине состояний
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher

import keyboard
from create_bot import dp, bot
import conf
from database import sqlite_db
from keyboard import menu_admin

ID = None
text_price = ''
text_name = ''
list_category = []


class FSMAdminSelect(StatesGroup):
    select_product = State()


class FSMAdminSelectMenu(StatesGroup):
    select_menu = State()


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


async def change_menu_prod(callback_query: types.CallbackQuery):
    if callback_query.from_user.id == ID:
        btn = keyboard.btn_type_product_menu()
        await callback_query.message.edit_text(text='выбери меню или продукты!', reply_markup=btn)


async def change_menu(callback_query: types.CallbackQuery):
    btn = keyboard.btn_type_dishes()
    await callback_query.message.edit_text(text='выбери категорию меню!', reply_markup=btn)
    await FSMAdminSelectMenu.select_menu.set()


async def change_name_menu(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['menu_cat'] = callback_query.data
    name_price_products = sqlite_db.get_name_price_menu(conf.type_menu[data['menu_cat']])
    for name_price in name_price_products:
        await bot.send_message(ID, text=name_price)
    await bot.send_message(ID, 'Конец', reply_markup=menu_admin)
    await state.finish()


async def select_category(callback_query: types.CallbackQuery):
    if callback_query.from_user.id == ID:
        btn = keyboard.btn()

        await callback_query.message.edit_text(text='Отправляю список категорий!', reply_markup=btn)
        await FSMAdminSelect.select_product.set()


async def select_product(callback_query: types.CallbackQuery, state: FSMContext):
    text = callback_query.data
    name_price_products = sqlite_db.select_name_price_product(text)
    for name_price in name_price_products:
        await bot.send_message(ID, text=name_price)
    await bot.send_message(ID, 'Конец', reply_markup=menu_admin)
    await state.finish()


class FSMAdminChangesProduct(StatesGroup):
    changes1 = State()
    changes2 = State()
    changes3 = State()
    changes_4 = State()



async def change_category(callback_query: types.CallbackQuery):
    await FSMAdminChangesProduct.changes1.set()
    btn_prod = keyboard.btn()
    await callback_query.message.edit_text(text='выбери категорию продукт', reply_markup=btn_prod)


async def change_name(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['categ_prod'] = callback_query.data
    btn_pr = keyboard.btn_prod(data['categ_prod'])
    await callback_query.message.edit_text(text='выбери продукт', reply_markup=btn_pr)
    await FSMAdminChangesProduct.next()


async def change_price(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = callback_query.data
    await callback_query.message.edit_text(text='Укажи цену')
    await FSMAdminChangesProduct.next()


async def change_percent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.reply(text='Укажи процент потерь. Если нет, то укажи 0')
    await FSMAdminChangesProduct.next()


async def change_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['percent'] = message.text
    sqlite_db.select_chages(data['name'], int(data['price']), int(data['percent']))
    # TODO сделать проверку на дробное число,выдаёт ошибку если разделитель ","
    await message.answer(text='Значение обновлено', reply_markup=menu_admin)
    await state.finish()


class FSMAdminAdd(StatesGroup):
    add_tab = State()
    add_name = State()
    add_price = State()
    add_percent = State()


async def add_table(callback_query: types.CallbackQuery):
    if callback_query.from_user.id == ID:
        await FSMAdminAdd.add_tab.set()
        btn = keyboard.btn()
        await callback_query.message.edit_text(text='Отправляю список категорий для добавления!', reply_markup=btn)



text_category = ''


async def add_category(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['category_product'] = callback_query.data
    await callback_query.message.edit_text(f'Добавление в категорию {data["category_product"]}:')
    await FSMAdminAdd.next()


text_add_name = ''


async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_product'] = message.text
    await message.reply(f'Добавление цены для {data["name_product"]}:')
    await FSMAdminAdd.next()


text_add_price = ''


async def add_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price_product'] = message.text
    await message.reply(f'Добавление процента потерь для {data["price_product"]}:')
    await FSMAdminAdd.next()


async def add_percent_off(message: types.Message, state: FSMContext):
    #TODO: сделать проверку на наличие процента
    async with state.proxy() as data:
        data['percent_product'] = message.text
    sqlite_db.sql_add_command(data['category_product'], data['name_product'],
                              data['price_product'], data['percent_product'])
    await message.reply('Значение добавлено', reply_markup=menu_admin)
    await state.finish()


class FSMAdminDelMenu(StatesGroup):
    del1 = State()
    del2 = State()
    del3 = State()


async def del_change_menu_product(callback_query: types.CallbackQuery):
    btn_type_product_menu = keyboard.btn_del_product_menu()
    await callback_query.message.edit_text(text='Выбери откуда удалять', reply_markup=btn_type_product_menu)

async def del_for_menu(callback_query: types.CallbackQuery):
    btn_type_dishes = keyboard.btn_type_dishes()
    await callback_query.message.edit_text(text='Выбери категорию', reply_markup=btn_type_dishes)
    await FSMAdminDelMenu.del1.set()

async def del_name_menu(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['categ_menu'] = callback_query.data
    btn_type_menu = keyboard.btn_type_menu(conf.type_menu[data['categ_menu']])
    await callback_query.message.edit_text(text='Выбери что удалять', reply_markup=btn_type_menu)
    await FSMAdminDelMenu.next()

async def del_menu(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['name_menu'] = callback_query.data
    sqlite_db.del_menu(data['name_menu'])
    await callback_query.message.edit_text(text=f'Удалено {data["name_menu"]}')
    await state.finish()




async def del_sql_type(callback_query: types.CallbackQuery):
    if callback_query.from_user.id == ID:
        await FSMAdminDel.del_cat.set()
        btn = keyboard.btn()
        await callback_query.message.edit_text(text='Отправляю список категорий откуда надо удалить!', reply_markup=btn)




async def del_sql_cat(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['categ'] = callback_query.data

    btn_prod = keyboard.btn_prod(data['categ'])
    await callback_query.message.edit_text(f'Удаление из категорию {data["categ"]}:', reply_markup=btn_prod)
    await FSMAdminDel.next()


del_name = ''


async def del_sql_name(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['name_prod'] = callback_query.data
    sqlite_db.sql_del(data['name_prod'])
    await callback_query.message.edit_text(f'Удаление {del_name}', reply_markup=menu_admin)
    await state.finish()


class FSMAdminAddDishes(StatesGroup):
    select_add_0 = State()
    select_add_1 = State()
    select_add_2 = State()
    select_add_3 = State()
    select_add_4 = State()
    select_add_5 = State()
    select_add_6 = State()


async def select_for_add_dishes(callback_query: types.CallbackQuery):
    await FSMAdminAddDishes.select_add_0.set()
    await bot.send_message(ID, 'Название блюда')


name_dish = ''


async def select_for_add_type_dishes(message: types.Message):
    global name_dish
    name_dish = message.text
    btn = keyboard.btn_type_dishes()
    await message.reply('Выбери категорию блюда:', reply_markup=btn)
    await FSMAdminAddDishes.next()


type_dishes = ''


async def select_for_add_name_dish(callback_query: types.CallbackQuery):
    global type_dishes
    type_dishes = callback_query.data
    btn = keyboard.btn()
    await bot.send_message(ID, 'Выбери продукты входящие в состав. Сначала категорию продуктов:', reply_markup=btn)
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

    # TODO сделать отдельгную функцию
    percent, price = sqlite_db.get_percent_price(name_product)
    brutto_prod = round((int(netto_prod) / (100 - int(percent))) * 100)
    sum = round((int(price) * brutto_prod) / 1000)

    btn_choice = keyboard.btn_choice(name_dish)
    await message.answer('Продолжить выбор или закончить?', reply_markup=btn_choice)
    await FSMAdminAddDishes.next()





async def select_for_add_choice(callback_query: types.CallbackQuery, state: FSMContext):
    product_list = []
    netto_list = []
    brutto_plist = []
    price_list = []
    sum_list = []
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

        sqlite_db.create_table_dish(name_dish)
        for r in list(ff):
            name_product = r[0]
            brutto_product = r[2]
            netto_product = r[1]
            price_kg = r[3]
            summ = r[4]
            sqlite_db.add_table_dish(name_dish, name_product, brutto_product, netto_product, price_kg, summ)
        price_sum = sqlite_db.get_price(name_dish)
        price_sum = float(price_sum)
        netto = sqlite_db.get_netto(name_dish)
        netto = float(netto)
        price_s = round((price_sum * 1000) / netto)
        sqlite_db.add_dishes_for_table_menu(type=type_dishes, name=name_dish, price=price_s)
        await bot.send_message(ID, 'DONE', reply_markup=menu_admin)
        await state.finish()





async def update(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text='Идёт обновление')
    sqlite_db.update_price()
    await bot.send_message(ID, text='Обновлено', reply_markup=menu_admin)




# Регситрируем хэндлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands='good', state=None)

    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")

    dp.register_callback_query_handler(change_menu_prod, lambda k: k.data == 'Просмотр')
    dp.register_callback_query_handler(change_menu, lambda c: c.data == 'Menu', state=None)
    dp.register_callback_query_handler(change_name_menu, state=FSMAdminSelectMenu.select_menu)
    dp.register_callback_query_handler(select_category, lambda c: c.data == 'Products', state=None)
    dp.register_callback_query_handler(select_product, state=FSMAdminSelect.select_product)

    dp.register_callback_query_handler(change_category, lambda k: k.data == 'Изменение')
    dp.register_callback_query_handler(change_name, state=FSMAdminChangesProduct.changes1)
    dp.register_callback_query_handler(change_price, state=FSMAdminChangesProduct.changes2)
    dp.register_message_handler(change_percent, state=FSMAdminChangesProduct.changes3)
    dp.register_message_handler(change_finish, state=FSMAdminChangesProduct.changes_4)

    dp.register_callback_query_handler(add_table, lambda c: c.data == 'Добавление Продуктов', state=None)
    dp.register_callback_query_handler(add_category, state=FSMAdminAdd.add_tab)
    dp.register_message_handler(add_name, state=FSMAdminAdd.add_name)
    dp.register_message_handler(add_price, state=FSMAdminAdd.add_price)
    dp.register_message_handler(add_percent_off, state=FSMAdminAdd.add_percent)


    dp.register_callback_query_handler(del_change_menu_product, lambda c: c.data == 'Удаление', state=None)
    dp.register_callback_query_handler(del_for_menu, lambda c: c.data == 'Del menu')
    dp.register_callback_query_handler(del_name_menu, state=FSMAdminDelMenu.del1)
    dp.register_callback_query_handler(del_menu, state=FSMAdminDelMenu.del2)

    dp.register_callback_query_handler(del_sql_type, lambda c: c.data == 'Del products', state=None)
    dp.register_callback_query_handler(del_sql_cat, state=FSMAdminDel.del_cat)
    dp.register_callback_query_handler(del_sql_name, state=FSMAdminDel.del_name)

    dp.register_callback_query_handler(select_for_add_dishes, lambda c: c.data == 'Добавление Блюда', state=None)
    dp.register_message_handler(select_for_add_type_dishes, state=FSMAdminAddDishes.select_add_0)
    dp.register_callback_query_handler(select_for_add_name_dish, state=FSMAdminAddDishes.select_add_1)
    dp.register_callback_query_handler(select_for_add_categ, state=FSMAdminAddDishes.select_add_2)
    dp.register_callback_query_handler(select_for_add_prod, state=FSMAdminAddDishes.select_add_3)
    dp.register_message_handler(select_for_add_netto, state=FSMAdminAddDishes.select_add_4)
    dp.register_callback_query_handler(select_for_add_choice, state=FSMAdminAddDishes.select_add_5)

    dp.register_callback_query_handler(update, lambda c: c.data == 'Обновление')
