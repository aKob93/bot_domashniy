# -*- coding: utf-8 -*-
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher

from create_bot import bot
import conf
from database import changing_data, data_request
from keyboards import keyboards_for_admin

ID = None


class FSMAdminSelectCategoryProducts(StatesGroup):
    select_category = State()


class FSMAdminSelectCategoryMenu(StatesGroup):
    select_category = State()
    select_choice_price_or_structure = State()
    select_name_dish = State()


class FSMAdminDelProducts(StatesGroup):
    select_del_category = State()
    select_del_name_product = State()


class FSMAdminDelMenu(StatesGroup):
    select_del_category = State()
    select_del_name = State()


class FSMAdminChangesProduct(StatesGroup):
    select_changes_category = State()
    select_changes_name = State()
    select_changes_price = State()
    select_changes_percent = State()
    select_changes_percent_choice = State()
    select_changes_finish = State()


class FSMAdminAddProduct(StatesGroup):
    select_category_for_add = State()
    select_name_product = State()
    select_price_product = State()
    select_percent_product = State()


class FSMAdminAddDishes(StatesGroup):
    select_category_dish = State()
    select_name_dish = State()
    select_category_product = State()
    select_name_product = State()
    select_netto_product = State()
    select_choice_next = State()


# Получаем ID текущего админа
async def make_changes_command(message: types.Message):
    global ID
    if message.from_user.id in conf.ID_ADMIN:
        ID = message.from_user.id
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await message.reply('Ты повелеваешь мной', reply_markup=start_keyboard)
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
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await message.reply('OK', reply_markup=start_keyboard)


async def choice_menu_and_products(callback_query: types.CallbackQuery):
    if callback_query.from_user.id == ID:
        keyboard_products_menu = keyboards_for_admin.create_keyboard_products_menu()
        await callback_query.message.edit_text(text='Выбери что хочешь посмотреть:',
                                               reply_markup=keyboard_products_menu)


async def select_category_dish(callback_query: types.CallbackQuery):
    keyboard_category_dishes = keyboards_for_admin.create_keyboard_category_dishes()
    await callback_query.message.edit_text(text='Выбери категорию блюда', reply_markup=keyboard_category_dishes)
    await FSMAdminSelectCategoryMenu.select_category.set()


