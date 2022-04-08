# -*- coding: utf-8 -*-
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


btn_availability_dishes = InlineKeyboardButton(text='Узнать, какие блюда в наличии', callback_data='availability')
btn_order_menu = InlineKeyboardButton(text='Показать меню для заказа', callback_data='order_menu')

check_menu = InlineKeyboardMarkup(row_width=2)
check_menu.insert(btn_availability_dishes)
check_menu.insert(btn_order_menu)


#Кнопки клавиатуры админа
button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton('/Удалить')
#TODO добавить кнопку просмотра

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_delete)