#!/usr/bin/python3
#-*-Coding:utf-8 -*-

# sql.py
import sqlite3

# Kreye koneksyon ak baz done a
conn = sqlite3.connect('finance_tracker.db')
cursor = conn.cursor()

# Kreye tab "users" si li pa deja ekziste
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Kreye tab "income" si li pa deja ekziste
cursor.execute('''
    CREATE TABLE IF NOT EXISTS income (
        income_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date DATE NOT NULL,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
''')

# Kreye tab "expenses" si li pa deja ekziste
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date DATE NOT NULL,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
''')

# Kreye tab "budgets" si li pa deja ekziste
cursor.execute('''
    CREATE TABLE IF NOT EXISTS budgets (
        budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
''')

# Kòmanse anrejistre
conn.commit()
conn.close()
