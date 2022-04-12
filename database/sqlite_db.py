import re
import sqlite3 as sq
from conf import type_product

#Создание/подключение бд
def sql_start():
    global base, cur
    base = sq.connect('menu_domashniy.db')#коннект к базе
    cur = base.cursor()#создание курсора
    if base:
        print('DataBase connected OK')
    base.execute('CREATE TABLE IF NOT EXISTS products(type_product TEXT, name_product TEXT, price TEXT)')#создаём таблицу бд(excecute - создание если нет)
    base.commit()#сохранение изменений


#Выбор из таблицы название продукат и цену
def select_name_price_product(category):
    cur.execute(f'SELECT name_product, price FROM products WHERE type_product = "{type_product[category]}"')
    rows_data = cur.fetchall()
    name_price_products = []
    for data in rows_data:
        patern = "[(',)]"
        data = re.sub(patern, '', str(data))#убирает лишние символы по patern

        name_price_products.append(data)
    return name_price_products

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO products VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()
