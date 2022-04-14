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
btn_select = InlineKeyboardButton('Просмотр', callback_data='Просмотр')
btn_changing_data = InlineKeyboardButton(text='Изменение', callback_data='Изменение')
btn_add_data = InlineKeyboardButton(text='Добавление Продуктов', callback_data='Добавление Продуктов')
btn_add_dish = InlineKeyboardButton(text='Добавление Блюда', callback_data='Добавление Блюда')
btn_delete_data = InlineKeyboardButton(text='Удаление', callback_data='Удаление')
menu_admin = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
menu_admin.add(btn_select, btn_changing_data, btn_add_data, btn_add_dish, btn_delete_data)



#Кнопки категорий
def btn():
    greet_kb = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
    for i in type_product.keys():
        button_hi = InlineKeyboardButton(text=i, callback_data=i)
        greet_kb.insert(button_hi)
    return greet_kb


#КНопка продуктов
def btn_prod(i):
    btns_product = InlineKeyboardMarkup(row_width=3, one_time_keyboard=True)
    btn = sqlite_db.select_for_btn(i)
    for b in btn:
        button1 = InlineKeyboardButton(text=b, callback_data=b)
        btns_product.insert(button1)
    return btns_product

#Кнопка продолжения
def btn_choice(name_dish):
    btn1 = InlineKeyboardButton(text='Продолжить', callback_data=f'{name_dish}')
    btn2 = InlineKeyboardButton(text='СТОП', callback_data='STOP')

    btn_ch = InlineKeyboardMarkup(row_width=2)
    btn_ch.add(btn1, btn2)
    return btn_ch


    # btn_ch = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    # btn1 = ('Продолжить')
    # btn2 = ('/Закончить')
    # btn_ch.add(btn1, btn2)
    # return btn_ch









