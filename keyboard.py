# -*- coding: utf-8 -*-
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from conf import type_product

btn_availability_dishes = InlineKeyboardButton(text='Узнать, какие блюда в наличии', callback_data='availability')
btn_order_menu = InlineKeyboardButton(text='Показать меню для заказа', callback_data='order_menu')

check_menu = InlineKeyboardMarkup(row_width=2)
check_menu.insert(btn_availability_dishes)
check_menu.insert(btn_order_menu)


#Кнопки клавиатуры админа

btn_select = KeyboardButton('/Просмотр')
btn_changing_data = KeyboardButton(text='/Изменение')
btn_delete_data = KeyboardButton(text='/Удаление')
menu_admin = ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
menu_admin.add(btn_select, btn_changing_data, btn_delete_data)

# btn_select = InlineKeyboardButton(text='Просмотр данных', callback_data='select_dat')
# btn_changing_data = InlineKeyboardButton(text='Изменение данных', callback_data='changing_data')
# btn_delete_data = InlineKeyboardButton(text='Удаление данных', callback_data='delete_data')
#
# menu_admin = InlineKeyboardMarkup(row_width=1)
#
# menu_admin.add(btn_select, btn_changing_data, btn_delete_data)



#Кнопки продуктов
def btn(*type_prod):
    greet_kb = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    for i in type_product.keys():
        button_hi = KeyboardButton(i)
        greet_kb.insert(button_hi)
    return greet_kb






