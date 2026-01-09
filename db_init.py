# db_init.py
import sqlite3

DB = "bot.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    hora_envio TEXT,
    fecha_registro TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS channels_chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER UNIQUE,
    name_chat TEXT,
    register TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    fecha_registro TEXT
)
""")

conn.commit()
conn.close()

print("Base de datos creada correctamente.")
