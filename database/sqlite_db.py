import sqlite3 as sq

#Создание/подключение бд
def sql_start():
    global base, cur
    base = sq.connect('menu_domashniy.db')#коннект к базе
    cur = base.cursor()#создание курсора
    if base:
        print('DataBase connected OK')
    base.execute('CREATE TABLE IF NOT EXISTS products(type_product TEXT, name_product TEXT, price TEXT)')#создаём таблицу бд(excecute - создание если нет)
    base.commit()#сохранение изменений



def sql_select():
    cur.execute('SELECT name_product FROM products WHERE type_product = "fishes"')
    rows = cur.fetchall()
    return rows
    #     # print(f'тип продукта - {row[0]}\n'
    #     #       f'название продукта - {row[1]}\n'
    #     #       f'цена - {row[2]}')

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO products VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()
