# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from conf import type_product, type_menu
from database import data_request


# Стартовая клавитура админа
def create_admin_keyboard():
    admin_keyboard = InlineKeyboardMarkup(row_width=2)
    btn_view = InlineKeyboardButton('Просмотр', callback_data='Просмотр')
    btn_changing = InlineKeyboardButton(text='Изменение', callback_data='Изменение')
    btn_add_products = InlineKeyboardButton(text='Добавление Продуктов', callback_data='Добавление Продуктов')
    btn_add_dish = InlineKeyboardButton(text='Добавление Блюда', callback_data='Добавление Блюда')
    btn_delete_data = InlineKeyboardButton(text='Удаление', callback_data='Удаление')
    btn_update = InlineKeyboardButton(text='Обновление цен', callback_data='Обновление')
    admin_keyboard.add(btn_view, btn_changing, btn_add_products, btn_add_dish, btn_delete_data, btn_update)
    return admin_keyboard


# Клавиатура "продукты" "меню"
def create_keyboard_products_menu():
    keyboard_products_menu = InlineKeyboardMarkup(row_width=2)
    btn_products = InlineKeyboardButton('Продукты', callback_data='Products')
    btn_menu = InlineKeyboardButton('Меню', callback_data='Menu')
    keyboard_products_menu.add(btn_products, btn_menu)
    return keyboard_products_menu


# Клавиатура для удаления
def create_keyboard_for_deleting():
    keyboard_del_prod_menu = InlineKeyboardMarkup(row_width=2)
    btn_del_prod = InlineKeyboardButton('Удаление из продуктов', callback_data='Del products')
    btn_del_menu = InlineKeyboardButton('Удаление из меню', callback_data='Del menu')
    keyboard_del_prod_menu.add(btn_del_prod, btn_del_menu)
    return keyboard_del_prod_menu


# Клавиатура с категориями продуктов
def create_keyboard_category_products():
    keyboard_category_products = InlineKeyboardMarkup(row_width=2)
    for category in type_product.keys():
        btn_category = InlineKeyboardButton(text=category, callback_data=category)
        keyboard_category_products.add(btn_category)
    return keyboard_category_products


# Клавиатура с категориями блюд
def create_keyboard_category_dishes():
    keyboard_category_dishes = InlineKeyboardMarkup(row_width=2)
    for category in type_menu.keys():
        btn_category = InlineKeyboardButton(text=category, callback_data=category)
        keyboard_category_dishes.insert(btn_category)
    return keyboard_category_dishes


# Клавиатура продуктов
def create_keyboard_products(category):
    keyboard_products = InlineKeyboardMarkup(row_width=2)
    products = data_request.get_names_for_keyboard(category)
    for product in products:
        btn_product = InlineKeyboardButton(text=product, callback_data=product)
        keyboard_products.add(btn_product)
    return keyboard_products


# Клавиатура продолжения
def create_keyboard_next_or_stop(name_dish):
    keyboard_next_or_stop = InlineKeyboardMarkup(row_width=2)
    btn_next = InlineKeyboardButton(text='Продолжить', callback_data=f'{name_dish}')
    btn_stop = InlineKeyboardButton(text='Стоп', callback_data='STOP')
    keyboard_next_or_stop.add(btn_next, btn_stop)
    return keyboard_next_or_stop


# Клавиатура категорий menu
def create_keyboard_name_from_menu(type):
    keyboard_name_from_menu = InlineKeyboardMarkup(row_width=2)
    names = data_request.get_name_menu(type)
    for name in names:
        btn_name = InlineKeyboardButton(text=name, callback_data=name)
        keyboard_name_from_menu.insert(btn_name)
    return keyboard_name_from_menu


# Клавиатура да/нет
def create_keybord_yes_or_no():
    keybord_yes_no = InlineKeyboardMarkup(row_width=2)
    btn_yes = InlineKeyboardButton(text='Да', callback_data='Yes')
    btn_no = InlineKeyboardButton(text='Нет', callback_data='No')
    keybord_yes_no.add(btn_yes, btn_no)
    return keybord_yes_no


# Клавиатура да
def create_keybord_yes():
    keybord_yes = InlineKeyboardMarkup()
    btn_yes = InlineKeyboardButton(text='Да', callback_data='ye')
    keybord_yes.insert(btn_yes)
    return keybord_yes
