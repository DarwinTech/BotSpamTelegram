#DEV BY TELEGRAM: @ErzScarlet (Darwin R)

import sqlite3
import asyncio
from telethon import TelegramClient, events

DB_PATH = "bot.db"
db_lock = asyncio.Lock()
API_ID = 111111111  # TU_API_ID_AQUI
API_HASH = "TU_API_HASH_AQUI"
OWNER_ID = 8381560803
SPAM_INTERVAL = 300  # Tiempo en segundos entre envíos

client = TelegramClient('session', API_ID, API_HASH)

def db_conn():
    return sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False)

# =============================================================== #
# Función para inicializar las tablas de la DB
# =============================================================== #
def setup_db():
    conn = db_conn()
    cur = conn.cursor()
    

    cur.execute("""
        CREATE TABLE IF NOT EXISTS channels_chats (
            chat_id INTEGER PRIMARY KEY
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS scheduled_message (
            chat_id INTEGER,
            message_id INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS last_sent_message (
            chat_id INTEGER PRIMARY KEY,
            last_message_id INTEGER
        )
    """)
    conn.commit()
    conn.close()

# =============================================================== #
# /add - agregar grupo
# =============================================================== #
@client.on(events.NewMessage(pattern='/add'))
async def add_chat(event):
    if event.sender_id != OWNER_ID:
        return
    parts = event.text.split() 
    if len(parts) != 2:
        return await event.reply("Uso correcto: /add -1001234567890")
    chat_id = int(parts[1])

    async with db_lock:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO channels_chats (chat_id) VALUES (?)", (chat_id,))
        conn.commit()
        conn.close()

    await event.reply(f"✔ Chat agregado: `{chat_id}`")


@client.on(events.NewMessage(pattern='/send'))
async def cmd_send(event):
    if event.sender_id != OWNER_ID:
        return

    if not event.is_reply:
        return await event.reply("Responde al mensaje que quieres enviar periódicamente.")

    msg = await event.get_reply_message()

    async with db_lock:
        conn = db_conn()
        cur = conn.cursor()

        cur.execute("DELETE FROM scheduled_message")

        cur.execute("""
            INSERT INTO scheduled_message (chat_id, message_id)
            VALUES (?, ?)
        """, (msg.chat_id, msg.id))

        conn.commit()
        conn.close()

    await event.reply("✔ Mensaje guardado para envío automático.")


# =============================================================== #
# Auto-sender
# =============================================================== #
async def auto_sender():
    while True:
        async with db_lock:
            conn = db_conn()
            cur = conn.cursor()
            
            cur.execute("SELECT chat_id, message_id FROM scheduled_message ORDER BY rowid DESC LIMIT 1")
            row = cur.fetchone()
            
            if not row:
                conn.close()
                await asyncio.sleep(SPAM_INTERVAL)
                continue
                
            origin_chat, message_id = row
            
            cur.execute("SELECT c.chat_id, l.last_message_id FROM channels_chats c LEFT JOIN last_sent_message l ON c.chat_id = l.chat_id")
            targets_data = cur.fetchall()
            
            conn.close()

        for target, last_message_id in targets_data:
            try:
                if last_message_id:
                    await client.delete_messages(entity=target, message_ids=[last_message_id])
                    print(f"Mensaje anterior {last_message_id} eliminado de {target}")

                sent_message = await client.forward_messages(entity=target, messages=message_id, from_peer=origin_chat)
                print(f"Mensaje reenviado a {target}. Nuevo ID: {sent_message.id}")
                
                async with db_lock:
                    conn = db_conn()
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT OR REPLACE INTO last_sent_message (chat_id, last_message_id)
                        VALUES (?, ?)
                    """, (target, sent_message.id))
                    conn.commit()
                    conn.close()

            except Exception as e:
                print(f"Error procesando el envío a {target}. Error: {e}")

        await asyncio.sleep(SPAM_INTERVAL)
        
        
# =============================================================== #
# Iniciar client y auto_sender
# =============================================================== #
async def main():

    setup_db() 
    
    await client.start()
    print("Userbot ejecutándose…")

    asyncio.create_task(auto_sender())
    await client.run_until_disconnected()


asyncio.run(main())
