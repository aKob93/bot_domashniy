import re
import sqlite3 as sq
from conf import type_product

#Создание/подключение бд
def sql_start():
    global base, cur
    base = sq.connect('menu_domashniyTEST.db')#коннект к базе
    cur = base.cursor()#создание курсора
    if base:
        print('DataBase connected OK')
    base.execute('CREATE TABLE IF NOT EXISTS products(type_product TEXT, name_product TEXT, price TEXT)')#создаём таблицу бд(excecute - создание если нет)
    base.commit()#сохранение изменений


#Выбор из таблицы название продукта и цену
def select_name_price_product(category):
    cur.execute(f'SELECT name_product, price FROM products WHERE type_product = "{type_product[category]}"')
    rows_data = cur.fetchall()
    name_price_products = []
    for data in rows_data:
        patern = "[(',)]"
        data = re.sub(patern, '', str(data))#убирает лишние символы по patern

        name_price_products.append(data)
    return name_price_products

#Выбор данных для клавиатуры название продукта
def select_for_btn(i):
    cur.execute(f'SELECT name_product FROM products WHERE type_product = "{type_product[i]}"')
    rows_data = cur.fetchall()
    name_price_products = []
    for data in rows_data:
        patern = "[(',)]"
        data = re.sub(patern, '', str(data))#убирает лишние символы по patern
        name_price_products.append(data)
    return name_price_products


#Изменение данных в таблице
def select_chages(name_product, price):
    cur.execute(f'UPDATE products SET price = {price} WHERE name_product = "{name_product}";')
    base.commit()

#Добавление данных
async def sql_add_command(category, name, price):
    cur.execute(f'INSERT INTO products (type_product, name_product, price) VALUES ("{type_product[category]}", "{name}", {price})')
    base.commit()