async def select_choice_price_or_structure_dish(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['category_dishes'] = callback_query.data
    keyboard_price_or_structure = keyboards_for_admin.create_keyboard_price_or_structure()
    await callback_query.message.edit_text(text='Посмотреть цену или состав?', reply_markup=keyboard_price_or_structure)
    await FSMAdminSelectCategoryMenu.select_choice_price_or_structure.set()


async def sending_name_price_dish(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:

            names_prices_menu = data_request.get_name_price_menu(conf.type_menu[data['category_dishes']])
        await bot.send_message(ID, text=f'{names_prices_menu[0]} цена - {names_prices_menu[1]}')
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await bot.send_message(ID, 'В начало', reply_markup=start_keyboard)
        await state.finish()
    except Exception as exp:
        await state.finish()
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await callback_query.message.edit_text(f'Ошибка - {exp}, попробуй сначала', reply_markup=start_keyboard)


async def select_name_dish_for_sending(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        keyboard_dishes = keyboards_for_admin.create_keyboard_dishes(data['category_dishes'])
    await callback_query.message.edit_text(text='Выбери что хочешь посмотреть', reply_markup=keyboard_dishes)
    await FSMAdminSelectCategoryMenu.select_name_dish.set()


async def sending_structure_dish(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        data_structures = data_request.get_structure(callback_query.data)
        for structure in data_structures:
            await bot.send_message(ID, text=f'Продукт - {structure[0]} Брутто -{structure[1]} Нетто -{structure[2]}'
                                            f' Цена за килограмм -{structure[3]} Цена в блюде -{structure[4]}')
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await bot.send_message(ID, text='В начало', reply_markup=start_keyboard)
        await state.finish()
    except Exception as exp:
        await state.finish()
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await callback_query.message.edit_text(f'Ошибка - {exp}, попробуй сначала', reply_markup=start_keyboard)


async def select_category_products(callback_query: types.CallbackQuery):
    if callback_query.from_user.id == ID:
        keyboard_category_products = keyboards_for_admin.create_keyboard_category_products()
        await callback_query.message.edit_text(text='Выбери категорию продуктов',
                                               reply_markup=keyboard_category_products)
        await FSMAdminSelectCategoryProducts.select_category.set()


async def sending_name_price_product(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        category = callback_query.data
        name_price_percent_products = data_request.get_name_price_from_table_products(category)
        for name_price_percent in name_price_percent_products:
            await bot.send_message(ID, text=name_price_percent)
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await bot.send_message(ID, 'В начало', reply_markup=start_keyboard)
        await state.finish()
    except Exception as exp:
        await state.finish()
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await callback_query.message.edit_text(f'Ошибка - {exp}, попробуй сначала', reply_markup=start_keyboard)


async def select_category_for_change(callback_query: types.CallbackQuery):
    if callback_query.from_user.id == ID:
        await FSMAdminChangesProduct.select_changes_category.set()
        keyboard_category_products = keyboards_for_admin.create_keyboard_category_products()
        await callback_query.message.edit_text(text='Выбери категорию продуктов',
                                               reply_markup=keyboard_category_products)


async def select_name_product_for_change(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['category_product'] = callback_query.data
    keyboard_products = keyboards_for_admin.create_keyboard_products(data['category_product'])
    await callback_query.message.edit_text(text='Выбери продукт', reply_markup=keyboard_products)
    await FSMAdminChangesProduct.next()


async def select_price_product_for_change(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['name_product'] = callback_query.data
    await callback_query.message.edit_text(text='Укажи цену')
    await FSMAdminChangesProduct.next()


async def select_percent_losses_product_for_change(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price_product'] = message.text
    keyboard_choice = keyboards_for_admin.create_keyboard_yes_or_no()
    await message.reply(text='Изменить процент потерь?', reply_markup=keyboard_choice)
    await FSMAdminChangesProduct.next()


async def select_choice_write_percent_losses(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'No':
        async with state.proxy() as data:
            percent_loss = data_request.get_percent_loss(data['name_product'])
            data['percent_loss'] = percent_loss
        keyboard_yes = keyboards_for_admin.create_keyboard_yes()
        await callback_query.message.edit_text(text=f'Процент потерь будет {data["percent_loss"]}?',
                                               reply_markup=keyboard_yes)
        await FSMAdminChangesProduct.select_changes_finish.set()
    else:
        await callback_query.message.edit_text(text='Укажи процент потерь:')
        await FSMAdminChangesProduct.select_changes_percent_choice.set()


async def write_percent_losses(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['percent_loss'] = message.text
    keyboard_yes = keyboards_for_admin.create_keyboard_yes()
    await message.answer(text=f'Процент потерь будет {data["percent_loss"]}?', reply_markup=keyboard_yes)
    await FSMAdminChangesProduct.next()


async def change_values_from_product(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            changing_data.change_name_price_percent_in_table(data['name_product'],
                                                             int(data['price_product']), int(data['percent_loss']))
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await callback_query.message.edit_text(text='Значение обновлено', reply_markup=start_keyboard)
        await state.finish()
    except Exception as exp:
        await state.finish()
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await callback_query.message.edit_text(f'Ошибка - {exp}, попробуй сначала', reply_markup=start_keyboard)


async def select_category_product_for_add(callback_query: types.CallbackQuery):
    if callback_query.from_user.id == ID:
        await FSMAdminAddProduct.select_category_for_add.set()
        keyboard_category_products = keyboards_for_admin.create_keyboard_category_products()
        await callback_query.message.edit_text(text='Выбери категорию продукта для добавления',
                                               reply_markup=keyboard_category_products)


async def select_name_product_for_add(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['category_product'] = callback_query.data
    await callback_query.message.edit_text(f'Напиши название продукта:')
    await FSMAdminAddProduct.next()


async def select_price_product_for_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_product'] = message.text
    await message.reply(f'Напиши цену для {data["name_product"]}:')
    await FSMAdminAddProduct.next()


async def select_percent_losses_product_for_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price_product'] = message.text
    await message.reply(f'Напиши процент потерь для {data["name_product"]}, если нет то укажи 0:')
    await FSMAdminAddProduct.next()


async def add_new_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['percent_product'] = message.text
    try:
        changing_data.adding_row_to_table(data['category_product'], data['name_product'],
                                          data['price_product'], data['percent_product'])
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await message.reply('Продукт добавлен', reply_markup=start_keyboard)
        await state.finish()
    except Exception as exp:
        await state.finish()
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await message.reply(f'Ошибка - {exp}, попробуй сначала', reply_markup=start_keyboard)


async def del_choice_menu_and_product(callback_query: types.CallbackQuery):
    if callback_query.from_user.id == ID:
        keyboard_for_deleting = keyboards_for_admin.create_keyboard_for_deleting()
        await callback_query.message.edit_text(text='Выбери откуда удалять', reply_markup=keyboard_for_deleting)


async def select_category_menu_for_del(callback_query: types.CallbackQuery):
    keyboard_category_dishes = keyboards_for_admin.create_keyboard_category_dishes()
    await callback_query.message.edit_text(text='Выбери категорию', reply_markup=keyboard_category_dishes)
    await FSMAdminDelMenu.select_del_category.set()


async def select_name_dish_for_del(callback_query: types.CallbackQuery):
    category_menu = callback_query.data
    btn_type_menu = keyboards_for_admin.create_keyboard_name_from_menu(conf.type_menu[category_menu])
    await callback_query.message.edit_text(text='Выбери что удалять', reply_markup=btn_type_menu)
    await FSMAdminDelMenu.next()


async def deleting_dish(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        name_dish = callback_query.data
        changing_data.deleting_table_and_row(name_dish)
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await callback_query.message.edit_text(text=f'Удалено {name_dish}', reply_markup=start_keyboard)
        await state.finish()
    except Exception as exp:
        await state.finish()
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await callback_query.message.edit_text(f'Ошибка - {exp}, попробуй сначала', reply_markup=start_keyboard)


async def select_category_product_for_del(callback_query: types.CallbackQuery):
    if callback_query.from_user.id == ID:
        await FSMAdminDelProducts.select_del_category.set()
        keyboard_category_products = keyboards_for_admin.create_keyboard_category_products()
        await callback_query.message.edit_text(text='Выбери категорию', reply_markup=keyboard_category_products)


async def select_name_product_for_del(callback_query: types.CallbackQuery):
    category_product = callback_query.data
    keyboard_products = keyboards_for_admin.create_keyboard_products(category_product)
    await callback_query.message.edit_text(f'Выбери что удалять', reply_markup=keyboard_products)
    await FSMAdminDelProducts.next()


async def deleting_product(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        name_product = callback_query.data
        changing_data.deleting_row(name_product)
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await callback_query.message.edit_text(f'Удалено {name_product}', reply_markup=start_keyboard)
        await state.finish()
    except Exception as exp:
        await state.finish()
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await callback_query.message.edit_text(f'Ошибка - {exp}, попробуй сначала', reply_markup=start_keyboard)


async def select_name_dish_for_add(callback_query: types.CallbackQuery):
    if callback_query.from_user.id == ID:
        await FSMAdminAddDishes.select_category_dish.set()
        await bot.send_message(ID, 'Напиши название блюда')


async def select_category_dish_for_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_dish'] = message.text
    keyboard_category_dishes = keyboards_for_admin.create_keyboard_category_dishes()
    await message.reply('Выбери категорию блюда:', reply_markup=keyboard_category_dishes)
    await FSMAdminAddDishes.next()


async def select_products_for_add(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['category_dish'] = callback_query.data
    category_products = keyboards_for_admin.create_keyboard_category_products()
    await callback_query.message.edit_text('Выбери продукты входящие в состав. Сначала категорию продуктов:',
                                           reply_markup=category_products)
    await FSMAdminAddDishes.next()


async def select_name_product_for_add_dish(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['category_product'] = callback_query.data
    keyboard_products = keyboards_for_admin.create_keyboard_products(data['category_product'])
    await callback_query.message.edit_text('Выбери продукт', reply_markup=keyboard_products)
    await FSMAdminAddDishes.next()


async def select_netto_product_for_add_dish(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['name_product'] = callback_query.data
    await callback_query.message.edit_text('Напиши нетто')
    await FSMAdminAddDishes.next()


async def get_brutto_summed_product(name_product, netto_product):
    percent, price = data_request.get_percent_price(name_product)
    brutto_prod = round((float(netto_product) / (100 - float(percent))) * 100)
    summed = round((int(price) * brutto_prod) / 1000)
    return brutto_prod, summed, price


async def select_choice_next_or_stop(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['netto_product'] = message.text
        brutto_prod, summed, price = await get_brutto_summed_product(name_product=data['name_product'],
                                                                     netto_product=data['netto_product'])
        data['brutto_product'] = brutto_prod
        data['summed'] = summed
        data['price'] = price
    keyboard_next_or_stop = keyboards_for_admin.create_keyboard_next_or_stop(data['name_dish'])
    await message.answer('Продолжить выбор или закончить?', reply_markup=keyboard_next_or_stop)
    await FSMAdminAddDishes.next()


products = []
netto_products = []
brutto_products = []
prices = []
summeds = []


async def add_new_dish(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            products.append(data['name_product'])
            netto_products.append(data['netto_product'])
            brutto_products.append(data['brutto_product'])
            prices.append(data['price'])
            summeds.append(data['summed'])

        keyboard_category_products = keyboards_for_admin.create_keyboard_category_products()
        if callback_query.data == data['name_dish']:
            await callback_query.answer('Продолжаем')
            await callback_query.message.edit_text(
                text='Выбери продукты входящие в состав. Сначала категорию продуктов:',
                reply_markup=keyboard_category_products)
            await FSMAdminAddDishes.select_category_product.set()
        elif callback_query.data == 'STOP':
            data_products = zip(products, netto_products, brutto_products, prices, summeds)

            changing_data.creating_dish_table(data['name_dish'])
            for data_product in list(data_products):
                name_product = data_product[0]
                brutto_product = data_product[2]
                netto_product = data_product[1]
                price_kg = data_product[3]
                summed = data_product[4]
                changing_data.add_dish_to_table(data['name_dish'], name_product, brutto_product, netto_product,
                                                price_kg,
                                                summed)
            sum = data_request.get_sum(data['name_dish'])
            sum = float(sum)
            netto = data_request.get_netto(data['name_dish'])
            netto = float(netto)
            price_per_kg = round((sum * 1000) / netto)
            changing_data.add_dish_to_table_menu(category=data['category_dish'], name=data['name_dish'],
                                                 price=price_per_kg)
            start_keyboard = keyboards_for_admin.create_admin_keyboard()
            await callback_query.message.edit_text(f'{data["name_dish"]} добавлено', reply_markup=start_keyboard)
            products.clear()
            netto_products.clear()
            brutto_products.clear()
            prices.clear()
            summeds.clear()
            await state.finish()
    except Exception as exp:
        await state.finish()
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await callback_query.message.edit_text(f'Ошибка - {exp}, попробуй сначала', reply_markup=start_keyboard)


async def update_dishes(callback_query: types.CallbackQuery):
    try:
        if callback_query.from_user.id == ID:
            await callback_query.message.edit_text(text='Идёт обновление')
            changing_data.update_price()
            start_keyboard = keyboards_for_admin.create_admin_keyboard()
            await bot.send_message(ID, text='Обновлено', reply_markup=start_keyboard)
    except Exception as exp:
        start_keyboard = keyboards_for_admin.create_admin_keyboard()
        await callback_query.message.edit_text(f'Ошибка - {exp}, попробуй сначала', reply_markup=start_keyboard)


# Регситрируем хэндлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands='admin', state=None)

    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")

    dp.register_callback_query_handler(choice_menu_and_products, lambda k: k.data == 'Просмотр')
    dp.register_callback_query_handler(select_category_dish, lambda c: c.data == 'Menu', state=None)
    dp.register_callback_query_handler(select_choice_price_or_structure_dish,
                                       state=FSMAdminSelectCategoryMenu.select_category)
    dp.register_callback_query_handler(sending_name_price_dish, lambda c: c.data == 'Цена блюда',
                                       state=FSMAdminSelectCategoryMenu.select_choice_price_or_structure)
    dp.register_callback_query_handler(select_name_dish_for_sending, lambda c: c.data == 'Состав блюда',
                                       state=FSMAdminSelectCategoryMenu.select_choice_price_or_structure)
    dp.register_callback_query_handler(sending_structure_dish, state=FSMAdminSelectCategoryMenu.select_name_dish)

    dp.register_callback_query_handler(select_category_products, lambda c: c.data == 'Products', state=None)
    dp.register_callback_query_handler(sending_name_price_product,
                                       state=FSMAdminSelectCategoryProducts.select_category)

    dp.register_callback_query_handler(select_category_for_change, lambda k: k.data == 'Изменение')
    dp.register_callback_query_handler(select_name_product_for_change,
                                       state=FSMAdminChangesProduct.select_changes_category)
    dp.register_callback_query_handler(select_price_product_for_change,
                                       state=FSMAdminChangesProduct.select_changes_name)
    dp.register_message_handler(select_percent_losses_product_for_change,
                                state=FSMAdminChangesProduct.select_changes_price)
    dp.register_callback_query_handler(select_choice_write_percent_losses,
                                       state=FSMAdminChangesProduct.select_changes_percent)
    dp.register_message_handler(write_percent_losses, state=FSMAdminChangesProduct.select_changes_percent_choice)
    dp.register_callback_query_handler(change_values_from_product, state=FSMAdminChangesProduct.select_changes_finish)

    dp.register_callback_query_handler(select_category_product_for_add,
                                       lambda c: c.data == 'Добавление Продуктов', state=None)
    dp.register_callback_query_handler(select_name_product_for_add, state=FSMAdminAddProduct.select_category_for_add)
    dp.register_message_handler(select_price_product_for_add, state=FSMAdminAddProduct.select_name_product)
    dp.register_message_handler(select_percent_losses_product_for_add, state=FSMAdminAddProduct.select_price_product)
    dp.register_message_handler(add_new_product, state=FSMAdminAddProduct.select_percent_product)

    dp.register_callback_query_handler(del_choice_menu_and_product, lambda c: c.data == 'Удаление', state=None)
    dp.register_callback_query_handler(select_category_menu_for_del, lambda c: c.data == 'Del menu')
    dp.register_callback_query_handler(select_name_dish_for_del, state=FSMAdminDelMenu.select_del_category)
    dp.register_callback_query_handler(deleting_dish, state=FSMAdminDelMenu.select_del_name)

    dp.register_callback_query_handler(select_category_product_for_del,
                                       lambda c: c.data == 'Del products', state=None)
    dp.register_callback_query_handler(select_name_product_for_del, state=FSMAdminDelProducts.select_del_category)
    dp.register_callback_query_handler(deleting_product, state=FSMAdminDelProducts.select_del_name_product)

    dp.register_callback_query_handler(select_name_dish_for_add, lambda c: c.data == 'Добавление Блюда', state=None)
    dp.register_message_handler(select_category_dish_for_add, state=FSMAdminAddDishes.select_category_dish)
    dp.register_callback_query_handler(select_products_for_add, state=FSMAdminAddDishes.select_name_dish)
    dp.register_callback_query_handler(select_name_product_for_add_dish,
                                       state=FSMAdminAddDishes.select_category_product)
    dp.register_callback_query_handler(select_netto_product_for_add_dish,
                                       state=FSMAdminAddDishes.select_name_product)
    dp.register_message_handler(select_choice_next_or_stop, state=FSMAdminAddDishes.select_netto_product)
    dp.register_callback_query_handler(add_new_dish, state=FSMAdminAddDishes.select_choice_next)

    dp.register_callback_query_handler(update_dishes, lambda c: c.data == 'Обновление')
