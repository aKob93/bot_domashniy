import re
import sqlite3 as sq
from conf import type_product, type_menu

#Создание/подключение бд
def sql_start():
    global base, cur
    base = sq.connect('menu_domashniyTEST.db')#коннект к базе
    cur = base.cursor()#создание курсора
    if base:
        print('DataBase connected OK')



#Выбор из таблицы название продукта и цену
def select_name_price_product(category):
    cur.execute(f'SELECT name_product, price, percent_off FROM products WHERE type_product = "{type_product[category]}"')
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
    base.commit()
    return name_price_products


#Изменение данных в таблице
def select_chages(name_product, price, percent):
    cur.execute(f'UPDATE products SET price = {price}, percent_off = {percent} '
                f'WHERE name_product = "{name_product}";')
    base.commit()



#Добавление данных
def sql_add_command(category, name, price, percent_off):
    cur.execute(f'INSERT INTO products (type_product, name_product, price, percent_off) VALUES '
                f'("{type_product[category]}", "{name}", {price}, {percent_off})')
    base.commit()



#Удаление данных
def sql_del(name):
    # print(f'DELETE FROM products WHERE name_product = "{name}";')
    cur.execute(f'DELETE FROM products WHERE name_product = "{name}";')
    base.commit()

#Удаление таблицы из меню
def del_menu(name):
    cur.execute(f'DROP TABLE "{name}";')
    cur.execute(f'DELETE FROM menu WHERE name = "{name}";')
    base.commit()


# подсчёт брутто цена за кг продукта
def get_percent_price(prod):

    percent = cur.execute(f'SELECT percent_off FROM products WHERE name_product = "{prod}";').fetchall()
    price = cur.execute(f'SELECT price FROM products WHERE name_product = "{prod}"').fetchall()
    patern = "[](',)[]"
    percent = re.sub(patern, '', str(percent))
    price = re.sub(patern, '', str(price))
    return percent, price


#Создание таблицыс блюдом
def create_table_dish(name_dishes):
    cur.execute(f'CREATE TABLE "{name_dishes}" (products TEXT, brutto REAL, netto REAL, price_kg REAL, summ REAL)')
    base.commit()

#Добавление блюд в таблицу
def add_table_dish(name_dishes, name_product, brutto_product, netto_product, price_kg, summ):
    cur.execute(f'INSERT INTO "{name_dishes}" (products, brutto, netto, price_kg, summ) '
                f'VALUES ("{name_product}", {brutto_product}, {netto_product}, {price_kg}, {summ})')
    base.commit()
#Добавление блюда в таблицу menu и с ценой себестоимости
def add_dishes_for_table_menu(type, name, price):
    cur.execute(f'INSERT INTO menu (type_menu, name, price) VALUES ("{type_menu[type]}", "{name}", {price})')
    base.commit()

#получение суммы цен
def get_price(name_dishes):
    price_sum = cur.execute(f'SELECT SUM(summ) FROM "{name_dishes}"').fetchall()
    base.commit()
    patern = "[](',)[]"
    price_sum = re.sub(patern, '', str(price_sum))
    return price_sum
#Получение суммы нетто
def get_netto(name_dishes):
    netto_sum = cur.execute(f'SELECT SUM(netto) FROM "{name_dishes}";').fetchall()
    base.commit()
    patern = "[](',)[]"
    netto_sum = re.sub(patern, '', str(netto_sum))
    return netto_sum

#Получение name из meny
def get_name_menu(type_name):
    names = cur.execute(f"SELECT name FROM menu WHERE type_menu = '{type_name}';").fetchall()

    names_menu = []
    for name in names:
        patern = "[(',)]"
        data = re.sub(patern, '', str(name))  # убирает лишние символы по patern
        names_menu.append(data)

    return names_menu

#Получение name price из menu
def get_name_price_menu(type):
    names = cur.execute(f"SELECT name, price FROM menu WHERE type_menu = '{type}';").fetchall()
    base.commit()
    name_price_products = []
    for data in names:
        patern = "[(',)]"
        data = re.sub(patern, '', str(data))  # убирает лишние символы по patern
        name_price_products.append(data)
    return name_price_products


#получение блюд из меню
def get_name_from_menu():
    names = cur.execute('SELECT name FROM menu;').fetchall()
    names_from_menu = []
    for name in names:
        patern = "[](',)[]"
        name = re.sub(patern, '', str(name))
        names_from_menu.append(name)
    return names_from_menu

def get_nameproduct_price():
    names_product = cur.execute('SELECT name_product FROM products;').fetchall()
    prices_product = cur.execute('SELECT price FROM products').fetchall()
    names_from_products = []
    prices_from_products = []
    for name in names_product:
        patern = "[](',)[]"
        name = re.sub(patern, '', str(name))
        names_from_products.append(name)
    for price in prices_product:
        patern = "[](',)[]"
        price = re.sub(patern, '', str(price))
        prices_from_products.append(price)
    name_price_zip = zip(names_from_products, prices_from_products)
    return name_price_zip
def select_product(dish):
    try:
        names_product = cur.execute(f'SELECT products FROM "{dish}";').fetchall()
        patern = "[](',)[]"
        names_product = re.sub(patern, '', str(names_product))
        return names_product
    except Exception:
        pass
def get_brutto(name, price):
    brutto = cur.execute(f'SELECT brutto FROM "{name}" WHERE products = "{price}";').fetchall()

    patern = "[](',)[]"
    brutto = re.sub(patern, '', str(brutto))
    base.commit()
    return brutto
def update_price():
    names_from_menu = get_name_from_menu()
    name_price_zip = get_nameproduct_price()
    name_price_zip = list(name_price_zip)

    for name in names_from_menu:
            names_product = select_product(name)
            for name_price in name_price_zip:

                try:
                    if name_price[0] in names_product:
                        price = float(name_price[1])
                        brutto = get_brutto(name, name_price[0])
                        brutto = float(brutto)
                        sum = round(price * brutto / 1000)
                        cur.execute(f'UPDATE "{name}" SET price_kg = {price}, summ = {sum} WHERE products = "{name_price[0]}"')
                        base.commit()

                except Exception as e:
                    print(e)
                    continue

    for name in names_from_menu:
        try:

            price_sum = cur.execute(f'SELECT SUM(summ) FROM "{name}"').fetchall()
            patern = "[](',)[]"
            price_sum = re.sub(patern, '', str(price_sum))
            price_sum = float(price_sum)
            netto = get_netto(name)
            netto = float(netto)

            price_s = round((price_sum * 1000) / netto)
            cur.execute(f'UPDATE menu SET price = {price_s} WHERE name = "{name}"')
            base.commit()
        except Exception:
            continue