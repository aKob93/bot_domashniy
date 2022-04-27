import sqlite3 as sq

PATTERN = "[](',)[]"
BASE = sq.connect('menu_domashniyTEST.db')  # коннект к базе
CUR = BASE.cursor()  # создание курсора


# Проверка подключения
def sql_start():
    if BASE:
        print('DataBase connected OK')



