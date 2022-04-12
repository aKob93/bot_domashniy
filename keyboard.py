# -*- coding: utf-8 -*-
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from conf import type_product
from database import sqlite_db


btn_availability_dishes = InlineKeyboardButton(text='Узнать, какие блюда в наличии', callback_data='availability')
btn_order_menu = InlineKeyboardButton(text='Показать меню для заказа', callback_data='order_menu')

check_menu = InlineKeyboardMarkup(row_width=2)
check_menu.insert(btn_availability_dishes)
check_menu.insert(btn_order_menu)


#Кнопки клавиатуры админа
btn_select = KeyboardButton('/Просмотр')
btn_changing_data = KeyboardButton(text='/Изменение')
btn_add_data = KeyboardButton(text='/Добавление')
btn_delete_data = KeyboardButton(text='/Удаление')
menu_admin = ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
menu_admin.add(btn_select, btn_changing_data, btn_add_data, btn_delete_data)



#Кнопки категорий
def btn():
    greet_kb = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    for i in type_product.keys():
        button_hi = KeyboardButton(i)
        greet_kb.insert(button_hi)
    return greet_kb


#КНопка продуктов
def btn_prod(i):
    btns_product = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    btn = sqlite_db.select_for_btn(i)
    for b in btn:
        button1 = KeyboardButton(b)
        btns_product.insert(button1)
    return btns_product









