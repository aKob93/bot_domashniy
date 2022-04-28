# -*- coding: utf-8 -*-
from conf import type_product, type_menu
from database.sqlite_db import CUR, BASE
from database import data_request


# Изменение цены, процента потерь и имени в таблице products
def change_name_price_percent_in_table(name_product, price, percent):
    CUR.execute(f'UPDATE products SET price = {price}, percent_loss = {percent} '
                f'WHERE name_product = "{name_product}";')
    BASE.commit()


# Добавление строки в таблицу products
def adding_row_to_table(category, name, price, percent_off):
    CUR.execute(f'INSERT INTO products (type_product, name_product, price, percent_loss) VALUES '
                f'("{type_product[category]}", "{name}", {price}, {percent_off});')
    BASE.commit()


# Удаление строки из products
def deleting_row(name):
    CUR.execute(f'DELETE FROM products WHERE name_product = "{name}";')
    BASE.commit()


# Удаление таблицы и строки их menu
def deleting_table_and_row(name):
    CUR.execute(f'DROP TABLE "{name}";')
    CUR.execute(f'DELETE FROM menu WHERE name = "{name}";')
    BASE.commit()


# Создание таблицы с блюдом
def creating_dish_table(name_dish):
    CUR.execute(f'CREATE TABLE "{name_dish}" (products TEXT, brutto REAL, netto REAL, price_kg REAL, summ REAL);')
    BASE.commit()


# Добавление блюд в таблицу
def add_dish_to_table(name_dishes, name_product, brutto_product, netto_product, price_kg, summ):
    CUR.execute(f'INSERT INTO "{name_dishes}" (products, brutto, netto, price_kg, summ) '
                f'VALUES ("{name_product}", {brutto_product}, {netto_product}, {price_kg}, {summ});')
    BASE.commit()


# Добавление блюда в таблицу menu
def add_dish_to_table_menu(category, name, price):
    CUR.execute(f'INSERT INTO menu (type_menu, name, price) VALUES ("{type_menu[category]}", "{name}", {price});')
    BASE.commit()


# обновление цен и суммы в products
def update_price_kg_sum_in_products():
    names_from_menu = data_request.get_name_from_menu()
    names_prices = data_request.get_names_prices_from_product()

    for name in names_from_menu:
        names_product = data_request.get_product_from_dish(name)

        for name_price in names_prices:

            try:
                if name_price[0] in names_product:
                    price = float(name_price[1])
                    brutto = data_request.get_brutto(name, name_price[0])
                    brutto = float(brutto)
                    summar = round(price * brutto / 1000)
                    CUR.execute(
                        f'UPDATE "{name}" SET price_kg = {price}, summ = {summar} WHERE products = "{name_price[0]}";')
                    BASE.commit()

            except Exception:
                continue


# Обновление цены в menu
def update_price_in_menu():
    names_from_menu = data_request.get_name_from_menu()

    for name in names_from_menu:
        try:

            summar = data_request.get_sum(name)
            netto = data_request.get_netto(name)
            netto = float(netto)

            price = round((float(summar) * 1000) / netto)
            CUR.execute(f'UPDATE menu SET price = {price} WHERE name = "{name}";')
            BASE.commit()
        except Exception:
            continue


# обновление цен в таблице menu
def update_price():
    update_price_kg_sum_in_products()
    update_price_in_menu()
