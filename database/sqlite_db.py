import sqlite3 as sq

#Создание/подключение бд
def sql_start():
    global base, cur
    base = sq.connect('menu_domashniy.db')
    cur = base.cursor()
    if base:
        print('DataBase connected OK')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, price TEXT)')#создаём таблицу бд(excecute - создание если нет)
    base.commit()#сохранение изменений


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()
