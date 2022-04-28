# -*- coding: utf-8 -*-
import re
from conf import type_product, type_menu
from database.sqlite_db import CUR, PATTERN


# Выбор из таблицы название продукта, цену и процент потерь
def get_name_price_from_table_products(category):
    CUR.execute(f'SELECT name_product, price, percent_loss FROM products '
                f'WHERE type_product = "{type_product[category]}";')
    rows_data = CUR.fetchall()
    name_price_percent_products = [re.sub(PATTERN, '', str(data)) for data in rows_data]
    return name_price_percent_products


# Выбор названия продуктов для создания кнопок клавиатуры
def get_names_for_keyboard(category):
    CUR.execute(f'SELECT name_product FROM products WHERE type_product = "{type_product[category]}";')
    rows_data = CUR.fetchall()
    names_product = [re.sub(PATTERN, '', str(data)) for data in rows_data]
    return names_product


# Получние процента потерь и цены
def get_percent_price(name_prod):
    percent = CUR.execute(f'SELECT percent_loss FROM products WHERE name_product = "{name_prod}";').fetchall()
    price = CUR.execute(f'SELECT price FROM products WHERE name_product = "{name_prod}";').fetchall()
    percent = re.sub(PATTERN, '', str(percent))
    price = re.sub(PATTERN, '', str(price))
    return percent, price


# Получение суммы из столбца summ
def get_sum(name_dish):
    CUR.execute(f'SELECT SUM(summ) FROM "{name_dish}";')
    summar = CUR.fetchall()
    summar = re.sub(PATTERN, '', str(summar))
    return summar


# Получение нетто
def get_netto(name_dish):
    CUR.execute(f'SELECT SUM(netto) FROM "{name_dish}";')
    netto = CUR.fetchall()
    netto = re.sub(PATTERN, '', str(netto))
    return netto


# Получени процента потерь
def get_percent_loss(name_product):
    CUR.execute(f'SELECT percent_loss FROM products WHERE name_product = "{name_product}";')
    percent_loss = CUR.fetchall()
    percent_loss = re.sub(PATTERN, '', str(percent_loss))
    return percent_loss


# Получение имён из таблицы menu
def get_name_menu(type_name):
    CUR.execute(f"SELECT name FROM menu WHERE type_menu = '{type_name}';")
    rows_data = CUR.fetchall()
    names_menu = [re.sub(PATTERN, '', str(data)) for data in rows_data]
    return names_menu


# Получение имён и цен из menu
def get_name_price_menu(type_name):
    CUR.execute(f"SELECT name, price FROM menu WHERE type_menu = '{type_name}';")
    rows_data = CUR.fetchall()
    names_prices_products = [re.sub(PATTERN, '', str(data)) for data in rows_data]
    names_prices_products = names_prices_products[0].split()
    return names_prices_products


# Получение блюд из меню
def get_name_from_menu():
    CUR.execute('SELECT name FROM menu;')
    rows_data = CUR.fetchall()
    names_from_menu = [re.sub(PATTERN, '', str(data)) for data in rows_data]
    return names_from_menu

# Получение блюд из меню по категориям
def get_name_dish_from_menu(category):
    CUR.execute(f'SELECT name FROM menu WHERE type_menu = "{type_menu[category]}";')
    rows_data = CUR.fetchall()
    names_from_menu = [re.sub(PATTERN, '', str(data)) for data in rows_data]
    return names_from_menu

# Получение имён и цен из products
def get_names_prices_from_product():
    names_product = CUR.execute('SELECT name_product FROM products;').fetchall()
    prices_product = CUR.execute('SELECT price FROM products;').fetchall()
    names_from_product = [re.sub(PATTERN, '', str(data)) for data in names_product]
    prices_from_product = [re.sub(PATTERN, '', str(data)) for data in prices_product]
    names_prices = zip(names_from_product, prices_from_product)
    return list(names_prices)


# Получени состава продуктов из блюда
def get_product_from_dish(dish):
    try:
        CUR.execute(f'SELECT products FROM "{dish}";')
        name_products = CUR.fetchall()
        name_products = re.sub(PATTERN, '', str(name_products))
        return name_products
    except Exception:
        pass


# Получение брутто
def get_brutto(name, product):
    CUR.execute(f'SELECT brutto FROM "{name}" WHERE products = "{product}";')
    brutto = CUR.fetchall()
    brutto = re.sub(PATTERN, '', str(brutto))
    return brutto

# Получние состава блюда
def get_structure(name_dish):
    CUR.execute(f'SELECT products, brutto, netto, price_kg, summ FROM "{name_dish}";')
    structures = CUR.fetchall()
    data_structures = []
    for structure in structures:
        structure = re.sub("[](')[]", '', str(structure))
        data_structures.append(structure.split(','))
    return data_structures

