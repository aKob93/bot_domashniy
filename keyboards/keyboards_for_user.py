# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Клавиатура для пользователя
def create_user_keyboard():
    client_keyboard = InlineKeyboardMarkup(row_width=1)
    btn_availability_dishes = InlineKeyboardButton(text='Узнать, какие блюда в наличии', callback_data='availability')
    btn_order_menu = InlineKeyboardButton(text='Показать меню для заказа', callback_data='order_menu')
    client_keyboard.add(btn_availability_dishes, btn_order_menu)
    return client_keyboard