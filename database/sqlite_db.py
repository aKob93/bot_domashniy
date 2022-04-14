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
    cur.execute(f'INSERT INTO products (type_product, name_product, price) VALUES '
                f'("{type_product[category]}", "{name}", {price})')
    base.commit()



#Удаление данных
async def sql_del(name):
    # print(f'DELETE FROM products WHERE name_product = "{name}";')
    cur.execute(f'DELETE FROM products WHERE name_product = "{name}";')
    base.commit()

# подсчёт брутто цена за кг продукта
async def get_percent_price(prod):

    percent = cur.execute(f'SELECT percent_off FROM products WHERE name_product = "{prod}";').fetchall()
    price = cur.execute(f'SELECT price FROM products WHERE name_product = "{prod}"').fetchall()
    patern = "[](',)[]"
    percent = re.sub(patern, '', str(percent))
    price = re.sub(patern, '', str(price))
    return percent, price


#Создание таблицыс блюдом
async def create_table_dish(name_dishes):
    cur.execute(f'CREATE TABLE {name_dishes} (products TEXT, brutto REAL, netto REAL, price_kg REAL, summ REAL)')
    base.commit()

#Добавление блюд в таблицу
async def add_table_dish(name_dishes, name_product, brutto_product, netto_product, price_kg, summ):
    cur.execute(f'INSERT INTO {name_dishes} (products, brutto, netto, price_kg, summ) '
                f'VALUES ("{name_product}", {brutto_product}, {netto_product}, {price_kg}, {summ})')
    base.commit()
